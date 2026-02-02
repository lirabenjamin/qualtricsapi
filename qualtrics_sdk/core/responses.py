"""
Response Management Mixin
Handles survey response operations including retrieval, export, and deletion
"""

import requests
import time
import io
import zipfile
from typing import Dict, List, Any, Optional


class ResponseMixin:
    """Mixin providing survey response management operations"""

    def get_response_count(self, survey_id: str) -> int:
        """
        Get the total number of responses for a survey

        Args:
            survey_id: The survey ID

        Returns:
            Total count of responses
        """
        response = requests.get(
            f'{self.base_url}/surveys/{survey_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            result = response.json()['result']
            return result.get('responseCounts', {}).get('auditable', 0)
        else:
            raise Exception(f"Failed to get response count: {response.text}")

    def list_responses(
        self,
        survey_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        List survey responses with optional filtering and pagination

        Args:
            survey_id: The survey ID
            start_date: Filter responses after this date (ISO 8601 format, e.g., "2024-01-01T00:00:00Z")
            end_date: Filter responses before this date (ISO 8601 format)
            status: Filter by response status (e.g., "Complete", "Incomplete")
            limit: Maximum number of responses to return (default: 100)
            offset: Number of responses to skip for pagination (default: 0)

        Returns:
            Dictionary containing 'responses' list and pagination info
        """
        params = {
            'limit': limit,
            'offset': offset
        }

        if start_date:
            params['startDate'] = start_date
        if end_date:
            params['endDate'] = end_date
        if status:
            params['status'] = status

        response = requests.get(
            f'{self.base_url}/surveys/{survey_id}/responses',
            headers=self.headers,
            params=params
        )

        if response.status_code == 200:
            result = response.json()['result']
            return {
                'responses': result.get('elements', []),
                'nextPage': result.get('nextPage'),
                'total': len(result.get('elements', []))
            }
        else:
            raise Exception(f"Failed to list responses: {response.text}")

    def get_response(self, survey_id: str, response_id: str) -> Dict[str, Any]:
        """
        Get a single response by ID

        Args:
            survey_id: The survey ID
            response_id: The response ID

        Returns:
            Dictionary with response details
        """
        response = requests.get(
            f'{self.base_url}/surveys/{survey_id}/responses/{response_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get response: {response.text}")

    def export_responses(
        self,
        survey_id: str,
        format: str = "csv",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        compress: bool = True,
        include_labels: bool = True,
        poll_interval: float = 1.0,
        max_wait: float = 300.0
    ) -> bytes:
        """
        Export survey responses in the specified format

        This method initiates an asynchronous export, polls for completion,
        and returns the exported data.

        Args:
            survey_id: The survey ID
            format: Export format - "csv", "json", "spss", or "xml" (default: "csv")
            start_date: Export responses after this date (ISO 8601 format)
            end_date: Export responses before this date (ISO 8601 format)
            compress: Whether to compress the export as a zip file (default: True)
            include_labels: Include question labels in export (default: True)
            poll_interval: Seconds between progress checks (default: 1.0)
            max_wait: Maximum seconds to wait for export (default: 300.0)

        Returns:
            Bytes containing the exported data (zip file if compress=True)
        """
        # Validate format
        valid_formats = ['csv', 'json', 'spss', 'xml']
        format_lower = format.lower()
        if format_lower not in valid_formats:
            raise ValueError(f"Invalid format '{format}'. Must be one of: {valid_formats}")

        # Map format to Qualtrics format specification
        format_map = {
            'csv': 'csv',
            'json': 'json',
            'spss': 'spss',
            'xml': 'xml'
        }

        # Build export request
        export_data = {
            'format': format_map[format_lower],
            'compress': compress,
            'includeDisplayOrder': include_labels
        }

        if start_date:
            export_data['startDate'] = start_date
        if end_date:
            export_data['endDate'] = end_date

        # Start export
        response = requests.post(
            f'{self.base_url}/surveys/{survey_id}/export-responses',
            headers=self.headers,
            json=export_data
        )

        if response.status_code != 200:
            raise Exception(f"Failed to start export: {response.text}")

        progress_id = response.json()['result']['progressId']

        # Poll for completion
        start_time = time.time()
        while True:
            if time.time() - start_time > max_wait:
                raise Exception(f"Export timed out after {max_wait} seconds")

            progress_response = requests.get(
                f'{self.base_url}/surveys/{survey_id}/export-responses/{progress_id}',
                headers=self.headers
            )

            if progress_response.status_code != 200:
                raise Exception(f"Failed to check export progress: {progress_response.text}")

            progress_result = progress_response.json()['result']
            status = progress_result.get('status')

            if status == 'complete':
                file_id = progress_result.get('fileId')
                break
            elif status == 'failed':
                raise Exception("Export failed")

            time.sleep(poll_interval)

        # Download the file
        download_response = requests.get(
            f'{self.base_url}/surveys/{survey_id}/export-responses/{file_id}/file',
            headers=self.headers
        )

        if download_response.status_code == 200:
            return download_response.content
        else:
            raise Exception(f"Failed to download export: {download_response.text}")

    def export_responses_to_file(
        self,
        survey_id: str,
        file_path: str,
        format: str = "csv",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        extract: bool = True,
        include_labels: bool = True,
        poll_interval: float = 1.0,
        max_wait: float = 300.0
    ) -> str:
        """
        Export survey responses and save to a file

        Args:
            survey_id: The survey ID
            file_path: Path to save the exported file
            format: Export format - "csv", "json", "spss", or "xml" (default: "csv")
            start_date: Export responses after this date (ISO 8601 format)
            end_date: Export responses before this date (ISO 8601 format)
            extract: If True, extract the file from the zip archive (default: True)
            include_labels: Include question labels in export (default: True)
            poll_interval: Seconds between progress checks (default: 1.0)
            max_wait: Maximum seconds to wait for export (default: 300.0)

        Returns:
            Path to the saved file
        """
        data = self.export_responses(
            survey_id=survey_id,
            format=format,
            start_date=start_date,
            end_date=end_date,
            compress=True,
            include_labels=include_labels,
            poll_interval=poll_interval,
            max_wait=max_wait
        )

        if extract:
            # Extract from zip
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                # Get the first file in the archive
                file_names = zf.namelist()
                if file_names:
                    with zf.open(file_names[0]) as source:
                        with open(file_path, 'wb') as target:
                            target.write(source.read())
        else:
            # Save as zip
            with open(file_path, 'wb') as f:
                f.write(data)

        return file_path

    def delete_response(self, survey_id: str, response_id: str) -> bool:
        """
        Delete a single response

        Args:
            survey_id: The survey ID
            response_id: The response ID to delete

        Returns:
            True if successful
        """
        response = requests.delete(
            f'{self.base_url}/surveys/{survey_id}/responses/{response_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to delete response: {response.text}")

    def delete_responses(
        self,
        survey_id: str,
        response_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Delete multiple responses

        Args:
            survey_id: The survey ID
            response_ids: List of response IDs to delete

        Returns:
            Dictionary with 'deleted' count and any 'errors'
        """
        deleted = 0
        errors = []

        for response_id in response_ids:
            try:
                self.delete_response(survey_id, response_id)
                deleted += 1
            except Exception as e:
                errors.append({'response_id': response_id, 'error': str(e)})

        return {
            'deleted': deleted,
            'errors': errors
        }

    def get_response_statistics(self, survey_id: str) -> Dict[str, Any]:
        """
        Get summary statistics for survey responses

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with response statistics including:
            - total: Total number of responses
            - complete: Number of complete responses
            - incomplete: Number of incomplete responses
            - completion_rate: Percentage of complete responses
        """
        response = requests.get(
            f'{self.base_url}/surveys/{survey_id}',
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Failed to get response statistics: {response.text}")

        result = response.json()['result']
        response_counts = result.get('responseCounts', {})

        auditable = response_counts.get('auditable', 0)
        generated = response_counts.get('generated', 0)
        deleted = response_counts.get('deleted', 0)

        # Calculate statistics
        total = auditable
        complete = auditable - generated  # Generated responses are incomplete/test
        incomplete = generated

        completion_rate = (complete / total * 100) if total > 0 else 0.0

        return {
            'total': total,
            'complete': complete,
            'incomplete': incomplete,
            'deleted': deleted,
            'completion_rate': round(completion_rate, 2)
        }

    def get_response_schema(self, survey_id: str) -> Dict[str, Any]:
        """
        Get the schema/structure of response data for a survey

        This is useful for understanding what fields will be present
        in exported response data.

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with response schema information
        """
        response = requests.get(
            f'{self.base_url}/surveys/{survey_id}/response-schema',
            headers=self.headers
        )

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get response schema: {response.text}")
