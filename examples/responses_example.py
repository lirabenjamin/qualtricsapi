"""
Response Management Example
Demonstrates how to retrieve, export, and manage survey responses
"""

import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from qualtrics_sdk import QualtricsAPI

# Load credentials from .env file
load_dotenv()

API_TOKEN = os.getenv('QUALTRICS_API_TOKEN')
DATA_CENTER = os.getenv('QUALTRICS_DATA_CENTER')

if not API_TOKEN or not DATA_CENTER:
    raise ValueError("Please set QUALTRICS_API_TOKEN and QUALTRICS_DATA_CENTER in .env file")

# Initialize
api = QualtricsAPI(api_token=API_TOKEN, data_center=DATA_CENTER)


def response_management_demo(survey_id: str):
    """
    Demonstrate response management features

    Args:
        survey_id: An existing survey ID with responses
    """
    print(f"Response Management Demo for Survey: {survey_id}")
    print("=" * 50)

    # 1. Get response count
    print("\n1. Getting response count...")
    count = api.get_response_count(survey_id)
    print(f"   Total responses: {count}")

    # 2. Get response statistics
    print("\n2. Getting response statistics...")
    stats = api.get_response_statistics(survey_id)
    print(f"   Total: {stats['total']}")
    print(f"   Complete: {stats['complete']}")
    print(f"   Incomplete: {stats['incomplete']}")
    print(f"   Completion rate: {stats['completion_rate']}%")

    # 3. List responses with pagination
    print("\n3. Listing responses (first 10)...")
    result = api.list_responses(survey_id, limit=10)
    print(f"   Found {result['total']} responses in this page")
    for i, response in enumerate(result['responses'][:5], 1):
        response_id = response.get('responseId', 'N/A')
        print(f"   {i}. Response ID: {response_id}")

    # 4. List responses with date filter
    print("\n4. Listing responses with date filter...")
    # Example: Get responses from the last 30 days
    result = api.list_responses(
        survey_id,
        start_date="2024-01-01T00:00:00Z",
        limit=5
    )
    print(f"   Found {result['total']} responses since 2024-01-01")

    # 5. Export responses to CSV
    print("\n5. Exporting responses to CSV...")
    try:
        output_path = api.export_responses_to_file(
            survey_id,
            "responses_export.csv",
            format="csv",
            extract=True
        )
        print(f"   Exported to: {output_path}")
    except Exception as e:
        print(f"   Export failed: {e}")

    # 6. Export responses to JSON
    print("\n6. Exporting responses to JSON...")
    try:
        output_path = api.export_responses_to_file(
            survey_id,
            "responses_export.json",
            format="json",
            extract=True
        )
        print(f"   Exported to: {output_path}")
    except Exception as e:
        print(f"   Export failed: {e}")

    # 7. Get raw export data (bytes)
    print("\n7. Getting raw export data...")
    try:
        data = api.export_responses(survey_id, format="csv")
        print(f"   Downloaded {len(data)} bytes")
    except Exception as e:
        print(f"   Export failed: {e}")

    # 8. Get response schema
    print("\n8. Getting response schema...")
    try:
        schema = api.get_response_schema(survey_id)
        print(f"   Schema contains {len(schema)} properties")
    except Exception as e:
        print(f"   Schema retrieval failed: {e}")

    print("\n" + "=" * 50)
    print("Demo complete!")


def delete_response_demo(survey_id: str, response_id: str):
    """
    Demonstrate deleting a single response

    WARNING: This permanently deletes data!

    Args:
        survey_id: The survey ID
        response_id: The response ID to delete
    """
    print(f"Deleting response {response_id} from survey {survey_id}")

    # Delete single response
    success = api.delete_response(survey_id, response_id)
    if success:
        print("Response deleted successfully")


def bulk_delete_demo(survey_id: str, response_ids: list):
    """
    Demonstrate bulk deletion of responses

    WARNING: This permanently deletes data!

    Args:
        survey_id: The survey ID
        response_ids: List of response IDs to delete
    """
    print(f"Bulk deleting {len(response_ids)} responses...")

    result = api.delete_responses(survey_id, response_ids)
    print(f"Deleted: {result['deleted']}")
    if result['errors']:
        print(f"Errors: {len(result['errors'])}")
        for error in result['errors']:
            print(f"  - {error['response_id']}: {error['error']}")


# Run it
if __name__ == "__main__":
    # Replace with your actual survey ID
    SURVEY_ID = "SV_XXXXXXXXXXXXXXX"

    # List available surveys first
    print("Available surveys:")
    surveys = api.list_surveys()
    for survey in surveys[:5]:
        print(f"  - {survey['id']}: {survey['name']}")

    print("\n" + "-" * 50)
    print("To run the demo, update SURVEY_ID with a valid survey ID")
    print("Then uncomment the demo call below:")
    print("-" * 50)

    # Uncomment to run the demo
    # response_management_demo(SURVEY_ID)

    # Uncomment to delete a specific response (use with caution!)
    # delete_response_demo(SURVEY_ID, "R_XXXXXXXXXXXXXXX")
