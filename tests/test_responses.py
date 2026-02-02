"""
Tests for Response Management (ResponseMixin)
Run with: python -m pytest tests/test_responses.py -v
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import io
import zipfile
import json

# Import the module under test
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from qualtrics_sdk import QualtricsAPI


class TestResponseMixin(unittest.TestCase):
    """Test cases for ResponseMixin methods"""

    def setUp(self):
        """Set up test fixtures"""
        self.api = QualtricsAPI(
            api_token="test_token",
            data_center="test.qualtrics.com"
        )
        self.survey_id = "SV_TEST123"
        self.response_id = "R_TEST456"

    @patch('requests.get')
    def test_get_response_count(self, mock_get):
        """Test get_response_count returns correct count"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'responseCounts': {
                    'auditable': 150,
                    'generated': 10,
                    'deleted': 5
                }
            }
        }

        count = self.api.get_response_count(self.survey_id)

        self.assertEqual(count, 150)
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_response_count_empty(self, mock_get):
        """Test get_response_count handles empty response counts"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {}
        }

        count = self.api.get_response_count(self.survey_id)

        self.assertEqual(count, 0)

    @patch('requests.get')
    def test_get_response_count_error(self, mock_get):
        """Test get_response_count raises exception on error"""
        mock_get.return_value.status_code = 404
        mock_get.return_value.text = "Survey not found"

        with self.assertRaises(Exception) as context:
            self.api.get_response_count(self.survey_id)

        self.assertIn("Failed to get response count", str(context.exception))

    @patch('requests.get')
    def test_list_responses(self, mock_get):
        """Test list_responses returns responses with pagination"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'elements': [
                    {'responseId': 'R_1', 'status': 'Complete'},
                    {'responseId': 'R_2', 'status': 'Complete'}
                ],
                'nextPage': 'https://api.qualtrics.com/next'
            }
        }

        result = self.api.list_responses(self.survey_id, limit=10)

        self.assertEqual(len(result['responses']), 2)
        self.assertEqual(result['responses'][0]['responseId'], 'R_1')
        self.assertIsNotNone(result['nextPage'])

    @patch('requests.get')
    def test_list_responses_with_filters(self, mock_get):
        """Test list_responses with date and status filters"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'elements': [{'responseId': 'R_1'}],
                'nextPage': None
            }
        }

        result = self.api.list_responses(
            self.survey_id,
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z",
            status="Complete",
            limit=50,
            offset=10
        )

        # Verify the params were passed correctly
        call_args = mock_get.call_args
        params = call_args.kwargs.get('params', {})
        self.assertEqual(params['startDate'], "2024-01-01T00:00:00Z")
        self.assertEqual(params['endDate'], "2024-12-31T23:59:59Z")
        self.assertEqual(params['status'], "Complete")
        self.assertEqual(params['limit'], 50)
        self.assertEqual(params['offset'], 10)

    @patch('requests.get')
    def test_get_response(self, mock_get):
        """Test get_response returns single response"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'responseId': self.response_id,
                'status': 'Complete',
                'values': {'Q1': 'Answer 1'}
            }
        }

        response = self.api.get_response(self.survey_id, self.response_id)

        self.assertEqual(response['responseId'], self.response_id)
        self.assertEqual(response['status'], 'Complete')

    @patch('requests.delete')
    def test_delete_response(self, mock_delete):
        """Test delete_response returns True on success"""
        mock_delete.return_value.status_code = 200

        result = self.api.delete_response(self.survey_id, self.response_id)

        self.assertTrue(result)
        mock_delete.assert_called_once()

    @patch('requests.delete')
    def test_delete_response_error(self, mock_delete):
        """Test delete_response raises exception on error"""
        mock_delete.return_value.status_code = 404
        mock_delete.return_value.text = "Response not found"

        with self.assertRaises(Exception) as context:
            self.api.delete_response(self.survey_id, self.response_id)

        self.assertIn("Failed to delete response", str(context.exception))

    def test_delete_responses_bulk(self):
        """Test delete_responses deletes multiple responses"""
        response_ids = ['R_1', 'R_2', 'R_3']

        with patch.object(self.api, 'delete_response') as mock_delete:
            mock_delete.return_value = True

            result = self.api.delete_responses(self.survey_id, response_ids)

            self.assertEqual(result['deleted'], 3)
            self.assertEqual(len(result['errors']), 0)
            self.assertEqual(mock_delete.call_count, 3)

    def test_delete_responses_partial_failure(self):
        """Test delete_responses handles partial failures"""
        response_ids = ['R_1', 'R_2', 'R_3']

        with patch.object(self.api, 'delete_response') as mock_delete:
            mock_delete.side_effect = [
                True,
                Exception("Not found"),
                True
            ]

            result = self.api.delete_responses(self.survey_id, response_ids)

            self.assertEqual(result['deleted'], 2)
            self.assertEqual(len(result['errors']), 1)
            self.assertEqual(result['errors'][0]['response_id'], 'R_2')

    @patch('requests.get')
    def test_get_response_statistics(self, mock_get):
        """Test get_response_statistics returns calculated stats"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'responseCounts': {
                    'auditable': 100,
                    'generated': 20,
                    'deleted': 5
                }
            }
        }

        stats = self.api.get_response_statistics(self.survey_id)

        self.assertEqual(stats['total'], 100)
        self.assertEqual(stats['complete'], 80)  # 100 - 20
        self.assertEqual(stats['incomplete'], 20)
        self.assertEqual(stats['deleted'], 5)
        self.assertEqual(stats['completion_rate'], 80.0)

    @patch('requests.get')
    def test_get_response_statistics_zero_responses(self, mock_get):
        """Test get_response_statistics handles zero responses"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'responseCounts': {
                    'auditable': 0,
                    'generated': 0,
                    'deleted': 0
                }
            }
        }

        stats = self.api.get_response_statistics(self.survey_id)

        self.assertEqual(stats['total'], 0)
        self.assertEqual(stats['completion_rate'], 0.0)

    @patch('requests.get')
    def test_get_response_schema(self, mock_get):
        """Test get_response_schema returns schema"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {
                'Q1': {'type': 'string'},
                'Q2': {'type': 'number'}
            }
        }

        schema = self.api.get_response_schema(self.survey_id)

        self.assertIn('Q1', schema)
        self.assertIn('Q2', schema)

    def test_export_responses_invalid_format(self):
        """Test export_responses raises error for invalid format"""
        with self.assertRaises(ValueError) as context:
            self.api.export_responses(self.survey_id, format="invalid")

        self.assertIn("Invalid format", str(context.exception))

    @patch('requests.get')
    @patch('requests.post')
    def test_export_responses_success(self, mock_post, mock_get):
        """Test export_responses completes async export"""
        # Mock the POST to start export
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'result': {'progressId': 'progress_123'}
        }

        # Create a mock zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('responses.csv', 'id,Q1\n1,answer')
        zip_content = zip_buffer.getvalue()

        # Mock the GET requests for progress and download
        progress_response = Mock()
        progress_response.status_code = 200
        progress_response.json.return_value = {
            'result': {'status': 'complete', 'fileId': 'file_123'}
        }

        download_response = Mock()
        download_response.status_code = 200
        download_response.content = zip_content

        mock_get.side_effect = [progress_response, download_response]

        result = self.api.export_responses(
            self.survey_id,
            format="csv",
            poll_interval=0.01
        )

        self.assertEqual(result, zip_content)
        mock_post.assert_called_once()

    @patch('requests.get')
    @patch('requests.post')
    def test_export_responses_timeout(self, mock_post, mock_get):
        """Test export_responses raises exception on timeout"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'result': {'progressId': 'progress_123'}
        }

        # Always return 'inProgress' status
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {'status': 'inProgress'}
        }

        with self.assertRaises(Exception) as context:
            self.api.export_responses(
                self.survey_id,
                format="csv",
                poll_interval=0.01,
                max_wait=0.05
            )

        self.assertIn("timed out", str(context.exception))

    @patch('requests.get')
    @patch('requests.post')
    def test_export_responses_failed(self, mock_post, mock_get):
        """Test export_responses raises exception on export failure"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'result': {'progressId': 'progress_123'}
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'result': {'status': 'failed'}
        }

        with self.assertRaises(Exception) as context:
            self.api.export_responses(
                self.survey_id,
                format="csv",
                poll_interval=0.01
            )

        self.assertIn("Export failed", str(context.exception))


class TestExportFormats(unittest.TestCase):
    """Test export format handling"""

    def setUp(self):
        self.api = QualtricsAPI(
            api_token="test_token",
            data_center="test.qualtrics.com"
        )
        self.survey_id = "SV_TEST123"

    def test_valid_formats(self):
        """Test that all valid formats are accepted"""
        valid_formats = ['csv', 'json', 'spss', 'xml', 'CSV', 'JSON', 'SPSS', 'XML']

        for format in valid_formats:
            with patch('requests.post') as mock_post:
                mock_post.return_value.status_code = 200
                mock_post.return_value.json.return_value = {
                    'result': {'progressId': 'test'}
                }

                with patch('requests.get') as mock_get:
                    mock_get.return_value.status_code = 200
                    mock_get.return_value.json.return_value = {
                        'result': {'status': 'complete', 'fileId': 'file_123'}
                    }
                    mock_get.return_value.content = b'data'

                    # Should not raise ValueError
                    try:
                        self.api.export_responses(
                            self.survey_id,
                            format=format,
                            poll_interval=0.01,
                            max_wait=0.1
                        )
                    except Exception as e:
                        if "Invalid format" in str(e):
                            self.fail(f"Format {format} should be valid")


class TestResponseMixinIntegration(unittest.TestCase):
    """Integration tests for ResponseMixin"""

    def test_mixin_available_in_api(self):
        """Test that ResponseMixin methods are available on QualtricsAPI"""
        api = QualtricsAPI(
            api_token="test_token",
            data_center="test.qualtrics.com"
        )

        # Check all response methods exist
        self.assertTrue(hasattr(api, 'get_response_count'))
        self.assertTrue(hasattr(api, 'list_responses'))
        self.assertTrue(hasattr(api, 'get_response'))
        self.assertTrue(hasattr(api, 'export_responses'))
        self.assertTrue(hasattr(api, 'export_responses_to_file'))
        self.assertTrue(hasattr(api, 'delete_response'))
        self.assertTrue(hasattr(api, 'delete_responses'))
        self.assertTrue(hasattr(api, 'get_response_statistics'))
        self.assertTrue(hasattr(api, 'get_response_schema'))

    def test_api_initialization(self):
        """Test QualtricsAPI initializes correctly with ResponseMixin"""
        api = QualtricsAPI(
            api_token="test_token",
            data_center="test.qualtrics.com"
        )

        self.assertEqual(api.api_token, "test_token")
        self.assertEqual(api.data_center, "test.qualtrics.com")
        self.assertEqual(api.base_url, "https://test.qualtrics.com/API/v3")


if __name__ == '__main__':
    unittest.main()
