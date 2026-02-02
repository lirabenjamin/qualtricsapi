"""
Example usage of the Qualtrics API module
This script demonstrates how to create surveys with various question types
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

# Initialize the API client
api = QualtricsAPI(api_token=API_TOKEN, data_center=DATA_CENTER)

print("=" * 60)
print("Qualtrics API - Comprehensive Example")
print("=" * 60)


def example_create_comprehensive_survey():
    """Create a survey with all question types"""
    try:
        # 1. Create the survey
        print("\n[1] Creating survey...")
        survey = api.create_survey(
            survey_name="Comprehensive Demo Survey - All Question Types"
        )
        survey_id = survey['SurveyID']
        print(f"✓ Survey created: {survey_id}")

        # 2. Add welcome text
        print("\n[2] Adding welcome text...")
        api.create_descriptive_text(
            survey_id,
            "<h2>Welcome to our survey!</h2><p>Thank you for taking the time to provide your feedback.</p>"
        )
        print("✓ Welcome text added")

        # 3. Add multiple choice question (radio buttons)
        print("\n[3] Adding multiple choice question (radio buttons)...")
        api.create_multiple_choice_question(
            survey_id,
            "What is your primary role?",
            choices=["Student", "Faculty", "Staff", "Administrator", "Other"],
            selector="SAVR"  # Single Answer Vertical (Radio)
        )
        print("✓ Radio button question added")

        # 4. Add dropdown question
        print("\n[4] Adding dropdown question...")
        api.create_multiple_choice_question(
            survey_id,
            "Which department are you affiliated with?",
            choices=["Arts & Sciences", "Engineering", "Business", "Medicine", "Law"],
            selector="DL"  # Dropdown List
        )
        print("✓ Dropdown question added")

        # 5. Add another multiple choice question (horizontal layout)
        print("\n[5] Adding horizontal radio button question...")
        api.create_multiple_choice_question(
            survey_id,
            "How would you rate your overall experience?",
            choices=["Poor", "Fair", "Good", "Very Good", "Excellent"],
            selector="SAHR"  # Single Answer Horizontal
        )
        print("✓ Horizontal radio button question added")

        # 6. Add single-line text entry
        print("\n[6] Adding single-line text entry...")
        api.create_text_entry_question(
            survey_id,
            "What is your email address?",
            text_type="SL"  # Single Line
        )
        print("✓ Single-line text entry added")

        # 7. Add multi-line text entry (essay)
        print("\n[7] Adding essay text box...")
        api.create_text_entry_question(
            survey_id,
            "Please share any additional comments or suggestions:",
            text_type="ML"  # Multi-Line
        )
        print("✓ Essay text box added")

        # 8. Add matrix/Likert scale question
        print("\n[8] Adding Likert scale matrix question...")
        api.create_matrix_question(
            survey_id,
            "Please rate your satisfaction with the following:",
            statements=[
                "Quality of instruction",
                "Course materials",
                "Learning environment",
                "Support services"
            ],
            scale_points=[
                "Very Dissatisfied",
                "Dissatisfied",
                "Neutral",
                "Satisfied",
                "Very Satisfied"
            ]
        )
        print("✓ Likert scale question added")

        # 9. Add slider question
        print("\n[9] Adding slider question...")
        api.create_slider_question(
            survey_id,
            "On a scale from 0 to 100, how would you rate your overall experience?",
            min_value=0,
            max_value=100,
            left_label="Poor",
            right_label="Excellent"
        )
        print("✓ Slider question added")

        # 10. Add rank order question
        print("\n[10] Adding rank order question...")
        api.create_rank_order_question(
            survey_id,
            "Please rank the following priorities (drag to reorder):",
            items=[
                "Academic excellence",
                "Career preparation",
                "Social activities",
                "Health and wellness",
                "Financial aid"
            ]
        )
        print("✓ Rank order question added")

        # 11. Add NPS question
        print("\n[11] Adding NPS (Net Promoter Score) question...")
        api.create_nps_question(
            survey_id,
            "How likely are you to recommend this institution to a friend or colleague?"
        )
        print("✓ NPS question added")

        # 12. Add closing text
        print("\n[12] Adding closing text...")
        api.create_descriptive_text(
            survey_id,
            "<h3>Thank you!</h3><p>We appreciate your feedback and will use it to improve our services.</p>"
        )
        print("✓ Closing text added")

        # Get survey URL
        survey_url = api.get_survey_url(survey_id)

        print("\n" + "=" * 60)
        print("✓ Survey created successfully!")
        print("=" * 60)
        print(f"Survey ID: {survey_id}")
        print(f"Survey URL: {survey_url}")
        print("=" * 60)

        return survey_id

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def example_list_surveys():
    """List all surveys in the account"""
    try:
        print("\n[Listing all surveys...]")
        surveys = api.list_surveys()
        print(f"\nFound {len(surveys)} surveys:")
        for survey in surveys[:5]:  # Show first 5
            print(f"  - {survey['name']} (ID: {survey['id']})")
        if len(surveys) > 5:
            print(f"  ... and {len(surveys) - 5} more")
    except Exception as e:
        print(f"✗ Error listing surveys: {e}")


def example_update_question(survey_id: str, question_id: str):
    """Update a question's text"""
    try:
        print(f"\n[Updating question {question_id}...]")
        api.update_question_text(
            survey_id,
            question_id,
            "What is your PRIMARY role? (Updated)"
        )
        print("✓ Question updated")
    except Exception as e:
        print(f"✗ Error updating question: {e}")


def example_delete_survey(survey_id: str):
    """Delete a survey"""
    try:
        print(f"\n[Deleting survey {survey_id}...]")
        api.delete_survey(survey_id)
        print("✓ Survey deleted")
    except Exception as e:
        print(f"✗ Error deleting survey: {e}")


# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Create a comprehensive survey
    survey_id = example_create_comprehensive_survey()

    # Optionally list all surveys
    # example_list_surveys()

    # Uncomment to delete the survey after creation (for testing)
    # if survey_id:
    #     input("\nPress Enter to delete the survey...")
    #     example_delete_survey(survey_id)