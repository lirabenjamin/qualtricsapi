"""
Custom JavaScript Example - Add Interactivity to Survey Questions

This example demonstrates how to:
1. Add custom JavaScript to questions
2. Create auto-advance questions (timed displays)
3. Add countdown timers
4. Implement custom input validation
5. Embed iframes (videos, external content)
6. Modify the next button
7. Style response choices

Use cases:
- Putting in an iframe or timer
- Manipulating Qualtrics DOM (e.g., changing response option format)
- Changes to the next button
- Custom validation patterns
- A/B testing displays
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


def example_basic_javascript():
    """
    Example 1: Basic Custom JavaScript

    Add custom JavaScript to log messages and manipulate the question container.
    """
    print("\n" + "="*60)
    print("Example 1: Basic Custom JavaScript")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Basic")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a question
    q1 = api.create_multiple_choice_question(
        survey_id,
        "What is your favorite color?",
        choices=["Red", "Blue", "Green", "Yellow"]
    )
    q1_id = q1.get('QuestionID', 'QID1')
    print(f"Created question: {q1_id}")

    # Add custom JavaScript
    js_code = '''
Qualtrics.SurveyEngine.addOnload(function() {
    console.log('Question loaded - ID: ' + this.questionId);
});

Qualtrics.SurveyEngine.addOnReady(function() {
    // Add a custom message above the question
    var messageDiv = document.createElement('div');
    messageDiv.innerHTML = '<p style="color: #666; font-style: italic;">Please select your favorite color below:</p>';
    messageDiv.style.marginBottom = '10px';

    var questionContainer = this.getQuestionContainer();
    var questionText = questionContainer.querySelector('.QuestionText');
    if (questionText) {
        questionText.appendChild(messageDiv);
    }
});

Qualtrics.SurveyEngine.addOnUnload(function() {
    console.log('Question unloaded');
});
'''
    api.add_question_javascript(survey_id, q1_id, js_code)
    print("Added custom JavaScript to question")

    # Verify JavaScript was added
    js = api.get_question_javascript(survey_id, q1_id)
    print(f"JavaScript code length: {len(js)} characters")

    # Get survey URL
    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")

    return survey_id


def example_auto_advance():
    """
    Example 2: Auto-Advance Questions

    Create a timed question that automatically advances after a delay.
    Useful for showing instructions or stimuli for a fixed duration.
    """
    print("\n" + "="*60)
    print("Example 2: Auto-Advance Questions")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Auto Advance")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create an instruction screen that auto-advances
    q1 = api.create_descriptive_text(
        survey_id,
        """
        <h2>Welcome to our survey!</h2>
        <p>This screen will automatically advance in 5 seconds.</p>
        <p>Please read the following instructions carefully...</p>
        """
    )
    q1_id = q1.get('QuestionID', 'QID1')
    print(f"Created instruction screen: {q1_id}")

    # Add auto-advance after 5 seconds
    api.add_auto_advance(survey_id, q1_id, delay_ms=5000)
    print("Added auto-advance (5 seconds)")

    # Create a regular question after
    api.create_multiple_choice_question(
        survey_id,
        "Did you read the instructions?",
        choices=["Yes, completely", "Yes, partially", "No"]
    )

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")
    print("Note: The first screen will auto-advance after 5 seconds")

    return survey_id


def example_timer_display():
    """
    Example 3: Countdown Timer Display

    Add a visible countdown timer to a question.
    Useful for timed tests or limiting response time.
    """
    print("\n" + "="*60)
    print("Example 3: Countdown Timer Display")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Timer")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a timed question
    q1 = api.create_text_entry_question(
        survey_id,
        "You have 30 seconds to answer: What are the benefits of regular exercise? List as many as you can.",
        text_type="ML"
    )
    q1_id = q1.get('QuestionID', 'QID1')
    print(f"Created timed question: {q1_id}")

    # Add 30-second countdown timer that auto-advances
    api.add_timer_display(
        survey_id, q1_id,
        duration_seconds=30,
        auto_advance=True,
        timer_position='top'
    )
    print("Added 30-second countdown timer")

    # Create another timed question with timer at bottom, no auto-advance
    q2 = api.create_multiple_choice_question(
        survey_id,
        "Quick! Select your answer (60 seconds):",
        choices=["Option A", "Option B", "Option C", "Option D"]
    )
    q2_id = q2.get('QuestionID', 'QID2')

    api.add_timer_display(
        survey_id, q2_id,
        duration_seconds=60,
        auto_advance=False,
        timer_position='bottom'
    )
    print("Added 60-second timer (no auto-advance)")

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")

    return survey_id


def example_input_validation():
    """
    Example 4: Custom Input Validation

    Add custom validation patterns to text entry questions.
    """
    print("\n" + "="*60)
    print("Example 4: Custom Input Validation")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Validation")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a ZIP code question with validation
    q1 = api.create_text_entry_question(
        survey_id,
        "Please enter your 5-digit ZIP code:",
        text_type="SL"
    )
    q1_id = q1.get('QuestionID', 'QID1')

    api.add_input_validation(
        survey_id, q1_id,
        regex=r"^\d{5}$",
        error_message="Please enter a valid 5-digit ZIP code (e.g., 12345)"
    )
    print(f"Created ZIP code question with validation: {q1_id}")

    # Create an email question with validation
    q2 = api.create_text_entry_question(
        survey_id,
        "Please enter your email address:",
        text_type="SL"
    )
    q2_id = q2.get('QuestionID', 'QID2')

    api.add_input_validation(
        survey_id, q2_id,
        regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
        error_message="Please enter a valid email address (e.g., user@example.com)"
    )
    print(f"Created email question with validation: {q2_id}")

    # Create a phone number question with validation
    q3 = api.create_text_entry_question(
        survey_id,
        "Please enter your phone number (format: 123-456-7890):",
        text_type="SL"
    )
    q3_id = q3.get('QuestionID', 'QID3')

    api.add_input_validation(
        survey_id, q3_id,
        regex=r"^\d{3}-\d{3}-\d{4}$",
        error_message="Please enter phone number in format: 123-456-7890"
    )
    print(f"Created phone number question with validation: {q3_id}")

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")
    print("Note: Validation will show error messages for invalid inputs")

    return survey_id


def example_iframe_embed():
    """
    Example 5: Embed iframes

    Embed external content (videos, websites) in questions.
    """
    print("\n" + "="*60)
    print("Example 5: Embed iframes")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - iframes")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a question with embedded video
    q1 = api.create_multiple_choice_question(
        survey_id,
        "After watching the video above, how would you rate it?",
        choices=["Excellent", "Good", "Average", "Poor"]
    )
    q1_id = q1.get('QuestionID', 'QID1')

    # Add YouTube video iframe at top of question
    # Note: Replace with actual video URL
    api.add_iframe(
        survey_id, q1_id,
        iframe_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
        width="560px",
        height="315px",
        position="top"
    )
    print(f"Created question with embedded video: {q1_id}")

    # Create another question with embedded content
    q2 = api.create_text_entry_question(
        survey_id,
        "Please review the content above and provide your feedback:",
        text_type="ML"
    )
    q2_id = q2.get('QuestionID', 'QID2')

    api.add_iframe(
        survey_id, q2_id,
        iframe_url="https://example.com",
        width="100%",
        height="300px",
        position="top"
    )
    print(f"Created question with embedded website: {q2_id}")

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")

    return survey_id


def example_next_button():
    """
    Example 6: Modify Next Button

    Customize the next button behavior and appearance.
    """
    print("\n" + "="*60)
    print("Example 6: Modify Next Button")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Next Button")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a question with custom button text
    q1 = api.create_descriptive_text(
        survey_id,
        """
        <h2>Section 1: Demographics</h2>
        <p>In this section, we will ask about your background.</p>
        """
    )
    q1_id = q1.get('QuestionID', 'QID1')

    api.add_next_button_modification(
        survey_id, q1_id,
        button_text="Begin Demographics Section"
    )
    print(f"Created intro with custom button text: {q1_id}")

    # Create a question where button appears after delay
    q2 = api.create_descriptive_text(
        survey_id,
        """
        <h3>Please read carefully:</h3>
        <p>This is important information about the study.</p>
        <p>Take your time to read through all the details below...</p>
        <p>The 'Continue' button will appear in 5 seconds.</p>
        """
    )
    q2_id = q2.get('QuestionID', 'QID2')

    api.add_next_button_modification(
        survey_id, q2_id,
        button_text="Continue",
        hide_button=True,
        show_after_ms=5000
    )
    print(f"Created reading screen (button appears after 5s): {q2_id}")

    # Create a question with styled button
    q3 = api.create_multiple_choice_question(
        survey_id,
        "Are you ready to submit your final answers?",
        choices=["Yes, submit now", "No, let me review"]
    )
    q3_id = q3.get('QuestionID', 'QID3')

    api.add_next_button_modification(
        survey_id, q3_id,
        button_text="Submit Final Answers",
        custom_style="background-color: #4CAF50; color: white; font-weight: bold; padding: 15px 30px;"
    )
    print(f"Created final question with styled button: {q3_id}")

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")

    return survey_id


def example_choice_styling():
    """
    Example 7: Style Response Choices

    Customize the appearance of multiple choice options.
    """
    print("\n" + "="*60)
    print("Example 7: Style Response Choices")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Choice Styling")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a question with styled choices
    q1 = api.create_multiple_choice_question(
        survey_id,
        "Select your preferred option:",
        choices=["Option A - Premium", "Option B - Standard", "Option C - Basic", "Option D - Free"]
    )
    q1_id = q1.get('QuestionID', 'QID1')

    api.add_choice_style(
        survey_id, q1_id,
        background_color="#f5f5f5",
        border_radius="8px",
        hover_color="#e0e0e0",
        selected_color="#bbdefb"
    )
    print(f"Created styled multiple choice question: {q1_id}")

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")

    return survey_id


def example_combined_features():
    """
    Example 8: Combined Features

    Create a survey that combines multiple JavaScript features.
    """
    print("\n" + "="*60)
    print("Example 8: Combined Features")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Combined")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Screen 1: Welcome with auto-advance
    q1 = api.create_descriptive_text(
        survey_id,
        """
        <h2>Welcome to the Interactive Survey!</h2>
        <p>This survey demonstrates various JavaScript enhancements.</p>
        <p><em>This screen will advance automatically in 3 seconds...</em></p>
        """
    )
    q1_id = q1.get('QuestionID', 'QID1')
    api.add_auto_advance(survey_id, q1_id, delay_ms=3000)
    print(f"Screen 1: Welcome with auto-advance: {q1_id}")

    # Screen 2: Timed question
    q2 = api.create_text_entry_question(
        survey_id,
        "Quick response: Name three things you see around you right now.",
        text_type="SL"
    )
    q2_id = q2.get('QuestionID', 'QID2')
    api.add_timer_display(survey_id, q2_id, duration_seconds=15, auto_advance=True)
    print(f"Screen 2: Timed question: {q2_id}")

    # Screen 3: Styled choices
    q3 = api.create_multiple_choice_question(
        survey_id,
        "How would you rate this interactive survey experience?",
        choices=["Excellent", "Very Good", "Good", "Fair", "Poor"]
    )
    q3_id = q3.get('QuestionID', 'QID3')
    api.add_choice_style(
        survey_id, q3_id,
        background_color="#e3f2fd",
        border_radius="12px",
        hover_color="#bbdefb",
        selected_color="#2196f3"
    )
    api.add_next_button_modification(
        survey_id, q3_id,
        button_text="Submit Survey",
        custom_style="background-color: #1976D2; color: white; font-size: 16px;"
    )
    print(f"Screen 3: Styled choices with custom button: {q3_id}")

    url = api.get_survey_url(survey_id)
    print(f"\nSurvey URL: {url}")
    print("\nThis survey demonstrates:")
    print("  - Auto-advancing welcome screen (3s)")
    print("  - Timed text entry question (15s)")
    print("  - Styled choice options with custom submit button")

    return survey_id


def example_get_and_remove_javascript():
    """
    Example 9: Get and Remove JavaScript

    Demonstrate how to retrieve and remove JavaScript from questions.
    """
    print("\n" + "="*60)
    print("Example 9: Get and Remove JavaScript")
    print("="*60)

    # Create a new survey
    survey = api.create_survey("JavaScript Demo - Management")
    survey_id = survey['SurveyID']
    print(f"\nCreated survey: {survey_id}")

    # Create a question
    q1 = api.create_multiple_choice_question(
        survey_id,
        "Test question",
        choices=["A", "B", "C"]
    )
    q1_id = q1.get('QuestionID', 'QID1')

    # Initially no JavaScript
    js = api.get_question_javascript(survey_id, q1_id)
    print(f"Initial JavaScript: {js if js else '(none)'}")

    # Add JavaScript
    api.add_question_javascript(
        survey_id, q1_id,
        "Qualtrics.SurveyEngine.addOnload(function() { console.log('Hello!'); });"
    )
    print("Added JavaScript to question")

    # Get JavaScript
    js = api.get_question_javascript(survey_id, q1_id)
    print(f"Current JavaScript ({len(js)} chars): {js[:50]}...")

    # Append more JavaScript
    api.add_question_javascript(
        survey_id, q1_id,
        "Qualtrics.SurveyEngine.addOnReady(function() { console.log('Ready!'); });",
        append=True
    )
    print("Appended additional JavaScript")

    js = api.get_question_javascript(survey_id, q1_id)
    print(f"Updated JavaScript ({len(js)} chars)")

    # Remove JavaScript
    api.remove_question_javascript(survey_id, q1_id)
    print("Removed all JavaScript")

    js = api.get_question_javascript(survey_id, q1_id)
    print(f"Final JavaScript: {js if js else '(none)'}")

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
    print("Qualtrics SDK - Custom JavaScript Examples")
    print("="*60)

    created_surveys = []

    try:
        # Run all examples
        created_surveys.append(example_basic_javascript())
        created_surveys.append(example_auto_advance())
        created_surveys.append(example_timer_display())
        created_surveys.append(example_input_validation())
        created_surveys.append(example_iframe_embed())
        created_surveys.append(example_next_button())
        created_surveys.append(example_choice_styling())
        created_surveys.append(example_combined_features())
        created_surveys.append(example_get_and_remove_javascript())

        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        print("\nFeatures demonstrated:")
        print("  1. Basic custom JavaScript")
        print("  2. Auto-advance questions")
        print("  3. Countdown timer display")
        print("  4. Custom input validation")
        print("  5. Iframe embedding")
        print("  6. Next button modification")
        print("  7. Choice styling")
        print("  8. Combined features")
        print("  9. Get/remove JavaScript")

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
