"""
Question Management Mixin
Handles updating, deleting, and retrieving existing questions
"""

import requests
from typing import Dict, List, Any


class QuestionManagementMixin:
    """Mixin providing question management operations"""

    def update_question(
        self, survey_id: str, question_id: str,
        question_data: Dict[str, Any]
    ) -> bool:
        """
        Update an existing question

        Args:
            survey_id: The survey ID
            question_id: The question ID to update
            question_data: Dictionary with updated question data

        Returns:
            True if successful
        """
        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to update question: {response.text}")

    def update_question_text(
        self, survey_id: str, question_id: str,
        new_text: str
    ) -> bool:
        """
        Update just the text of a question

        Args:
            survey_id: The survey ID
            question_id: The question ID to update
            new_text: New question text

        Returns:
            True if successful
        """
        question_data = {
            "QuestionText": new_text
        }
        return self.update_question(survey_id, question_id, question_data)

    def delete_question(self, survey_id: str, question_id: str) -> bool:
        """
        Delete a question from a survey

        Args:
            survey_id: The survey ID
            question_id: The question ID to delete

        Returns:
            True if successful
        """
        response = requests.delete(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to delete question: {response.text}")

    def get_question(self, survey_id: str, question_id: str) -> Dict[str, Any]:
        """
        Get details of a specific question

        Args:
            survey_id: The survey ID
            question_id: The question ID

        Returns:
            Dictionary with question details
        """
        response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get question: {response.text}")

    def get_survey_questions(self, survey_id: str) -> List[Dict[str, Any]]:
        """
        Get all questions from a survey

        Args:
            survey_id: The survey ID

        Returns:
            List of question dictionaries
        """
        survey = self.get_survey(survey_id)
        questions = []

        # Navigate through blocks to get questions
        if 'Blocks' in survey:
            for block_id, block in survey['Blocks'].items():
                if 'BlockElements' in block:
                    for element in block['BlockElements']:
                        if element['Type'] == 'Question':
                            question_id = element['QuestionID']
                            question = self.get_question(survey_id, question_id)
                            questions.append(question)

        return questions

    def add_page_break(self, survey_id: str, question_id: str) -> bool:
        """
        Add a page break before a question.

        This is essential for display logic to work properly - the source question
        must be on a previous page so its answer can be evaluated.

        Args:
            survey_id: The survey ID
            question_id: The question ID to add page break before

        Returns:
            True if successful

        Example:
            # Add page break before conditional question Q2
            api.add_page_break(survey_id, "QID2")
        """
        # Get current question data
        current_question = self.get_question(survey_id, question_id)

        # Update with page break configuration
        question_data = {
            'QuestionText': current_question.get('QuestionText', ''),
            'DataExportTag': current_question.get('DataExportTag'),
            'QuestionType': current_question.get('QuestionType'),
            'Selector': current_question.get('Selector'),
            'Configuration': current_question.get('Configuration', {})
        }

        # Add page break configuration
        if 'Configuration' not in question_data:
            question_data['Configuration'] = {}
        question_data['Configuration']['QuestionDescriptionOption'] = 'UseText'

        # Include SubSelector if present
        if current_question.get('SubSelector'):
            question_data['SubSelector'] = current_question['SubSelector']

        # Include Choices if present
        if current_question.get('Choices'):
            question_data['Choices'] = current_question['Choices']

        # Include Answers if present (for matrix questions)
        if current_question.get('Answers'):
            question_data['Answers'] = current_question['Answers']

        # Include ChoiceOrder if present
        if current_question.get('ChoiceOrder'):
            question_data['ChoiceOrder'] = current_question['ChoiceOrder']

        # Include DisplayLogic if present
        if current_question.get('DisplayLogic'):
            question_data['DisplayLogic'] = current_question['DisplayLogic']

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to add page break: {response.text}")
