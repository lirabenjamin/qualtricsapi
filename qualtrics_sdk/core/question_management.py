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
