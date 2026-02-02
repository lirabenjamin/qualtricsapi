"""
Unit tests for Embedded Data functionality

Run with: pytest tests/test_embedded_data.py -v
"""

import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from qualtrics_sdk import QualtricsAPI


@pytest.fixture
def api():
    """Create a QualtricsAPI instance for testing"""
    return QualtricsAPI(api_token="test_token", data_center="test.qualtrics.com")


@pytest.fixture
def mock_flow_response():
    """Mock response for survey flow API"""
    return {
        "result": {
            "Flow": [
                {
                    "Type": "Block",
                    "ID": "BL_1",
                    "FlowID": "FL_1"
                }
            ],
            "FlowID": "FL_0",
            "Type": "Root"
        }
    }


@pytest.fixture
def mock_flow_with_embedded_data():
    """Mock response for survey flow with existing embedded data"""
    return {
        "result": {
            "Flow": [
                {
                    "Type": "EmbeddedData",
                    "FlowID": "FL_1",
                    "EmbeddedData": [
                        {
                            "Description": "existing_field",
                            "Type": "Recipient",
                            "Field": "existing_field",
                            "VariableType": "String"
                        }
                    ]
                },
                {
                    "Type": "Block",
                    "ID": "BL_1",
                    "FlowID": "FL_2"
                }
            ],
            "FlowID": "FL_0",
            "Type": "Root"
        }
    }


class TestSetEmbeddedData:
    """Tests for set_embedded_data method"""

    @patch('requests.get')
    @patch('requests.put')
    def test_set_embedded_data_text_field(self, mock_put, mock_get, api, mock_flow_response):
        """Test setting a text embedded data field"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)
        mock_put.return_value = Mock(status_code=200)

        result = api.set_embedded_data(
            survey_id="SV_123",
            field_name="user_id",
            field_type="text"
        )

        assert result["success"] is True
        assert result["field_name"] == "user_id"
        assert result["field_type"] == "text"
        mock_put.assert_called_once()

    @patch('requests.get')
    @patch('requests.put')
    def test_set_embedded_data_number_field(self, mock_put, mock_get, api, mock_flow_response):
        """Test setting a number embedded data field"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)
        mock_put.return_value = Mock(status_code=200)

        result = api.set_embedded_data(
            survey_id="SV_123",
            field_name="score",
            field_type="number",
            value="100"
        )

        assert result["success"] is True
        assert result["field_name"] == "score"
        assert result["field_type"] == "number"
        assert result["value"] == "100"

    @patch('requests.get')
    @patch('requests.put')
    def test_set_embedded_data_date_field(self, mock_put, mock_get, api, mock_flow_response):
        """Test setting a date embedded data field"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)
        mock_put.return_value = Mock(status_code=200)

        result = api.set_embedded_data(
            survey_id="SV_123",
            field_name="start_date",
            field_type="date"
        )

        assert result["success"] is True
        assert result["field_type"] == "date"

    def test_set_embedded_data_invalid_type(self, api):
        """Test that invalid field type raises ValueError"""
        with pytest.raises(ValueError) as exc_info:
            api.set_embedded_data(
                survey_id="SV_123",
                field_name="test",
                field_type="invalid"
            )
        assert "field_type must be one of" in str(exc_info.value)

    @patch('requests.get')
    def test_set_embedded_data_flow_fetch_fails(self, mock_get, api):
        """Test that exception is raised when flow fetch fails"""
        mock_get.return_value = Mock(status_code=400, text="Bad Request")

        with pytest.raises(Exception) as exc_info:
            api.set_embedded_data(
                survey_id="SV_123",
                field_name="test",
                field_type="text"
            )
        assert "Failed to get survey flow" in str(exc_info.value)


class TestSetEmbeddedDataFields:
    """Tests for set_embedded_data_fields method"""

    @patch('requests.get')
    @patch('requests.put')
    def test_set_multiple_fields(self, mock_put, mock_get, api, mock_flow_response):
        """Test setting multiple embedded data fields at once"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)
        mock_put.return_value = Mock(status_code=200)

        result = api.set_embedded_data_fields(
            survey_id="SV_123",
            fields={
                "user_id": {"type": "text"},
                "score": {"type": "number", "value": "0"},
                "start_date": {"type": "date"}
            }
        )

        assert result["success"] is True
        assert result["count"] == 3
        assert set(result["fields"]) == {"user_id", "score", "start_date"}

    @patch('requests.get')
    @patch('requests.put')
    def test_set_fields_with_existing_embedded_data(
        self, mock_put, mock_get, api, mock_flow_with_embedded_data
    ):
        """Test adding fields when embedded data already exists"""
        mock_get.return_value = Mock(
            status_code=200, json=lambda: mock_flow_with_embedded_data
        )
        mock_put.return_value = Mock(status_code=200)

        result = api.set_embedded_data_fields(
            survey_id="SV_123",
            fields={"new_field": {"type": "text"}}
        )

        assert result["success"] is True

    @patch('requests.get')
    def test_set_fields_invalid_type(self, mock_get, api, mock_flow_response):
        """Test that invalid field type raises ValueError"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)

        with pytest.raises(ValueError) as exc_info:
            api.set_embedded_data_fields(
                survey_id="SV_123",
                fields={"test": {"type": "invalid"}}
            )
        assert "field_type for 'test' must be one of" in str(exc_info.value)


class TestGetEmbeddedData:
    """Tests for get_embedded_data method"""

    @patch('requests.get')
    def test_get_embedded_data(self, mock_get, api, mock_flow_with_embedded_data):
        """Test retrieving embedded data fields"""
        mock_get.return_value = Mock(
            status_code=200, json=lambda: mock_flow_with_embedded_data
        )

        result = api.get_embedded_data(survey_id="SV_123")

        assert len(result) == 1
        assert result[0]["Field"] == "existing_field"

    @patch('requests.get')
    def test_get_embedded_data_empty(self, mock_get, api, mock_flow_response):
        """Test retrieving embedded data when none exists"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)

        result = api.get_embedded_data(survey_id="SV_123")

        assert result == []


class TestDeleteEmbeddedData:
    """Tests for delete_embedded_data method"""

    @patch('requests.get')
    @patch('requests.put')
    def test_delete_embedded_data(self, mock_put, mock_get, api, mock_flow_with_embedded_data):
        """Test deleting an embedded data field"""
        mock_get.return_value = Mock(
            status_code=200, json=lambda: mock_flow_with_embedded_data
        )
        mock_put.return_value = Mock(status_code=200)

        result = api.delete_embedded_data(
            survey_id="SV_123",
            field_name="existing_field"
        )

        assert result is True

    @patch('requests.get')
    def test_delete_nonexistent_field(self, mock_get, api, mock_flow_response):
        """Test deleting a field that doesn't exist"""
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)

        with pytest.raises(Exception) as exc_info:
            api.delete_embedded_data(
                survey_id="SV_123",
                field_name="nonexistent"
            )
        assert "not found" in str(exc_info.value)


class TestGetSurveyUrlWithEmbeddedData:
    """Tests for get_survey_url_with_embedded_data method"""

    def test_url_with_embedded_data(self, api):
        """Test generating URL with embedded data parameters"""
        url = api.get_survey_url_with_embedded_data(
            survey_id="SV_123",
            embedded_data={
                "user_id": "12345",
                "source": "email"
            }
        )

        assert "https://test.qualtrics.com/jfe/form/SV_123?" in url
        assert "user_id=12345" in url
        assert "source=email" in url

    def test_url_with_special_characters(self, api):
        """Test URL encoding of special characters"""
        url = api.get_survey_url_with_embedded_data(
            survey_id="SV_123",
            embedded_data={"name": "John Doe", "tag": "a&b"}
        )

        assert "name=John+Doe" in url or "name=John%20Doe" in url
        assert "tag=a%26b" in url

    def test_url_without_embedded_data(self, api):
        """Test generating URL with empty embedded data"""
        url = api.get_survey_url_with_embedded_data(
            survey_id="SV_123",
            embedded_data={}
        )

        assert url == "https://test.qualtrics.com/jfe/form/SV_123"

    def test_url_base_format(self, api):
        """Test that base URL format is correct"""
        url = api.get_survey_url_with_embedded_data(
            survey_id="SV_abc123",
            embedded_data={"test": "value"}
        )

        assert url.startswith("https://test.qualtrics.com/jfe/form/SV_abc123?")


class TestIntegration:
    """Integration-style tests for embedded data workflow"""

    @patch('requests.get')
    @patch('requests.put')
    def test_full_workflow(self, mock_put, mock_get, api, mock_flow_response):
        """Test a complete embedded data workflow"""
        # Setup mocks
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_flow_response)
        mock_put.return_value = Mock(status_code=200)

        survey_id = "SV_test123"

        # 1. Set multiple embedded data fields
        result = api.set_embedded_data_fields(
            survey_id,
            {
                "user_id": {"type": "text"},
                "score": {"type": "number"},
                "enrolled_date": {"type": "date"}
            }
        )
        assert result["success"] is True

        # 2. Generate URL with values
        url = api.get_survey_url_with_embedded_data(
            survey_id,
            {
                "user_id": "U12345",
                "score": "95",
                "enrolled_date": "2026-01-15"
            }
        )

        assert "user_id=U12345" in url
        assert "score=95" in url
        assert "enrolled_date=2026-01-15" in url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
