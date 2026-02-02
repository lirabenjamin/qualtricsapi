"""
Block Operations Mixin
Handles survey block creation and management
"""

import requests
from typing import Dict, Any


class BlockMixin:
    """Mixin providing block operations"""

    def get_blocks(self, survey_id: str) -> Dict[str, Any]:
        """
        Get all blocks in a survey by fetching the full survey definition

        Args:
            survey_id: The survey ID

        Returns:
            Dictionary with block details
        """
        response = requests.get(
            f'{self.base_url}/survey-definitions/{survey_id}',
            headers=self.headers
        )

        if response.status_code == 200:
            result = response.json()['result']
            # Return just the blocks
            return {'Elements': result.get('Blocks', {})}
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
