"""
Embedded Data Example - Personalize Surveys with External Data

This example demonstrates how to:
1. Configure embedded data fields in a survey
2. Generate personalized survey URLs with pre-populated data
3. Retrieve and manage embedded data configurations
4. Set dynamic values from question answers, random numbers, and text

Use cases:
- Pass user information (name, ID, email) to personalize surveys
- Track the source of survey respondents (email campaign, social media, etc.)
- Implement conditional logic based on external data
- Enable advanced data analysis with segmentation
- Capture question answers as embedded data for downstream processing
- Generate random numbers for A/B testing or lottery systems
- Record timestamps and response metadata
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


def example_dynamic_values():
    """
    Example 5: Dynamic Embedded Data Values

    Demonstrates embedded data set from:
    - Question answers (piped text)
    - Random numbers
    - Static text values

    IMPORTANT: Embedded data placement matters!
    - position="start": For static values, random numbers, URL parameters
      (evaluated BEFORE questions are shown)
    - position="end": For capturing question answers with piped text
      (evaluated AFTER questions are answered)
    """
    print("\n" + "="*60)
    print("Example 5: Dynamic Embedded Data Values")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("Dynamic Embedded Data Demo")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # STEP 1: Set embedded data that should be evaluated at the START
    # (before questions are shown) - static values and random numbers
    result1 = api.set_embedded_data_fields(
        survey_id,
        fields={
            # Static text value - always the same
            "survey_version": {"type": "text", "value": "v2.1"},

            # Random number between 1-1000 (for A/B testing, random assignment)
            # Uses Qualtrics syntax: ${rand://int/min:max}
            "random_group": {"type": "text", "value": "${rand://int/1:1000}"},

            # Random number for lottery/prize drawing
            "lottery_number": {"type": "text", "value": "${rand://int/100000:999999}"},

            # Response ID for tracking (available at start)
            "response_id": {"type": "text", "value": "${e://Field/ResponseID}"},
        },
        position="start"  # Evaluated before questions
    )
    print(f"\nConfigured {result1['count']} START embedded data fields (static/random)")

    # STEP 2: Add questions
    q1 = api.create_multiple_choice_question(
        survey_id,
        "What is your role?",
        choices=["Student", "Teacher", "Administrator", "Other"]
    )
    q1_id = q1.get('QuestionID', 'QID1')
    print(f"Created role question: {q1_id}")

    q2 = api.create_text_entry_question(
        survey_id,
        "What is your name?",
        text_type="SL"  # Single line
    )
    q2_id = q2.get('QuestionID', 'QID2')
    print(f"Created name question: {q2_id}")

    # STEP 3: Set embedded data that captures question answers
    # These MUST be at the END of the flow (after questions)
    result2 = api.set_embedded_data_fields(
        survey_id,
        fields={
            # Capture the respondent's role from Q1
            # Uses piped text: ${q://QID/ChoiceGroup/SelectedChoices}
            "user_role": {"type": "text", "value": f"${{q://{q1_id}/ChoiceGroup/SelectedChoices}}"},

            # Capture the respondent's name from Q2
            # Uses piped text: ${q://QID/ChoiceTextEntryValue}
            "respondent_name": {"type": "text", "value": f"${{q://{q2_id}/ChoiceTextEntryValue}}"},

            # Current date/time when survey is completed
            "completion_date": {"type": "text", "value": "${date://CurrentDate/m%2Fd%2FY}"},
        },
        position="end"  # Evaluated AFTER questions are answered
    )
    print(f"Configured {result2['count']} END embedded data fields (question captures)")

    # STEP 4: Create a NEW BLOCK for the thank you message
    # This block will be added to the flow AFTER the END embedded data,
    # so it can display all captured values including name and role.
    thank_you_block = api.create_block(survey_id, "Thank You Block")
    thank_you_block_id = thank_you_block.get('BlockID')
    print(f"Created thank you block: {thank_you_block_id}")

    # Add the thank you message to the new block
    # Now we can display ALL embedded data including the captured values!
    api.create_descriptive_text(
        survey_id,
        """
        <h3>Thank you, ${e://Field/respondent_name}!</h3>
        <p>Your response has been recorded.</p>
        <p>Your lottery number is: <strong>${e://Field/lottery_number}</strong></p>
        <p>You were assigned to group: ${e://Field/random_group}</p>
        <p>Your role: ${e://Field/user_role}</p>
        <p>Survey version: ${e://Field/survey_version}</p>
        <p>Completed on: ${e://Field/completion_date}</p>
        """,
        block_id=thank_you_block_id
    )

    # STEP 5: Move the thank you block to the END of the flow (after END embedded data)
    # Get current flow and reorder it
    flow = api.get_survey_flow(survey_id)
    flow_list = flow.get('Flow', [])

    # Find and remove the thank you block from its current position
    thank_you_flow_element = None
    new_flow_list = []
    for element in flow_list:
        if element.get('ID') == thank_you_block_id:
            thank_you_flow_element = element
        else:
            new_flow_list.append(element)

    # Add it back at the very end
    if thank_you_flow_element:
        new_flow_list.append(thank_you_flow_element)

    # Update the flow
    import requests
    update_payload = {
        "FlowID": flow.get('FlowID'),
        "Type": flow.get('Type'),
        "Flow": new_flow_list,
        "Properties": flow.get('Properties', {})
    }
    response = requests.put(
        f'{api.base_url}/survey-definitions/{survey_id}/flow',
        headers=api.headers,
        json=update_payload
    )
    if response.status_code == 200:
        print("Moved thank you block to end of flow")
    else:
        print(f"Warning: Could not reorder flow: {response.text}")

    # Retrieve and display the embedded data configuration
    fields = api.get_embedded_data(survey_id)
    print(f"\nEmbedded data fields configured ({len(fields)} total):")
    for field in fields:
        field_name = field.get('Field', 'unknown')
        value = field.get('Value', '(no default)')
        print(f"  - {field_name}: {value}")

    # Generate the survey URL
    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")
    print("\nFlow order:")
    print("  1. START embedded data (random_group, lottery_number, etc.)")
    print("  2. Questions block (role question, name question)")
    print("  3. END embedded data (captures user_role, respondent_name from answers)")
    print("  4. Thank You block (can display ALL embedded data including captured values)")

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
        created_surveys.append(example_dynamic_values())

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
