"""
Simple Qualtrics API Example - Quick Start
Copy and modify this for your own surveys
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

# Create a simple survey
def create_simple_survey():
    # 1. Create the survey
    survey = api.create_survey("Quick Survey Example")
    survey_id = survey['SurveyID']

    print(f"Survey created: {survey_id}")

    # 2. Add a welcome message
    api.create_descriptive_text(
        survey_id,
        "<h2>Welcome!</h2><p>This survey will take about 2 minutes.</p>"
    )

    # 3. Add a multiple choice question
    api.create_multiple_choice_question(
        survey_id,
        "How did you hear about us?",
        choices=["Google", "Social Media", "Friend", "Advertisement", "Other"],
        selector="SAVR"  # Radio buttons
    )

    # 4. Add a rating scale
    api.create_matrix_question(
        survey_id,
        "Please rate the following:",
        statements=["Overall experience", "Ease of use", "Value"],
        scale_points=["Poor", "Fair", "Good", "Very Good", "Excellent"]
    )

    # 5. Add an open text question
    api.create_text_entry_question(
        survey_id,
        "Any suggestions for improvement?",
        text_type="ML"  # Multi-line
    )

    # 6. Add NPS question
    api.create_nps_question(
        survey_id,
        "How likely are you to recommend us to a friend?"
    )

    # 7. Add thank you message
    api.create_descriptive_text(
        survey_id,
        "<h3>Thank you!</h3><p>We appreciate your feedback.</p>"
    )

    # Get the survey URL
    url = api.get_survey_url(survey_id)

    print(f"\n✓ Survey ready!")
    print(f"Survey URL: {url}")
    print(f"Survey ID: {survey_id}")

    return survey_id


# Run it
if __name__ == "__main__":
    survey_id = create_simple_survey()

    # Uncomment to delete the survey after testing
    # api.delete_survey(survey_id)
    # print(f"Survey {survey_id} deleted")
