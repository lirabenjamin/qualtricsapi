"""
Survey Operations Mixin
Handles all survey CRUD operations
"""

import inspect
import os
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional


class SurveyMixin:
    """Mixin providing survey CRUD operations"""

    def create_survey(
        self,
        survey_name: str,
        language: str = "EN",
        project_category: str = "CORE",
        setup_defaults: bool = True,
    ) -> Dict[str, Any]:
        """
        Create a new survey.

        By default, sets the survey to the "classic" look-and-feel template and
        adds standard embedded data fields (PROLIFIC_PID from URL, creation date,
        and the path of the script that created the survey).

        Args:
            survey_name: Name of the survey
            language: Survey language (default: "EN")
            project_category: Project category (default: "CORE")
            setup_defaults: If True, apply classic template and default embedded
                            data after creation (default: True)

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

        if response.status_code != 200:
            raise Exception(f"Failed to create survey: {response.text}")

        result = response.json()['result']

        if setup_defaults:
            survey_id = result['SurveyID']
            self._apply_default_options(survey_id)

        return result

    def _apply_default_options(self, survey_id: str) -> None:
        """Apply default options to a newly created survey (classic template + embedded data)."""
        self.set_survey_template(survey_id, "*classic")

        caller_path = self._get_caller_path()
        today = datetime.now().strftime("%Y-%m-%d")

        self.set_embedded_data_fields(survey_id, {
            "PROLIFIC_PID": {"type": "text"},
            "date_created": {"type": "text", "value": today},
            "created_by_script": {"type": "text", "value": caller_path},
        })

    @staticmethod
    def _get_caller_path() -> str:
        """Walk the call stack to find the first frame outside qualtrics_sdk."""
        for frame_info in inspect.stack():
            filename = frame_info.filename
            if "qualtrics_sdk" not in filename and filename != "<string>":
                return os.path.abspath(filename)
        return "unknown"

    def get_survey_options(self, survey_id: str) -> Dict[str, Any]:
        """
        Get survey options (look-and-feel, protection, navigation, etc.).

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with all survey options
        """
        response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/options',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get survey options: {response.text}")

    def update_survey_options(
        self, survey_id: str, updates: Dict[str, Any]
    ) -> bool:
        """
        Partially update survey options (GET-merge-PUT).

        Args:
            survey_id: The survey ID
            updates: Dictionary of option keys to update

        Returns:
            True if successful
        """
        options = self.get_survey_options(survey_id)
        options.update(updates)

        response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/options',
            headers=self.headers,
            json=options
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to update survey options: {response.text}")

    def set_survey_template(
        self, survey_id: str, template_id: str = "*classic"
    ) -> bool:
        """
        Set the survey's look-and-feel template.

        Args:
            survey_id: The survey ID
            template_id: Template identifier (default: "*classic").
                         Known values: "*base" (flat/modern), "*classic" (classic).

        Returns:
            True if successful
        """
        options = self.get_survey_options(survey_id)
        skin = options.get("Skin", {})
        skin["templateId"] = template_id
        return self.update_survey_options(survey_id, {"Skin": skin})

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

    def get_survey_url(self, survey_id: str) -> str:
        """
        Get the public URL for a survey

        Args:
            survey_id: The survey ID

        Returns:
            Survey URL
        """
        return f"https://{self.data_center}/jfe/form/{survey_id}"
