"""
Embedded Data Operations Mixin
Handles embedded data field configuration and URL generation
"""

import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urlencode
import re


class EmbeddedDataMixin:
    """Mixin providing embedded data operations for Qualtrics surveys"""

    def get_survey_flow(self, survey_id: str) -> Dict[str, Any]:
        """
        Get the raw survey flow structure (for debugging).

        Args:
            survey_id: The survey ID

        Returns:
            The complete flow structure from the API
        """
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        return flow_response.json()['result']

    def _get_next_flow_id(self, flow_list: List[Dict]) -> str:
        """Generate a unique FlowID by finding the max existing ID and incrementing."""
        max_id = 0
        for element in flow_list:
            flow_id = element.get('FlowID', '')
            match = re.match(r'FL_(\d+)', flow_id)
            if match:
                max_id = max(max_id, int(match.group(1)))
            # Also check nested flows
            if 'Flow' in element and isinstance(element['Flow'], list):
                for nested in element['Flow']:
                    nested_id = nested.get('FlowID', '')
                    match = re.match(r'FL_(\d+)', nested_id)
                    if match:
                        max_id = max(max_id, int(match.group(1)))
        return f"FL_{max_id + 1}"

    def _count_flow_elements(self, flow_list: List[Dict]) -> int:
        """Count total flow elements including nested ones."""
        count = 0
        for element in flow_list:
            count += 1
            if 'Flow' in element and isinstance(element['Flow'], list):
                count += self._count_flow_elements(element['Flow'])
        return count

    def set_embedded_data(
        self,
        survey_id: str,
        field_name: str,
        field_type: str = "text",
        value: Optional[str] = None,
        position: str = "start"
    ) -> Dict[str, Any]:
        """
        Configure an individual embedded data field in a survey.

        Args:
            survey_id: The survey ID
            field_name: Name of the embedded data field
            field_type: Type of field - "text", "number", or "date" (default: "text")
            value: Optional default value for the field (can use Qualtrics piped text)
            position: Where to place in flow - "start" or "end" (default: "start")
                      Use "start" for data passed via URL or static values.
                      Use "end" for capturing question answers with piped text.

        Returns:
            Dictionary with the embedded data field configuration

        Raises:
            Exception: If the API call fails
            ValueError: If field_type is not valid
        """
        valid_types = ["text", "number", "date"]
        if field_type not in valid_types:
            raise ValueError(f"field_type must be one of {valid_types}")

        if position not in ["start", "end"]:
            raise ValueError("position must be 'start' or 'end'")

        # Get current survey flow
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        current_flow = flow_response.json()['result']
        flow_list = current_flow.get('Flow', [])

        # Build the embedded data field item
        field_item = {
            "Description": field_name,
            "Type": "Custom",
            "Field": field_name,
            "VariableType": "String",
            "DataVisibility": []
        }

        if value is not None:
            field_item["Value"] = value

        # Find the right position to insert
        if position == "start":
            insert_idx = 0
            # Check if first element is already EmbeddedData
            if flow_list and flow_list[0].get('Type') == 'EmbeddedData':
                # Add to existing first EmbeddedData block
                existing_fields = flow_list[0].get('EmbeddedData', [])
                field_exists = any(f.get('Field') == field_name for f in existing_fields)
                if field_exists:
                    for f in existing_fields:
                        if f.get('Field') == field_name:
                            f.update(field_item)
                            break
                else:
                    existing_fields.append(field_item)
                flow_list[0]['EmbeddedData'] = existing_fields
            else:
                # Create new EmbeddedData block at start
                new_element = {
                    "Type": "EmbeddedData",
                    "FlowID": self._get_next_flow_id(flow_list),
                    "EmbeddedData": [field_item]
                }
                flow_list.insert(0, new_element)
        else:  # position == "end"
            # Find or create EmbeddedData at the end (before EndSurvey if present)
            end_idx = len(flow_list)
            for i, element in enumerate(flow_list):
                if element.get('Type') == 'EndSurvey':
                    end_idx = i
                    break

            # Check if there's already an EmbeddedData right before end position
            if end_idx > 0 and flow_list[end_idx - 1].get('Type') == 'EmbeddedData':
                # Add to existing end EmbeddedData block
                existing_fields = flow_list[end_idx - 1].get('EmbeddedData', [])
                field_exists = any(f.get('Field') == field_name for f in existing_fields)
                if field_exists:
                    for f in existing_fields:
                        if f.get('Field') == field_name:
                            f.update(field_item)
                            break
                else:
                    existing_fields.append(field_item)
                flow_list[end_idx - 1]['EmbeddedData'] = existing_fields
            else:
                # Create new EmbeddedData block at end
                new_element = {
                    "Type": "EmbeddedData",
                    "FlowID": self._get_next_flow_id(flow_list),
                    "EmbeddedData": [field_item]
                }
                flow_list.insert(end_idx, new_element)

        current_flow['Flow'] = flow_list

        # Update Properties.Count
        if 'Properties' not in current_flow:
            current_flow['Properties'] = {}
        current_flow['Properties']['Count'] = self._count_flow_elements(flow_list)

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
                "position": position,
                "success": True
            }
        else:
            raise Exception(f"Failed to set embedded data: {update_response.text}")

    def set_embedded_data_fields(
        self,
        survey_id: str,
        fields: Dict[str, Dict[str, Any]],
        position: str = "start"
    ) -> Dict[str, Any]:
        """
        Configure multiple embedded data fields simultaneously.

        Args:
            survey_id: The survey ID
            fields: Dictionary mapping field names to their configuration.
                    Each field config can contain:
                    - "type": "text", "number", or "date" (default: "text")
                    - "value": optional default value (can use Qualtrics piped text)
            position: Where to place in flow - "start" or "end" (default: "start")
                      Use "start" for data passed via URL, static values, random numbers.
                      Use "end" for capturing question answers with piped text.

        Returns:
            Dictionary with all configured fields

        Raises:
            Exception: If the API call fails

        Example:
            >>> # Static values and random numbers at start
            >>> api.set_embedded_data_fields(survey_id, {
            ...     "random_id": {"type": "text", "value": "${rand://int/1:1000}"},
            ...     "version": {"type": "text", "value": "v1.0"}
            ... }, position="start")
            >>>
            >>> # Capture question answers at end
            >>> api.set_embedded_data_fields(survey_id, {
            ...     "user_answer": {"type": "text", "value": "${q://QID1/ChoiceGroup/SelectedChoices}"}
            ... }, position="end")
        """
        if position not in ["start", "end"]:
            raise ValueError("position must be 'start' or 'end'")

        # Get current survey flow
        flow_response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}/flow',
            headers=self.headers
        )

        if flow_response.status_code != 200:
            raise Exception(f"Failed to get survey flow: {flow_response.text}")

        current_flow = flow_response.json()['result']
        flow_list = current_flow.get('Flow', [])

        # Build embedded data items for all fields
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
                "Type": "Custom",
                "Field": field_name,
                "VariableType": "String",
                "DataVisibility": []
            }

            if value is not None:
                item["Value"] = value

            embedded_data_items.append(item)

        # Insert based on position
        if position == "start":
            # Check if first element is already EmbeddedData
            if flow_list and flow_list[0].get('Type') == 'EmbeddedData':
                existing_fields = flow_list[0].get('EmbeddedData', [])
                existing_names = {f.get('Field') for f in existing_fields}

                for item in embedded_data_items:
                    if item['Field'] in existing_names:
                        # Update existing
                        for f in existing_fields:
                            if f.get('Field') == item['Field']:
                                f.update(item)
                                break
                    else:
                        existing_fields.append(item)

                flow_list[0]['EmbeddedData'] = existing_fields
            else:
                # Create new EmbeddedData block at start
                new_element = {
                    "Type": "EmbeddedData",
                    "FlowID": self._get_next_flow_id(flow_list),
                    "EmbeddedData": embedded_data_items
                }
                flow_list.insert(0, new_element)
        else:  # position == "end"
            # Find end position (before EndSurvey if present)
            end_idx = len(flow_list)
            for i, element in enumerate(flow_list):
                if element.get('Type') == 'EndSurvey':
                    end_idx = i
                    break

            # Check if there's already an EmbeddedData right before end
            # But NOT at position 0 (that's the start block)
            if end_idx > 1 and flow_list[end_idx - 1].get('Type') == 'EmbeddedData':
                existing_fields = flow_list[end_idx - 1].get('EmbeddedData', [])
                existing_names = {f.get('Field') for f in existing_fields}

                for item in embedded_data_items:
                    if item['Field'] in existing_names:
                        for f in existing_fields:
                            if f.get('Field') == item['Field']:
                                f.update(item)
                                break
                    else:
                        existing_fields.append(item)

                flow_list[end_idx - 1]['EmbeddedData'] = existing_fields
            else:
                # Create new EmbeddedData block at end
                new_element = {
                    "Type": "EmbeddedData",
                    "FlowID": self._get_next_flow_id(flow_list),
                    "EmbeddedData": embedded_data_items
                }
                flow_list.insert(end_idx, new_element)

        current_flow['Flow'] = flow_list

        # Update Properties.Count
        if 'Properties' not in current_flow:
            current_flow['Properties'] = {}
        current_flow['Properties']['Count'] = self._count_flow_elements(flow_list)

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
                "position": position,
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

        # Update Properties.Count
        if 'Properties' not in current_flow:
            current_flow['Properties'] = {}
        current_flow['Properties']['Count'] = self._count_flow_elements(flow_list)

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
