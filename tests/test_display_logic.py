"""
Unit tests for DisplayLogicMixin

Run tests with:
    pytest tests/test_display_logic.py -v

Run with coverage:
    pytest tests/test_display_logic.py -v --cov=qualtrics_sdk.core.display_logic
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import json

# Import the mixin class
from qualtrics_sdk.core.display_logic import DisplayLogicMixin


class TestDisplayLogicMixin:
    """Test cases for DisplayLogicMixin"""

    @pytest.fixture
    def mixin(self):
        """Create a DisplayLogicMixin instance with mocked base attributes"""
        class TestClient(DisplayLogicMixin):
            def __init__(self):
                self.base_url = "https://test.qualtrics.com/API/v3"
                self.headers = {
                    'X-API-TOKEN': 'test_token',
                    'Content-Type': 'application/json'
                }

            def get_question(self, survey_id, question_id):
                """Mock get_question method"""
                return {'QuestionID': question_id, 'DisplayLogic': None}

        return TestClient()

    # =========================================================================
    # Tests for _build_condition
    # =========================================================================

    def test_build_condition_basic(self, mixin):
        """Test building a basic condition"""
        condition = mixin._build_condition(
            question_id="QID1",
            operator="Selected",
            choice_locator="q://QID1/SelectableChoice/1"
        )

        assert condition['Type'] == 'Expression'
        assert condition['LogicType'] == 'Question'
        assert condition['QuestionID'] == 'QID1'
        assert condition['Operator'] == 'Selected'
        assert condition['ChoiceLocator'] == 'q://QID1/SelectableChoice/1'

    def test_build_condition_with_value(self, mixin):
        """Test building a condition with comparison value"""
        condition = mixin._build_condition(
            question_id="QID2",
            operator="GreaterThan",
            value=50
        )

        assert condition['Type'] == 'Expression'
        assert condition['Operator'] == 'GreaterThan'
        assert condition['RightOperand'] == '50'

    def test_build_condition_embedded_field(self, mixin):
        """Test building a condition for embedded data"""
        condition = mixin._build_condition(
            question_id="user_type",
            operator="EqualTo",
            value="premium",
            logic_type="EmbeddedField"
        )

        assert condition['LogicType'] == 'EmbeddedField'
        assert condition['LeftOperand'] == 'ed://user_type'
        assert condition['Operator'] == 'EqualTo'
        assert condition['RightOperand'] == 'premium'

    # =========================================================================
    # Tests for add_display_logic
    # =========================================================================

    @patch('requests.put')
    def test_add_display_logic_success(self, mock_put, mixin):
        """Test successful display logic addition"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.add_display_logic(
            survey_id="SV_test123",
            question_id="QID2",
            source_question_id="QID1",
            operator="Selected",
            choice_locator="q://QID1/SelectableChoice/1"
        )

        assert result is True
        mock_put.assert_called_once()

        # Verify the API call
        call_args = mock_put.call_args
        assert 'SV_test123' in call_args[0][0]
        assert 'QID2' in call_args[0][0]

    @patch('requests.put')
    def test_add_display_logic_failure(self, mock_put, mixin):
        """Test display logic addition failure"""
        mock_put.return_value = Mock(status_code=400, text='Error message')

        with pytest.raises(Exception) as exc_info:
            mixin.add_display_logic(
                survey_id="SV_test123",
                question_id="QID2",
                source_question_id="QID1",
                operator="Selected",
                choice_locator="q://QID1/SelectableChoice/1"
            )

        assert "Failed to add display logic" in str(exc_info.value)

    def test_add_display_logic_invalid_operator(self, mixin):
        """Test display logic with invalid operator raises error"""
        with pytest.raises(ValueError) as exc_info:
            mixin.add_display_logic(
                survey_id="SV_test123",
                question_id="QID2",
                source_question_id="QID1",
                operator="InvalidOperator"
            )

        assert "Invalid operator" in str(exc_info.value)

    # =========================================================================
    # Tests for add_display_logic_multiple
    # =========================================================================

    @patch('requests.put')
    def test_add_display_logic_multiple_and(self, mock_put, mixin):
        """Test multiple conditions with AND conjunction"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.add_display_logic_multiple(
            survey_id="SV_test123",
            question_id="QID3",
            conditions=[
                {
                    "source_question_id": "QID1",
                    "operator": "Selected",
                    "choice_locator": "q://QID1/SelectableChoice/1"
                },
                {
                    "source_question_id": "QID2",
                    "operator": "GreaterThan",
                    "value": 5
                }
            ],
            conjunction="AND"
        )

        assert result is True
        mock_put.assert_called_once()

        # Verify the payload contains both conditions
        call_args = mock_put.call_args
        payload = call_args[1]['json']
        assert 'DisplayLogic' in payload

    @patch('requests.put')
    def test_add_display_logic_multiple_or(self, mock_put, mixin):
        """Test multiple conditions with OR conjunction"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.add_display_logic_multiple(
            survey_id="SV_test123",
            question_id="QID3",
            conditions=[
                {
                    "source_question_id": "QID1",
                    "operator": "Selected",
                    "choice_locator": "q://QID1/SelectableChoice/1"
                },
                {
                    "source_question_id": "QID1",
                    "operator": "Selected",
                    "choice_locator": "q://QID1/SelectableChoice/2"
                }
            ],
            conjunction="OR"
        )

        assert result is True

    def test_add_display_logic_multiple_invalid_conjunction(self, mixin):
        """Test invalid conjunction raises error"""
        with pytest.raises(ValueError) as exc_info:
            mixin.add_display_logic_multiple(
                survey_id="SV_test123",
                question_id="QID3",
                conditions=[{"source_question_id": "QID1", "operator": "Selected"}],
                conjunction="INVALID"
            )

        assert "conjunction must be 'AND' or 'OR'" in str(exc_info.value)

    def test_add_display_logic_multiple_empty_conditions(self, mixin):
        """Test empty conditions list raises error"""
        with pytest.raises(ValueError) as exc_info:
            mixin.add_display_logic_multiple(
                survey_id="SV_test123",
                question_id="QID3",
                conditions=[],
                conjunction="AND"
            )

        assert "At least one condition is required" in str(exc_info.value)

    def test_add_display_logic_multiple_invalid_operator_in_conditions(self, mixin):
        """Test invalid operator in conditions raises error"""
        with pytest.raises(ValueError) as exc_info:
            mixin.add_display_logic_multiple(
                survey_id="SV_test123",
                question_id="QID3",
                conditions=[
                    {"source_question_id": "QID1", "operator": "InvalidOp"}
                ],
                conjunction="AND"
            )

        assert "Invalid operator" in str(exc_info.value)

    # =========================================================================
    # Tests for show_only_if
    # =========================================================================

    @patch('requests.put')
    def test_show_only_if(self, mock_put, mixin):
        """Test show_only_if helper method"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.show_only_if(
            survey_id="SV_test123",
            question_id="QID2",
            source_question_id="QID1",
            operator="Selected",
            choice_locator="q://QID1/SelectableChoice/1"
        )

        assert result is True
        mock_put.assert_called_once()

    # =========================================================================
    # Tests for skip_if
    # =========================================================================

    @patch('requests.put')
    def test_skip_if_inverts_selected(self, mock_put, mixin):
        """Test skip_if inverts Selected to NotSelected"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.skip_if(
            survey_id="SV_test123",
            question_id="QID2",
            source_question_id="QID1",
            operator="Selected",
            choice_locator="q://QID1/SelectableChoice/2"
        )

        assert result is True

        # Verify the inverted operator was used (NotSelected)
        call_args = mock_put.call_args
        payload = call_args[1]['json']
        # The payload should contain NotSelected (inverted)
        assert 'DisplayLogic' in payload

    # =========================================================================
    # Tests for get_display_logic
    # =========================================================================

    def test_get_display_logic_returns_logic(self, mixin):
        """Test get_display_logic returns display logic"""
        # Mock get_question to return a question with display logic
        mixin.get_question = Mock(return_value={
            'QuestionID': 'QID2',
            'DisplayLogic': {'Type': 'BooleanExpression'}
        })

        result = mixin.get_display_logic("SV_test123", "QID2")

        assert result == {'Type': 'BooleanExpression'}
        mixin.get_question.assert_called_once_with("SV_test123", "QID2")

    def test_get_display_logic_returns_none(self, mixin):
        """Test get_display_logic returns None when no logic set"""
        mixin.get_question = Mock(return_value={
            'QuestionID': 'QID2'
        })

        result = mixin.get_display_logic("SV_test123", "QID2")

        assert result is None

    # =========================================================================
    # Tests for delete_display_logic
    # =========================================================================

    @patch('requests.put')
    def test_delete_display_logic_success(self, mock_put, mixin):
        """Test successful display logic deletion"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.delete_display_logic("SV_test123", "QID2")

        assert result is True
        mock_put.assert_called_once()

        # Verify DisplayLogic is set to None
        call_args = mock_put.call_args
        payload = call_args[1]['json']
        assert payload['DisplayLogic'] is None

    @patch('requests.put')
    def test_delete_display_logic_failure(self, mock_put, mixin):
        """Test display logic deletion failure"""
        mock_put.return_value = Mock(status_code=400, text='Error message')

        with pytest.raises(Exception) as exc_info:
            mixin.delete_display_logic("SV_test123", "QID2")

        assert "Failed to delete display logic" in str(exc_info.value)

    # =========================================================================
    # Tests for add_embedded_data_logic
    # =========================================================================

    @patch('requests.put')
    def test_add_embedded_data_logic_success(self, mock_put, mixin):
        """Test successful embedded data logic addition"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.add_embedded_data_logic(
            survey_id="SV_test123",
            question_id="QID1",
            field_name="user_type",
            operator="EqualTo",
            value="premium"
        )

        assert result is True
        mock_put.assert_called_once()

    def test_add_embedded_data_logic_invalid_operator(self, mixin):
        """Test embedded data logic with invalid operator raises error"""
        with pytest.raises(ValueError) as exc_info:
            mixin.add_embedded_data_logic(
                survey_id="SV_test123",
                question_id="QID1",
                field_name="user_type",
                operator="InvalidOperator",
                value="premium"
            )

        assert "Invalid operator" in str(exc_info.value)


class TestOperators:
    """Test the OPERATORS constant"""

    def test_all_operators_defined(self):
        """Ensure all expected operators are defined"""
        expected_operators = [
            'Selected', 'NotSelected', 'Displayed', 'NotDisplayed',
            'EqualTo', 'NotEqualTo', 'GreaterThan', 'LessThan',
            'GreaterOrEqual', 'LessOrEqual', 'Contains', 'DoesNotContain',
            'MatchesRegex', 'Empty', 'NotEmpty'
        ]

        for op in expected_operators:
            assert op in DisplayLogicMixin.OPERATORS


class TestIntegrationScenarios:
    """Integration-style tests for common use cases"""

    @pytest.fixture
    def mixin(self):
        """Create a DisplayLogicMixin instance"""
        class TestClient(DisplayLogicMixin):
            def __init__(self):
                self.base_url = "https://test.qualtrics.com/API/v3"
                self.headers = {'X-API-TOKEN': 'test', 'Content-Type': 'application/json'}

            def get_question(self, survey_id, question_id):
                return {'QuestionID': question_id}

        return TestClient()

    @patch('requests.put')
    def test_branching_survey_scenario(self, mock_put, mixin):
        """Test a complete branching survey scenario"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        # Scenario: Show follow-up only if user selects "Yes"
        result = mixin.add_display_logic(
            survey_id="SV_branch",
            question_id="QID_followup",
            source_question_id="QID_screening",
            operator="Selected",
            choice_locator="q://QID_screening/SelectableChoice/1"
        )
        assert result is True

    @patch('requests.put')
    def test_satisfaction_followup_scenario(self, mock_put, mixin):
        """Test showing improvement question for low satisfaction"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        # Show improvement question if satisfaction < 50
        result = mixin.show_only_if(
            survey_id="SV_sat",
            question_id="QID_improve",
            source_question_id="QID_rating",
            operator="LessThan",
            value=50
        )
        assert result is True

    @patch('requests.put')
    def test_multi_product_comparison_scenario(self, mock_put, mixin):
        """Test showing comparison only when multiple products selected"""
        mock_put.return_value = Mock(status_code=200, text='{}')

        result = mixin.add_display_logic_multiple(
            survey_id="SV_products",
            question_id="QID_compare",
            conditions=[
                {
                    "source_question_id": "QID_products",
                    "operator": "Selected",
                    "choice_locator": "q://QID_products/SelectableChoice/1"
                },
                {
                    "source_question_id": "QID_products",
                    "operator": "Selected",
                    "choice_locator": "q://QID_products/SelectableChoice/2"
                }
            ],
            conjunction="AND"
        )
        assert result is True
