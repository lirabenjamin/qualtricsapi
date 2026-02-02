"""
Qualtrics API Module
A comprehensive Python wrapper for the Qualtrics REST API v3
Supports survey creation, deletion, and question management with all question types.
"""

import requests
from typing import Dict, List, Optional, Any


class QualtricsAPI:
    """Main class for interacting with the Qualtrics API"""

    def __init__(self, api_token: str, data_center: str):
        """
        Initialize the Qualtrics API client

        Args:
            api_token: Your Qualtrics API token
            data_center: Your data center (e.g., 'upenn.qualtrics.com')
        """
        self.api_token = api_token
        self.data_center = data_center
        self.base_url = f'https://{data_center}/API/v3'
        self.headers = {
            'X-API-TOKEN': api_token,
            'Content-Type': 'application/json'
        }

    # ==================== SURVEY OPERATIONS ====================

    def create_survey(self, survey_name: str, language: str = "EN",
                     project_category: str = "CORE") -> Dict[str, Any]:
        """
        Create a new survey

        Args:
            survey_name: Name of the survey
            language: Survey language (default: "EN")
            project_category: Project category (default: "CORE")

        Returns:
            Dictionary with survey details including SurveyID
        """
        survey_data = {
            "SurveyName": survey_name,
            "Language": language,
            "ProjectCategory": project_category
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions',
            headers=self.headers,
            json=survey_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create survey: {response.text}")

    def get_survey(self, survey_id: str) -> Dict[str, Any]:
        """
        Get survey details

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with complete survey details
        """
        response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get survey: {response.text}")

    def delete_survey(self, survey_id: str) -> bool:
        """
        Delete a survey

        Args:
            survey_id: The survey ID to delete

        Returns:
            True if successful
        """
        response = requests.delete(
            f'{self.base_url}/survey-definitions/{survey_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to delete survey: {response.text}")

    def list_surveys(self) -> List[Dict[str, Any]]:
        """
        List all surveys in your account

        Returns:
            List of survey dictionaries
        """
        response = requests.get(
            f'{self.base_url}/surveys',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']['elements']
        else:
            raise Exception(f"Failed to list surveys: {response.text}")

    def update_survey_name(self, survey_id: str, new_name: str) -> bool:
        """
        Update survey name

        Args:
            survey_id: The survey ID
            new_name: New name for the survey

        Returns:
            True if successful
        """
        update_data = {
            "SurveyName": new_name
        }

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}',
            headers=self.headers,
            json=update_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to update survey name: {response.text}")

    # ==================== QUESTION OPERATIONS ====================

    def create_multiple_choice_question(self, survey_id: str, question_text: str,
                                       choices: List[str],
                                       selector: str = "SAVR",
                                       allow_multiple: bool = False) -> Dict[str, Any]:
        """
        Create a multiple choice question (radio buttons or checkboxes)

        Args:
            survey_id: The survey ID
            question_text: The question text
            choices: List of choice texts
            selector: "SAVR" for single answer vertical (radio buttons),
                     "SAHR" for single answer horizontal,
                     "DL" for dropdown list
                     "MAVR" for multiple answer vertical (checkboxes) - use allow_multiple=True
                     "MAHR" for multiple answer horizontal - use allow_multiple=True
            allow_multiple: Set to True for checkboxes (multiple answers)

        Returns:
            Dictionary with question details including QuestionID
        """
        # Build choices dictionary
        choices_dict = {}
        for i, choice in enumerate(choices, start=1):
            choices_dict[str(i)] = {"Display": choice}

        # Adjust selector for multiple answer questions
        if allow_multiple:
            if selector == "SAVR":
                selector = "MAVR"
            elif selector == "SAHR":
                selector = "MAHR"

        question_data = {
            "QuestionText": question_text,
            "QuestionType": "MC",
            "Selector": selector,
            "Choices": choices_dict,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create question: {response.text}")

    def create_text_entry_question(self, survey_id: str, question_text: str,
                                   text_type: str = "SL",
                                   data_export_tag: str = None) -> Dict[str, Any]:
        """
        Create a text entry question

        Args:
            survey_id: The survey ID
            question_text: The question text
            text_type: "SL" for single line, "ML" for multi-line (essay),
                      "Form" for form field
            data_export_tag: Optional export tag (auto-generated if not provided)

        Returns:
            Dictionary with question details
        """
        if data_export_tag is None:
            # Generate a simple tag from the question text
            import re
            data_export_tag = re.sub(r'[^a-zA-Z0-9]', '_', question_text[:30])

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "TE",
            "Selector": text_type,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create text entry question: {response.text}")

    def create_matrix_question(self, survey_id: str, question_text: str,
                              statements: List[str], scale_points: List[str]) -> Dict[str, Any]:
        """
        Create a matrix (Likert scale) question

        Args:
            survey_id: The survey ID
            question_text: The question text
            statements: List of statement texts (rows)
            scale_points: List of scale point labels (columns)

        Returns:
            Dictionary with question details
        """
        # Build statements dictionary
        statements_dict = {}
        for i, statement in enumerate(statements, start=1):
            statements_dict[str(i)] = {"Display": statement}

        # Build scale points dictionary
        answers_dict = {}
        for i, point in enumerate(scale_points, start=1):
            answers_dict[str(i)] = {"Display": point}

        question_data = {
            "QuestionText": question_text,
            "QuestionType": "Matrix",
            "Selector": "Likert",
            "SubSelector": "SingleAnswer",
            "Choices": statements_dict,
            "Answers": answers_dict,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create matrix question: {response.text}")

    def create_slider_question(self, survey_id: str, question_text: str,
                              min_value: int = 0, max_value: int = 100,
                              left_label: str = "", right_label: str = "",
                              data_export_tag: str = None) -> Dict[str, Any]:
        """
        Create a slider question

        Args:
            survey_id: The survey ID
            question_text: The question text
            min_value: Minimum slider value
            max_value: Maximum slider value
            left_label: Label for left side
            right_label: Label for right side
            data_export_tag: Optional export tag (auto-generated if not provided)

        Returns:
            Dictionary with question details
        """
        if data_export_tag is None:
            import re
            data_export_tag = re.sub(r'[^a-zA-Z0-9]', '_', question_text[:30])

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "Slider",
            "Selector": "HSLIDER",
            "Configuration": {
                "QuestionDescriptionOption": "UseText",
                "GridLines": max_value - min_value + 1,
                "NumDecimals": "0",
                "ShowValue": True
            },
            "Choices": {
                "1": {
                    "Display": question_text
                }
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create slider question: {response.text}")

    def create_rank_order_question(self, survey_id: str, question_text: str,
                                   items: List[str],
                                   data_export_tag: str = None) -> Dict[str, Any]:
        """
        Create a rank order question

        Args:
            survey_id: The survey ID
            question_text: The question text
            items: List of items to rank
            data_export_tag: Optional export tag (auto-generated if not provided)

        Returns:
            Dictionary with question details
        """
        if data_export_tag is None:
            import re
            data_export_tag = re.sub(r'[^a-zA-Z0-9]', '_', question_text[:30])

        choices_dict = {}
        for i, item in enumerate(items, start=1):
            choices_dict[str(i)] = {"Display": item}

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "RO",
            "Selector": "DND",  # Drag and Drop
            "Choices": choices_dict,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create rank order question: {response.text}")

    def create_nps_question(self, survey_id: str, question_text: str = None) -> Dict[str, Any]:
        """
        Create a Net Promoter Score (NPS) question

        Args:
            survey_id: The survey ID
            question_text: The question text (default: standard NPS question)

        Returns:
            Dictionary with question details
        """
        if question_text is None:
            question_text = "How likely are you to recommend us to a friend or colleague?"

        # NPS is a 0-10 scale
        choices_dict = {}
        for i in range(11):
            choices_dict[str(i)] = {"Display": str(i)}

        question_data = {
            "QuestionText": question_text,
            "QuestionType": "MC",
            "Selector": "SAHR",  # Single answer horizontal
            "Choices": choices_dict,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create NPS question: {response.text}")

    def create_descriptive_text(self, survey_id: str, text: str) -> Dict[str, Any]:
        """
        Create descriptive text (non-question text block)

        Args:
            survey_id: The survey ID
            text: The descriptive text to display

        Returns:
            Dictionary with question details
        """
        question_data = {
            "QuestionText": text,
            "QuestionType": "DB",
            "Selector": "TB",
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/questions',
            headers=self.headers,
            json=question_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create descriptive text: {response.text}")

    def update_question(self, survey_id: str, question_id: str,
                       question_data: Dict[str, Any]) -> bool:
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

    def update_question_text(self, survey_id: str, question_id: str,
                            new_text: str) -> bool:
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

    # ==================== BLOCK OPERATIONS ====================

    def get_blocks(self, survey_id: str) -> Dict[str, Any]:
        """
        Get all blocks in a survey

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with block details
        """
        response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/blocks',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get blocks: {response.text}")

    def create_block(self, survey_id: str, block_name: str) -> Dict[str, Any]:
        """
        Create a new block in a survey

        Args:
            survey_id: The survey ID
            block_name: Name for the new block

        Returns:
            Dictionary with block details
        """
        block_data = {
            "Description": block_name,
            "Type": "Standard"
        }

        response = requests.post(
            f'{self.base_url}/survey-definitions/{survey_id}/blocks',
            headers=self.headers,
            json=block_data
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create block: {response.text}")

    # ==================== HELPER METHODS ====================

    def get_survey_url(self, survey_id: str) -> str:
        """
        Get the public URL for a survey

        Args:
            survey_id: The survey ID

        Returns:
            Survey URL
        """
        return f"https://{self.data_center}/jfe/form/{survey_id}"

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
