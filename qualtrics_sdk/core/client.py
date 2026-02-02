"""
Main Qualtrics API Client
Combines all functionality through mixins for clean organization
"""

from .base import APIBase
from .surveys import SurveyMixin
from .questions import QuestionMixin
from .question_management import QuestionManagementMixin
from .blocks import BlockMixin
from .display_logic import DisplayLogicMixin
from .embedded_data import EmbeddedDataMixin


class QualtricsAPI(
    APIBase,
    SurveyMixin,
    QuestionMixin,
    QuestionManagementMixin,
    BlockMixin,
    DisplayLogicMixin,
    EmbeddedDataMixin
):
    """
    Main Qualtrics API client.

    Combines all functionality from mixins:
    - APIBase: Core API communication and authentication
    - SurveyMixin: Survey CRUD operations (create, read, update, delete, list)
    - QuestionMixin: Question creation for all question types
    - QuestionManagementMixin: Question updates and deletions
    - BlockMixin: Block operations
    - DisplayLogicMixin: Display logic and conditional display
    - EmbeddedDataMixin: Embedded data field configuration and URL generation

    Usage:
        >>> from qualtrics_sdk import QualtricsAPI
        >>> api = QualtricsAPI(token="xxx", data_center="yyy.qualtrics.com")
        >>>
        >>> # Create survey
        >>> survey = api.create_survey("My Survey")
        >>> survey_id = survey['SurveyID']
        >>>
        >>> # Add questions
        >>> api.create_multiple_choice_question(
        ...     survey_id,
        ...     "What is your role?",
        ...     ["Student", "Faculty", "Staff"]
        ... )
        >>>
        >>> # Set embedded data fields
        >>> api.set_embedded_data_fields(survey_id, {
        ...     "user_id": {"type": "text"},
        ...     "source": {"type": "text", "value": "web"}
        ... })
        >>>
        >>> # Get survey URL with embedded data
        >>> url = api.get_survey_url_with_embedded_data(
        ...     survey_id,
        ...     {"user_id": "12345", "source": "email"}
        ... )
    """
    pass  # All methods inherited from mixins!
