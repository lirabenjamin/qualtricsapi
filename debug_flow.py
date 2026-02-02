"""
Debug script to examine survey flow before and after adding embedded data
"""
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from qualtrics_sdk import QualtricsAPI

load_dotenv()

API_TOKEN = os.getenv('QUALTRICS_API_TOKEN')
DATA_CENTER = os.getenv('QUALTRICS_DATA_CENTER')

if not API_TOKEN or not DATA_CENTER:
    raise ValueError("Please set QUALTRICS_API_TOKEN and QUALTRICS_DATA_CENTER in .env file")

api = QualtricsAPI(api_token=API_TOKEN, data_center=DATA_CENTER)


def debug_flow():
    """Create a survey and examine flow at each step"""

    print("=" * 60)
    print("STEP 1: Create survey")
    print("=" * 60)
    survey = api.create_survey("Debug Flow Test")
    survey_id = survey['SurveyID']
    print(f"Created survey: {survey_id}")

    print("\n" + "=" * 60)
    print("STEP 2: Get initial flow (before any changes)")
    print("=" * 60)
    flow1 = api.get_survey_flow(survey_id)
    print(json.dumps(flow1, indent=2))

    print("\n" + "=" * 60)
    print("STEP 3: Add a question")
    print("=" * 60)
    q1 = api.create_multiple_choice_question(
        survey_id,
        "Test question?",
        choices=["A", "B", "C"]
    )
    print(f"Created question: {q1.get('QuestionID')}")

    print("\n" + "=" * 60)
    print("STEP 4: Get flow after adding question")
    print("=" * 60)
    flow2 = api.get_survey_flow(survey_id)
    print(json.dumps(flow2, indent=2))

    print("\n" + "=" * 60)
    print("STEP 5: Add embedded data at START")
    print("=" * 60)
    result = api.set_embedded_data_fields(
        survey_id,
        fields={
            "test_field": {"type": "text", "value": "hello"}
        },
        position="start"
    )
    print(f"Result: {result}")

    print("\n" + "=" * 60)
    print("STEP 6: Get flow after adding embedded data")
    print("=" * 60)
    flow3 = api.get_survey_flow(survey_id)
    print(json.dumps(flow3, indent=2))

    print("\n" + "=" * 60)
    print("STEP 7: Survey URL for testing preview")
    print("=" * 60)
    url = api.get_survey_url(survey_id)
    print(f"Preview URL: {url}")
    print(f"\nTry opening this in your browser to test preview.")

    print("\n" + "=" * 60)
    response = input("Delete this test survey? (y/n): ").strip().lower()
    if response == 'y':
        api.delete_survey(survey_id)
        print(f"Deleted survey: {survey_id}")
    else:
        print(f"Survey kept: {survey_id}")


if __name__ == "__main__":
    debug_flow()
