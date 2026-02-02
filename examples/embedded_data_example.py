"""
Embedded Data Example - Personalize Surveys with External Data

This example demonstrates how to:
1. Configure embedded data fields in a survey
2. Generate personalized survey URLs with pre-populated data
3. Retrieve and manage embedded data configurations

Use cases:
- Pass user information (name, ID, email) to personalize surveys
- Track the source of survey respondents (email campaign, social media, etc.)
- Implement conditional logic based on external data
- Enable advanced data analysis with segmentation
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

# Initialize API
api = QualtricsAPI(api_token=API_TOKEN, data_center=DATA_CENTER)


def example_basic_embedded_data():
    """
    Example 1: Basic Embedded Data Setup

    Set up a simple survey with user identification fields.
    """
    print("\n" + "="*60)
    print("Example 1: Basic Embedded Data Setup")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("Customer Feedback with Embedded Data")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Set individual embedded data field
    result = api.set_embedded_data(
        survey_id=survey_id,
        field_name="customer_id",
        field_type="text"
    )
    print(f"Added field 'customer_id': {result}")

    # Set another field with a default value
    result = api.set_embedded_data(
        survey_id=survey_id,
        field_name="source",
        field_type="text",
        value="direct"
    )
    print(f"Added field 'source' with default value: {result}")

    # Add a question that references embedded data
    api.create_descriptive_text(
        survey_id,
        "<p>Thank you for participating in our survey!</p>"
    )

    api.create_multiple_choice_question(
        survey_id,
        "How satisfied are you with our service?",
        choices=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
    )

    # Generate personalized URL
    url = api.get_survey_url_with_embedded_data(
        survey_id,
        embedded_data={
            "customer_id": "CUST-12345",
            "source": "email_campaign"
        }
    )

    print(f"\nPersonalized Survey URL:")
    print(url)

    return survey_id


def example_multiple_fields():
    """
    Example 2: Multiple Embedded Data Fields

    Set up multiple fields at once for efficient configuration.
    """
    print("\n" + "="*60)
    print("Example 2: Multiple Embedded Data Fields")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("Employee Survey with Demographics")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Configure multiple fields at once
    result = api.set_embedded_data_fields(
        survey_id=survey_id,
        fields={
            "employee_id": {"type": "text"},
            "department": {"type": "text"},
            "years_employed": {"type": "number"},
            "hire_date": {"type": "date"},
            "is_manager": {"type": "text", "value": "false"}
        }
    )
    print(f"Configured {result['count']} embedded data fields: {result['fields']}")

    # Add questions
    api.create_nps_question(
        survey_id,
        "How likely are you to recommend our company as a place to work?"
    )

    api.create_text_entry_question(
        survey_id,
        "What would make our workplace better?",
        text_type="ML"
    )

    # Generate URLs for different employees
    print("\nGenerated URLs for employees:")

    employees = [
        {"employee_id": "E001", "department": "Engineering", "years_employed": "5"},
        {"employee_id": "E002", "department": "Marketing", "years_employed": "2"},
        {"employee_id": "E003", "department": "Sales", "years_employed": "8", "is_manager": "true"},
    ]

    for emp in employees:
        url = api.get_survey_url_with_embedded_data(survey_id, emp)
        print(f"  {emp['employee_id']} ({emp['department']}): {url[:80]}...")

    return survey_id


def example_retrieve_and_manage():
    """
    Example 3: Retrieve and Manage Embedded Data

    Demonstrate getting and deleting embedded data fields.
    """
    print("\n" + "="*60)
    print("Example 3: Retrieve and Manage Embedded Data")
    print("="*60)

    # Create a survey with some embedded data
    survey = api.create_survey("Data Management Example")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Add some fields
    api.set_embedded_data_fields(
        survey_id,
        fields={
            "field_to_keep": {"type": "text"},
            "field_to_delete": {"type": "text"},
            "another_field": {"type": "number"}
        }
    )

    # Retrieve all embedded data fields
    fields = api.get_embedded_data(survey_id)
    print(f"\nCurrent embedded data fields ({len(fields)}):")
    for field in fields:
        print(f"  - {field.get('Field')}: {field.get('VariableType')}")

    # Delete a field
    api.delete_embedded_data(survey_id, "field_to_delete")
    print("\nDeleted 'field_to_delete'")

    # Verify deletion
    fields = api.get_embedded_data(survey_id)
    print(f"\nRemaining embedded data fields ({len(fields)}):")
    for field in fields:
        print(f"  - {field.get('Field')}: {field.get('VariableType')}")

    return survey_id


def example_url_generation():
    """
    Example 4: URL Generation Patterns

    Different patterns for generating survey URLs with embedded data.
    """
    print("\n" + "="*60)
    print("Example 4: URL Generation Patterns")
    print("="*60)

    # Create a simple survey
    survey = api.create_survey("URL Generation Demo")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Configure embedded data
    api.set_embedded_data_fields(
        survey_id,
        fields={
            "utm_source": {"type": "text"},
            "utm_campaign": {"type": "text"},
            "user_segment": {"type": "text"}
        }
    )

    # Pattern 1: Basic URL (no embedded data)
    base_url = api.get_survey_url(survey_id)
    print(f"\nBase URL (no embedded data):")
    print(f"  {base_url}")

    # Pattern 2: URL with tracking parameters
    tracking_url = api.get_survey_url_with_embedded_data(
        survey_id,
        {
            "utm_source": "newsletter",
            "utm_campaign": "q1_feedback"
        }
    )
    print(f"\nTracking URL:")
    print(f"  {tracking_url}")

    # Pattern 3: URL with user segment
    segment_url = api.get_survey_url_with_embedded_data(
        survey_id,
        {
            "user_segment": "premium_users"
        }
    )
    print(f"\nSegment URL:")
    print(f"  {segment_url}")

    # Pattern 4: Full personalization
    full_url = api.get_survey_url_with_embedded_data(
        survey_id,
        {
            "utm_source": "email",
            "utm_campaign": "retention_survey",
            "user_segment": "at_risk"
        }
    )
    print(f"\nFully personalized URL:")
    print(f"  {full_url}")

    return survey_id


def cleanup_surveys(survey_ids):
    """Delete all created surveys"""
    print("\n" + "="*60)
    print("Cleanup")
    print("="*60)

    for survey_id in survey_ids:
        try:
            api.delete_survey(survey_id)
            print(f"Deleted survey: {survey_id}")
        except Exception as e:
            print(f"Failed to delete {survey_id}: {e}")


if __name__ == "__main__":
    print("Qualtrics SDK - Embedded Data Examples")
    print("="*60)

    created_surveys = []

    try:
        # Run all examples
        created_surveys.append(example_basic_embedded_data())
        created_surveys.append(example_multiple_fields())
        created_surveys.append(example_retrieve_and_manage())
        created_surveys.append(example_url_generation())

        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        raise

    finally:
        # Ask user if they want to delete the surveys
        print("\n")
        response = input("Delete all created surveys? (y/n): ").strip().lower()
        if response == 'y':
            cleanup_surveys(created_surveys)
        else:
            print("\nSurveys kept. IDs:")
            for survey_id in created_surveys:
                print(f"  - {survey_id}")
