"""
Question Creation Mixin
Handles creation of all question types
"""

import re
import requests
from typing import Dict, List, Any, Optional


class QuestionMixin:
    """Mixin providing question creation methods for all question types"""

    def _send_question(
        self,
        survey_id: str,
        question_data: Dict[str, Any],
        question_id: Optional[str] = None,
        block_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new question or replace an existing one in place.

        When question_id is provided, PUTs to replace the question at that QID,
        preserving its position in the block. When absent, POSTs to create a new
        question (appended to block_id or the default block).

        Args:
            survey_id: The survey ID
            question_data: Full question payload
            question_id: If provided, replace this question in place (PUT)
            block_id: For new questions only — which block to append to

        Returns:
            Dictionary with question details including QuestionID
        """
        if question_id:
            url = f"{self.base_url}/survey-definitions/{survey_id}/questions/{question_id}"
            response = requests.put(url, headers=self.headers, json=question_data)
        else:
            url = f"{self.base_url}/survey-definitions/{survey_id}/questions"
            params = {"blockId": block_id} if block_id else None
            response = requests.post(url, headers=self.headers, json=question_data, params=params)

        if response.status_code == 200:
            body = response.json()
            if question_id:
                # PUT returns no result key — just confirm success
                return {"QuestionID": question_id}
            return body["result"]
        else:
            action = "update" if question_id else "create"
            raise Exception(f"Failed to {action} question: {response.text}")

    def _generate_data_export_tag(self, question_text: str) -> str:
        """
        Generate a data export tag from question text.

        Args:
            question_text: The question text

        Returns:
            Sanitized export tag
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', question_text[:30])

    def create_multiple_choice_question(
        self, survey_id: str, question_text: str,
        choices: List[str],
        selector: str = "SAVR",
        allow_multiple: bool = False,
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a multiple choice question, or replace an existing question in place.

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
            block_id: Optional block ID to add question to specific block
            question_id: If provided, replace this existing question in place

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

        # Build choice order (list of choice IDs in order)
        choice_order = [str(i) for i in range(1, len(choices) + 1)]

        question_data = {
            "QuestionText": question_text,
            "QuestionType": "MC",
            "Selector": selector,
            "SubSelector": "TX",
            "Choices": choices_dict,
            "ChoiceOrder": choice_order,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        return self._send_question(survey_id, question_data, question_id, block_id)

    def create_text_entry_question(
        self, survey_id: str, question_text: str,
        text_type: str = "SL",
        data_export_tag: Optional[str] = None,
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a text entry question, or replace an existing question in place.

        Args:
            survey_id: The survey ID
            question_text: The question text
            text_type: "SL" for single line, "ML" for multi-line (essay),
                      "Form" for form field
            data_export_tag: Optional export tag (auto-generated if not provided)
            block_id: Optional block ID to add question to specific block
            question_id: If provided, replace this existing question in place

        Returns:
            Dictionary with question details
        """
        if data_export_tag is None:
            data_export_tag = self._generate_data_export_tag(question_text)

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "TE",
            "Selector": text_type,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        return self._send_question(survey_id, question_data, question_id, block_id)

    def create_matrix_question(
        self, survey_id: str, question_text: str,
        statements: List[str], scale_points: List[str],
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a matrix (Likert scale) question, or replace an existing question in place.

        Args:
            survey_id: The survey ID
            question_text: The question text
            statements: List of statement texts (rows)
            scale_points: List of scale point labels (columns)
            block_id: Optional block ID to add question to specific block
            question_id: If provided, replace this existing question in place

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

        return self._send_question(survey_id, question_data, question_id, block_id)

    def create_slider_question(
        self, survey_id: str, question_text: str,
        min_value: int = 0, max_value: int = 100,
        left_label: str = "", right_label: str = "",
        data_export_tag: Optional[str] = None,
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a slider question, or replace an existing question in place.

        Args:
            survey_id: The survey ID
            question_text: The question text
            min_value: Minimum slider value
            max_value: Maximum slider value
            left_label: Label for left side
            right_label: Label for right side
            data_export_tag: Optional export tag (auto-generated if not provided)
            block_id: Optional block ID to add question to specific block
            question_id: If provided, replace this existing question in place

        Returns:
            Dictionary with question details
        """
        if data_export_tag is None:
            data_export_tag = self._generate_data_export_tag(question_text)

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "Slider",
            "Selector": "HSLIDER",
            "Configuration": {
                "QuestionDescriptionOption": "UseText",
                "GridLines": 0,
                "NumDecimals": "0",
                "ShowValue": True
            },
            "Choices": {
                "1": {
                    "Display": question_text
                }
            },
            "ChoiceOrder": [1]
        }

        if left_label or right_label:
            question_data["Labels"] = {}
            if left_label:
                question_data["Labels"][str(min_value)] = {"Display": left_label}
            if right_label:
                question_data["Labels"][str(max_value)] = {"Display": right_label}

        return self._send_question(survey_id, question_data, question_id, block_id)

    def create_rank_order_question(
        self, survey_id: str, question_text: str,
        items: List[str],
        data_export_tag: Optional[str] = None,
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a rank order question, or replace an existing question in place.

        Args:
            survey_id: The survey ID
            question_text: The question text
            items: List of items to rank
            data_export_tag: Optional export tag (auto-generated if not provided)
            block_id: Optional block ID to add question to specific block
            question_id: If provided, replace this existing question in place

        Returns:
            Dictionary with question details
        """
        if data_export_tag is None:
            data_export_tag = self._generate_data_export_tag(question_text)

        choices_dict = {}
        for i, item in enumerate(items, start=1):
            choices_dict[str(i)] = {"Display": item}

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "RO",
            "Selector": "DND",
            "SubSelector": "TX",
            "Choices": choices_dict,
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        return self._send_question(survey_id, question_data, question_id, block_id)

    def create_nps_question(
        self, survey_id: str,
        question_text: Optional[str] = None,
        left_label: str = "Not at all likely",
        right_label: str = "Extremely likely",
        data_export_tag: Optional[str] = None,
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a Net Promoter Score (NPS) question, or replace an existing question in place.

        Creates a 0-10 horizontal scale with labeled endpoints. Uses the native
        Qualtrics NPS selector (MC/NPS) with ColumnLabels for endpoint text.

        Args:
            survey_id: The survey ID
            question_text: The question text (default: standard NPS question)
            left_label: Label for the 0 end of the scale (default: "Not at all likely")
            right_label: Label for the 10 end of the scale (default: "Extremely likely")
            data_export_tag: Optional export tag (auto-generated if not provided)
            block_id: Optional block ID to add question to specific block
            question_id: If provided, replace this existing question in place

        Returns:
            Dictionary with question details
        """
        if question_text is None:
            question_text = "How likely are you to recommend us to a friend or colleague?"

        if data_export_tag is None:
            data_export_tag = self._generate_data_export_tag(question_text)

        # NPS is a 0-10 scale
        choices_dict = {}
        for i in range(11):
            choices_dict[str(i)] = {"Display": str(i)}

        question_data = {
            "QuestionText": question_text,
            "DataExportTag": data_export_tag,
            "QuestionType": "MC",
            "Selector": "NPS",
            "SubSelector": "TX",
            "Choices": choices_dict,
            "ChoiceOrder": [str(i) for i in range(11)],
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            },
            "ColumnLabels": [
                {"Display": left_label, "IsLabelDefault": False},
                {"Display": right_label, "IsLabelDefault": False},
            ],
        }

        return self._send_question(survey_id, question_data, question_id, block_id)

    def create_descriptive_text(
        self, survey_id: str, text: str,
        block_id: Optional[str] = None,
        question_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create descriptive text, or replace an existing question in place.

        Args:
            survey_id: The survey ID
            text: The descriptive text to display
            block_id: Optional block ID to add text to specific block
            question_id: If provided, replace this existing question in place

        Returns:
            Dictionary with question details
        """
        question_data = {
            "QuestionText": text,
            "QuestionType": "DB",
            "Selector": "TB",
            "SubSelector": "TX",
            "Configuration": {
                "QuestionDescriptionOption": "UseText"
            }
        }

        return self._send_question(survey_id, question_data, question_id, block_id)
