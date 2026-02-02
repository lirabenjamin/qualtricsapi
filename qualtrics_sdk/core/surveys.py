"""
Survey Operations Mixin
Handles all survey CRUD operations
"""

import requests
from typing import Dict, List, Any


class SurveyMixin:
    """Mixin providing survey CRUD operations"""

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

    def get_survey_url(self, survey_id: str) -> str:
        """
        Get the public URL for a survey

        Args:
            survey_id: The survey ID

        Returns:
            Survey URL
        """
        return f"https://{self.data_center}/jfe/form/{survey_id}"
