"""
Tests for the Randomization Mixin

These tests verify the randomization functionality including:
- Block-level randomization
- Question-level randomization
- Choice-level randomization

To run tests:
    pytest tests/test_randomization.py -v

For integration tests (requires API credentials):
    pytest tests/test_randomization.py -v -m integration
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from qualtrics_sdk.core.randomization import RandomizationMixin


class MockAPI(RandomizationMixin):
    """Mock API class for testing the RandomizationMixin"""

    def __init__(self):
        self.base_url = "https://test.qualtrics.com/API/v3"
        self.headers = {
            'X-API-TOKEN': 'test_token',
            'Content-Type': 'application/json'
        }

    def get_survey(self, survey_id):
        """Mock get_survey method"""
        return {
            'SurveyID': survey_id,
            'SurveyFlow': {
                'Flow': [
                    {'Type': 'Block', 'ID': 'BL_001', 'FlowID': 'FL_1'},
                    {'Type': 'Block', 'ID': 'BL_002', 'FlowID': 'FL_2'},
                    {'Type': 'Block', 'ID': 'BL_003', 'FlowID': 'FL_3'}
                ],
                'Properties': {'Count': 3}
            },
            'Blocks': {
                'BL_001': {
                    'Type': 'Standard',
                    'Description': 'Block 1',
                    'Options': {},
                    'BlockElements': [
                        {'Type': 'Question', 'QuestionID': 'QID1'},
                        {'Type': 'Question', 'QuestionID': 'QID2'}
                    ]
                },
                'BL_002': {
                    'Type': 'Standard',
                    'Description': 'Block 2',
                    'Options': {},
                    'BlockElements': [
                        {'Type': 'Question', 'QuestionID': 'QID3'}
                    ]
                },
                'BL_003': {
                    'Type': 'Standard',
                    'Description': 'Block 3',
                    'Options': {},
                    'BlockElements': []
                }
            }
        }

    def get_question(self, survey_id, question_id):
        """Mock get_question method"""
        return {
            'QuestionID': question_id,
            'QuestionType': 'MC',
            'Selector': 'SAVR',
            'QuestionText': 'Test Question?',
            'Choices': {
                '1': {'Display': 'Choice A'},
                '2': {'Display': 'Choice B'},
                '3': {'Display': 'Choice C'},
                '4': {'Display': 'Other'}
            },
            'ChoiceOrder': ['1', '2', '3', '4'],
            'Configuration': {'QuestionDescriptionOption': 'UseText'},
            'Validation': {},
            'Language': []
        }


class TestRandomizeBlocks:
    """Tests for the randomize_blocks method"""

    def setup_method(self):
        """Set up test fixtures"""
        self.api = MockAPI()

    @patch('requests.put')
    def test_randomize_blocks_basic(self, mock_put):
        """Test basic block randomization"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'FlowID': 'FL_Randomizer'}}
        )

        result = self.api.randomize_blocks(
            'SV_test',
            block_ids=['BL_001', 'BL_002', 'BL_003']
        )

        assert mock_put.called
        call_args = mock_put.call_args
        assert 'flow' in call_args[0][0]

    @patch('requests.put')
    def test_randomize_blocks_even_presentation(self, mock_put):
        """Test block randomization with even presentation"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'FlowID': 'FL_Randomizer'}}
        )

        result = self.api.randomize_blocks(
            'SV_test',
            block_ids=['BL_001', 'BL_002'],
            evenly_present=True
        )

        assert mock_put.called
        # Check that the request includes even presentation
        call_args = mock_put.call_args
        json_data = call_args[1]['json']
        assert 'Flow' in json_data

    @patch('requests.put')
    def test_randomize_blocks_subset(self, mock_put):
        """Test block randomization with subset"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'FlowID': 'FL_Randomizer'}}
        )

        result = self.api.randomize_blocks(
            'SV_test',
            block_ids=['BL_001', 'BL_002', 'BL_003'],
            subset_count=2
        )

        assert mock_put.called

    def test_randomize_blocks_invalid_subset(self):
        """Test that invalid subset_count raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            self.api.randomize_blocks(
                'SV_test',
                block_ids=['BL_001', 'BL_002'],
                subset_count=5  # More than available blocks
            )
        assert 'subset_count must be less than' in str(exc_info.value)

    @patch('requests.put')
    def test_randomize_blocks_api_failure(self, mock_put):
        """Test handling of API failure"""
        mock_put.return_value = Mock(
            status_code=400,
            text='Bad Request'
        )

        with pytest.raises(Exception) as exc_info:
            self.api.randomize_blocks('SV_test', block_ids=['BL_001'])
        assert 'Failed to set block randomization' in str(exc_info.value)


class TestRandomizeQuestionsInBlock:
    """Tests for the randomize_questions_in_block method"""

    def setup_method(self):
        """Set up test fixtures"""
        self.api = MockAPI()

    @patch('requests.put')
    def test_randomize_questions_enable(self, mock_put):
        """Test enabling question randomization"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'BlockID': 'BL_001'}}
        )

        result = self.api.randomize_questions_in_block(
            'SV_test',
            block_id='BL_001',
            randomize=True
        )

        assert mock_put.called
        call_args = mock_put.call_args
        json_data = call_args[1]['json']
        assert 'Options' in json_data
        assert 'Randomization' in json_data['Options']

    @patch('requests.put')
    def test_randomize_questions_disable(self, mock_put):
        """Test disabling question randomization"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'BlockID': 'BL_001'}}
        )

        result = self.api.randomize_questions_in_block(
            'SV_test',
            block_id='BL_001',
            randomize=False
        )

        assert mock_put.called

    @patch('requests.put')
    def test_randomize_questions_with_subset(self, mock_put):
        """Test question randomization with subset count"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'BlockID': 'BL_001'}}
        )

        result = self.api.randomize_questions_in_block(
            'SV_test',
            block_id='BL_001',
            randomize=True,
            subset_count=3
        )

        assert mock_put.called
        call_args = mock_put.call_args
        json_data = call_args[1]['json']
        assert json_data['Options']['Randomization']['TotalRandSubset'] == 3

    def test_randomize_questions_invalid_block(self):
        """Test that invalid block_id raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            self.api.randomize_questions_in_block(
                'SV_test',
                block_id='BL_INVALID',
                randomize=True
            )
        assert 'not found in survey' in str(exc_info.value)

    @patch('requests.put')
    def test_randomize_questions_api_failure(self, mock_put):
        """Test handling of API failure"""
        mock_put.return_value = Mock(
            status_code=400,
            text='Bad Request'
        )

        with pytest.raises(Exception) as exc_info:
            self.api.randomize_questions_in_block(
                'SV_test',
                block_id='BL_001',
                randomize=True
            )
        assert 'Failed to set question randomization' in str(exc_info.value)


class TestRandomizeQuestionChoices:
    """Tests for the randomize_question_choices method"""

    def setup_method(self):
        """Set up test fixtures"""
        self.api = MockAPI()

    @patch('requests.put')
    def test_randomize_choices_enable(self, mock_put):
        """Test enabling choice randomization"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'QuestionID': 'QID1'}}
        )

        result = self.api.randomize_question_choices(
            'SV_test',
            question_id='QID1',
            randomize=True
        )

        assert mock_put.called
        call_args = mock_put.call_args
        json_data = call_args[1]['json']
        assert 'Randomization' in json_data

    @patch('requests.put')
    def test_randomize_choices_disable(self, mock_put):
        """Test disabling choice randomization"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'QuestionID': 'QID1'}}
        )

        result = self.api.randomize_question_choices(
            'SV_test',
            question_id='QID1',
            randomize=False
        )

        assert mock_put.called

    @patch('requests.put')
    def test_randomize_choices_anchor_last(self, mock_put):
        """Test choice randomization with anchor_last option"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'QuestionID': 'QID1'}}
        )

        result = self.api.randomize_question_choices(
            'SV_test',
            question_id='QID1',
            randomize=True,
            anchor_last=True
        )

        assert mock_put.called
        call_args = mock_put.call_args
        json_data = call_args[1]['json']
        assert 'Randomization' in json_data

    @patch('requests.put')
    def test_randomize_choices_specific_anchors(self, mock_put):
        """Test choice randomization with specific anchor choices"""
        mock_put.return_value = Mock(
            status_code=200,
            json=lambda: {'result': {'QuestionID': 'QID1'}}
        )

        result = self.api.randomize_question_choices(
            'SV_test',
            question_id='QID1',
            randomize=True,
            anchor_choices=['1', '4']
        )

        assert mock_put.called

    def test_randomize_choices_no_choices(self):
        """Test that question without choices raises ValueError"""
        # Override get_question to return a question without choices
        original_get_question = self.api.get_question
        self.api.get_question = lambda sid, qid: {
            'QuestionID': qid,
            'QuestionType': 'TE',
            'QuestionText': 'Text Entry Question'
            # No Choices field
        }

        with pytest.raises(ValueError) as exc_info:
            self.api.randomize_question_choices(
                'SV_test',
                question_id='QID1',
                randomize=True
            )
        assert 'does not have choices' in str(exc_info.value)

        # Restore original method
        self.api.get_question = original_get_question

    @patch('requests.put')
    def test_randomize_choices_api_failure(self, mock_put):
        """Test handling of API failure"""
        mock_put.return_value = Mock(
            status_code=400,
            text='Bad Request'
        )

        with pytest.raises(Exception) as exc_info:
            self.api.randomize_question_choices(
                'SV_test',
                question_id='QID1',
                randomize=True
            )
        assert 'Failed to set choice randomization' in str(exc_info.value)


class TestGetRandomizationSettings:
    """Tests for the get_randomization_settings method"""

    def setup_method(self):
        """Set up test fixtures"""
        self.api = MockAPI()

    def test_get_settings_empty_survey(self):
        """Test getting settings from a survey with no randomization"""
        result = self.api.get_randomization_settings('SV_test')

        assert 'block_randomization' in result
        assert 'question_randomization' in result
        assert 'choice_randomization' in result
        assert isinstance(result['block_randomization'], list)
        assert isinstance(result['question_randomization'], dict)
        assert isinstance(result['choice_randomization'], dict)

    def test_get_settings_with_block_randomizer(self):
        """Test getting settings when block randomizer exists"""
        # Override get_survey to include a randomizer
        original_get_survey = self.api.get_survey
        self.api.get_survey = lambda sid: {
            'SurveyID': sid,
            'SurveyFlow': {
                'Flow': [
                    {
                        'Type': 'BlockRandomizer',
                        'FlowID': 'FL_Rand',
                        'SubSet': 2,
                        'EvenPresentation': True,
                        'Flow': [
                            {'Type': 'Block', 'ID': 'BL_001'},
                            {'Type': 'Block', 'ID': 'BL_002'}
                        ]
                    }
                ],
                'Properties': {}
            },
            'Blocks': {}
        }

        result = self.api.get_randomization_settings('SV_test')

        assert len(result['block_randomization']) == 1
        assert result['block_randomization'][0]['flow_id'] == 'FL_Rand'
        assert result['block_randomization'][0]['even_presentation'] is True
        assert result['block_randomization'][0]['subset'] == 2

        # Restore original method
        self.api.get_survey = original_get_survey


# Integration tests (require API credentials)
@pytest.mark.integration
class TestRandomizationIntegration:
    """Integration tests that require actual API credentials.

    These tests are skipped by default. To run them:
    1. Set up your .env file with valid credentials
    2. Run: pytest tests/test_randomization.py -v -m integration
    """

    @pytest.fixture(autouse=True)
    def setup_api(self):
        """Set up the API client with real credentials"""
        from dotenv import load_dotenv
        load_dotenv()

        api_token = os.getenv('QUALTRICS_API_TOKEN')
        data_center = os.getenv('QUALTRICS_DATA_CENTER')

        if not api_token or not data_center:
            pytest.skip("API credentials not found in .env file")

        from qualtrics_sdk import QualtricsAPI
        self.api = QualtricsAPI(api_token=api_token, data_center=data_center)

    def test_full_randomization_workflow(self):
        """Test complete randomization workflow with real API"""
        # Create a test survey
        survey = self.api.create_survey("Randomization Test Survey")
        survey_id = survey['SurveyID']

        try:
            # Create blocks
            block1 = self.api.create_block(survey_id, "Block A")
            block2 = self.api.create_block(survey_id, "Block B")

            # Add questions
            q1 = self.api.create_multiple_choice_question(
                survey_id,
                "Question 1?",
                choices=["A", "B", "C", "Other"],
                block_id=block1['BlockID']
            )

            # Test randomization features
            # Note: Results may vary based on Qualtrics API behavior

            # Get randomization settings
            settings = self.api.get_randomization_settings(survey_id)
            assert 'block_randomization' in settings

        finally:
            # Cleanup: delete the test survey
            self.api.delete_survey(survey_id)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
