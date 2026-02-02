"""
Base API Client
Core functionality for making requests to the Qualtrics API
"""

import requests
from typing import Dict, Any, Optional


class APIBase:
    """
    Base class for Qualtrics API communication.

    Handles initialization, authentication, and provides common attributes
    that all mixins can access.
    """

    def __init__(self, api_token: str, data_center: str):
        """
        Initialize the Qualtrics API client.

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
