"""
Embedded Data Operations Mixin
Handles embedded data field configuration and URL generation
"""

import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urlencode


class EmbeddedDataMixin:
    """Mixin providing embedded data operations for Qualtrics surveys"""

    def set_embedded_data(
        self,
        survey_id: str,
        field_name: str,
        field_type: str = "text",
        value: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Configure an individual embedded data field in a survey.

        Embedded data fields allow you to pass respondent details, capture
        external data, and control survey flow.

        Args:
            survey_id: The survey ID
            field_name: Name of the embedded data field
            field_type: Type of field - "text", "number", or "date" (default: "text")
            value: Optional default value for the field

        Returns:
            Dictionary with the embedded data field configuration

        Raises:
            Exception: If the API call fails
            ValueError: If field_type is not valid
        """
        valid_types = ["text", "number", "date"]
        if field_type not in valid_types:
            raise ValueError(f"field_type must be one of {valid_types}")

        # Get current survey flow to add embedded data
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        current_flow = flow_response.json()['result']

        # Build embedded data element
        embedded_data_element = {
            "Type": "EmbeddedData",
            "FlowID": f"FL_{len(current_flow.get('Flow', []))+1}",
            "EmbeddedData": [
                {
                    "Description": field_name,
                    "Type": field_type.capitalize() if field_type != "text" else "Recipient",
                    "Field": field_name,
                    "VariableType": "String" if field_type == "text" else (
                        "Number" if field_type == "number" else "Date"
                    ),
                    "DataVisibility": [],
                    "AnalyzeText": False
                }
            ]
        }

        if value is not None:
            embedded_data_element["EmbeddedData"][0]["Value"] = value

        # Check if embedded data already exists in flow
        flow_list = current_flow.get('Flow', [])
        embedded_data_exists = False

        for i, element in enumerate(flow_list):
            if element.get('Type') == 'EmbeddedData':
                # Add to existing embedded data element
                existing_fields = element.get('EmbeddedData', [])
                # Check if field already exists
                field_exists = any(
                    f.get('Field') == field_name for f in existing_fields
                )
                if not field_exists:
                    existing_fields.append(embedded_data_element["EmbeddedData"][0])
                    element['EmbeddedData'] = existing_fields
                else:
                    # Update existing field
                    for f in existing_fields:
                        if f.get('Field') == field_name:
                            f.update(embedded_data_element["EmbeddedData"][0])
                            break
                embedded_data_exists = True
                break

        if not embedded_data_exists:
            # Insert at the beginning of flow (before blocks)
            flow_list.insert(0, embedded_data_element)

        current_flow['Flow'] = flow_list

        # Update the flow
        update_response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers,
            json=current_flow
        )

        if update_response.status_code == 200:
            return {
                "field_name": field_name,
                "field_type": field_type,
                "value": value,
                "success": True
            }
        else:
            raise Exception(f"Failed to set embedded data: {update_response.text}")

    def set_embedded_data_fields(
        self,
        survey_id: str,
        fields: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Configure multiple embedded data fields simultaneously.

        Args:
            survey_id: The survey ID
            fields: Dictionary mapping field names to their configuration.
                    Each field config can contain:
                    - "type": "text", "number", or "date" (default: "text")
                    - "value": optional default value

        Returns:
            Dictionary with all configured fields

        Raises:
            Exception: If the API call fails

        Example:
            >>> api.set_embedded_data_fields(survey_id, {
            ...     "user_id": {"type": "text"},
            ...     "score": {"type": "number", "value": "0"},
            ...     "start_date": {"type": "date"}
            ... })
        """
        # Get current survey flow
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        current_flow = flow_response.json()['result']

        # Build embedded data elements for all fields
        embedded_data_items = []
        for field_name, config in fields.items():
            field_type = config.get("type", "text")
            value = config.get("value")

            valid_types = ["text", "number", "date"]
            if field_type not in valid_types:
                raise ValueError(
                    f"field_type for '{field_name}' must be one of {valid_types}"
                )

            item = {
                "Description": field_name,
                "Type": field_type.capitalize() if field_type != "text" else "Recipient",
                "Field": field_name,
                "VariableType": "String" if field_type == "text" else (
                    "Number" if field_type == "number" else "Date"
                ),
                "DataVisibility": [],
                "AnalyzeText": False
            }

            if value is not None:
                item["Value"] = value

            embedded_data_items.append(item)

        # Check if embedded data already exists in flow
        flow_list = current_flow.get('Flow', [])
        embedded_data_exists = False

        for element in flow_list:
            if element.get('Type') == 'EmbeddedData':
                existing_fields = element.get('EmbeddedData', [])
                existing_field_names = {f.get('Field') for f in existing_fields}

                for item in embedded_data_items:
                    if item['Field'] in existing_field_names:
                        # Update existing field
                        for f in existing_fields:
                            if f.get('Field') == item['Field']:
                                f.update(item)
                                break
                    else:
                        # Add new field
                        existing_fields.append(item)

                element['EmbeddedData'] = existing_fields
                embedded_data_exists = True
                break

        if not embedded_data_exists:
            # Create new embedded data element
            embedded_data_element = {
                "Type": "EmbeddedData",
                "FlowID": f"FL_{len(flow_list)+1}",
                "EmbeddedData": embedded_data_items
            }
            flow_list.insert(0, embedded_data_element)

        current_flow['Flow'] = flow_list

        # Update the flow
        update_response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers,
            json=current_flow
        )

        if update_response.status_code == 200:
            return {
                "fields": list(fields.keys()),
                "count": len(fields),
                "success": True
            }
        else:
            raise Exception(f"Failed to set embedded data fields: {update_response.text}")

    def get_embedded_data(self, survey_id: str) -> List[Dict[str, Any]]:
        """
        Get all embedded data fields configured in a survey.

        Args:
            survey_id: The survey ID

        Returns:
            List of embedded data field configurations

        Raises:
            Exception: If the API call fails
        """
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        current_flow = flow_response.json()['result']
        flow_list = current_flow.get('Flow', [])

        embedded_data_fields = []
        for element in flow_list:
            if element.get('Type') == 'EmbeddedData':
                embedded_data_fields.extend(element.get('EmbeddedData', []))

        return embedded_data_fields

    def delete_embedded_data(
        self,
        survey_id: str,
        field_name: str
    ) -> bool:
        """
        Delete an embedded data field from a survey.

        Args:
            survey_id: The survey ID
            field_name: Name of the embedded data field to delete

        Returns:
            True if successful

        Raises:
            Exception: If the API call fails
        """
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        current_flow = flow_response.json()['result']
        flow_list = current_flow.get('Flow', [])

        field_found = False
        for element in flow_list:
            if element.get('Type') == 'EmbeddedData':
                existing_fields = element.get('EmbeddedData', [])
                new_fields = [
                    f for f in existing_fields if f.get('Field') != field_name
                ]
                if len(new_fields) != len(existing_fields):
                    field_found = True
                    element['EmbeddedData'] = new_fields
                break

        if not field_found:
            raise Exception(f"Embedded data field '{field_name}' not found")

        current_flow['Flow'] = flow_list

        update_response = requests.put(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers,
            json=current_flow
        )

        if update_response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to delete embedded data: {update_response.text}")

    def get_survey_url_with_embedded_data(
        self,
        survey_id: str,
        embedded_data: Dict[str, str]
    ) -> str:
        """
        Generate a survey URL pre-populated with embedded data values.

        This creates a URL that passes embedded data as query parameters,
        allowing you to personalize the survey experience for each respondent.

        Args:
            survey_id: The survey ID
            embedded_data: Dictionary mapping field names to their values
                          Values will be URL-encoded automatically

        Returns:
            Survey URL with embedded data as query parameters

        Example:
            >>> url = api.get_survey_url_with_embedded_data(
            ...     survey_id,
            ...     {
            ...         "user_id": "12345",
            ...         "name": "John Doe",
            ...         "source": "email_campaign"
            ...     }
            ... )
            >>> print(url)
            https://datacenter.qualtrics.com/jfe/form/SV_xxx?user_id=12345&name=John%20Doe&source=email_campaign
        """
        base_url = f"https://{self.data_center}/jfe/form/{survey_id}"

        if not embedded_data:
            return base_url

        query_string = urlencode(embedded_data)
        return f"{base_url}?{query_string}"
