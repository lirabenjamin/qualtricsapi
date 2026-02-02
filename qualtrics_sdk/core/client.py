"""
Main Qualtrics API Client
Combines all functionality through mixins for clean organization
"""

from .base import APIBase
from .surveys import SurveyMixin
from .questions import QuestionMixin
from .question_management import QuestionManagementMixin
from .blocks import BlockMixin


class QualtricsAPI(
    APIBase,
    SurveyMixin,
    QuestionMixin,
    QuestionManagementMixin,
    BlockMixin
):
    """
    Main Qualtrics API client.

    Combines all functionality from mixins:
    - APIBase: Core API communication and authentication
    - SurveyMixin: Survey CRUD operations (create, read, update, delete, list)
    - QuestionMixin: Question creation for all question types
    - QuestionManagementMixin: Question updates and deletions
    - BlockMixin: Block operations

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
        >>> # Get survey URL
        >>> url = api.get_survey_url(survey_id)
    """
    pass  # All methods inherited from mixins!
