# Qualtrics API Python Module

A comprehensive Python wrapper for the Qualtrics REST API v3. This module provides easy-to-use functions for creating, managing, and deleting surveys with support for all major question types.

## Features

- **Survey Management**: Create, read, update, and delete surveys
- **Question Types**: Support for all major question types:
  - Multiple choice (radio buttons)
  - Checkboxes (multiple answers)
  - Dropdown lists
  - Text entry (single line and multi-line/essay)
  - Matrix/Likert scale questions
  - Slider questions
  - Rank order questions
  - Net Promoter Score (NPS)
  - Descriptive text blocks
- **Question Management**: Add, update, and delete questions
- **Block Management**: Create and manage survey blocks
- **Display Logic**: Create conditional questions that show/hide based on responses
  - Single and multiple condition logic with AND/OR operators
  - Support for all comparison operators (Selected, EqualTo, GreaterThan, Contains, etc.)
  - Helper methods for common patterns (show_only_if, skip_if)
- **Embedded Data**: Configure embedded data fields and generate personalized survey URLs
- **Custom JavaScript**: Add custom JavaScript to questions for advanced interactivity
  - Auto-advance questions with timing delays
  - Countdown timers with visual display
  - Custom input validation with regex patterns
  - Embed iframes (videos, external content)
  - Modify next button appearance and behavior
  - Style response choices with custom colors
- **Professional Code Organization**: Modular structure with mixin pattern for easy maintenance and extension

## Code Organization

This package uses a clean, modular structure for easy navigation and maintenance:

```
qualtrics_sdk/core/
├── base.py                 - Core API & authentication
├── surveys.py              - Survey operations
├── questions.py            - Question creation (all types)
├── question_management.py  - Question updates/deletes
├── blocks.py               - Block operations
├── display_logic.py        - Display logic / conditional questions
├── embedded_data.py        - Embedded data operations
├── javascript.py           - Custom JavaScript for questions
└── client.py               - Combines all functionality
```

**Benefits:** Easy to find code, test independently, and extend with new features.

See [docs/CODE_ORGANIZATION.md](docs/CODE_ORGANIZATION.md) for details.

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```bash
QUALTRICS_API_TOKEN=your_api_token_here
QUALTRICS_DATA_CENTER=your_datacenter.qualtrics.com
```

**Important:** Never commit your `.env` file to version control. It's already in `.gitignore`.

## Quick Start

```python
import os
from dotenv import load_dotenv
from qualtrics_api import QualtricsAPI

# Load credentials from .env file
load_dotenv()

api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)

# Create a survey
survey = api.create_survey("My Survey")
survey_id = survey['SurveyID']

# Add a multiple choice question
api.create_multiple_choice_question(
    survey_id,
    "What is your role?",
    choices=["Student", "Faculty", "Staff"],
    selector="SAVR"  # Radio buttons
)

# Get the survey URL
url = api.get_survey_url(survey_id)
print(f"Survey URL: {url}")
```

## Usage Examples

### Creating Different Question Types

#### 1. Multiple Choice (Radio Buttons)
```python
api.create_multiple_choice_question(
    survey_id,
    "What is your primary role?",
    choices=["Student", "Faculty", "Staff", "Other"],
    selector="SAVR"  # Single Answer Vertical (Radio)
)
```

#### 2. Dropdown List
```python
api.create_multiple_choice_question(
    survey_id,
    "Select your department:",
    choices=["Engineering", "Business", "Arts", "Science"],
    selector="DL"  # Dropdown List
)
```

#### 3. Checkboxes (Multiple Answers)
```python
api.create_multiple_choice_question(
    survey_id,
    "Select all that apply:",
    choices=["Option 1", "Option 2", "Option 3"],
    selector="MAVR"  # Multiple Answer Vertical (Checkboxes)
)
```

#### 4. Text Entry (Single Line)
```python
api.create_text_entry_question(
    survey_id,
    "What is your email?",
    text_type="SL"  # Single Line
)
```

#### 5. Text Entry (Essay/Multi-line)
```python
api.create_text_entry_question(
    survey_id,
    "Please share your feedback:",
    text_type="ML"  # Multi-Line
)
```

#### 6. Matrix/Likert Scale
```python
api.create_matrix_question(
    survey_id,
    "Rate your satisfaction:",
    statements=["Quality", "Service", "Value"],
    scale_points=["Poor", "Fair", "Good", "Excellent"]
)
```

#### 7. Slider
```python
api.create_slider_question(
    survey_id,
    "Rate your experience:",
    min_value=0,
    max_value=100,
    left_label="Poor",
    right_label="Excellent"
)
```

#### 8. Rank Order
```python
api.create_rank_order_question(
    survey_id,
    "Rank your priorities:",
    items=["Price", "Quality", "Speed", "Support"]
)
```

#### 9. Net Promoter Score (NPS)
```python
api.create_nps_question(
    survey_id,
    "How likely are you to recommend us?"
)
```

#### 10. Descriptive Text
```python
api.create_descriptive_text(
    survey_id,
    "<h2>Welcome!</h2><p>Thank you for participating.</p>"
)
```

### Survey Management

#### List All Surveys
```python
surveys = api.list_surveys()
for survey in surveys:
    print(f"{survey['name']} - {survey['id']}")
```

#### Get Survey Details
```python
survey = api.get_survey(survey_id)
print(survey)
```

#### Update Survey Name
```python
api.update_survey_name(survey_id, "New Survey Name")
```

#### Delete Survey
```python
api.delete_survey(survey_id)
```

### Question Management

#### Update Question Text
```python
api.update_question_text(
    survey_id,
    question_id,
    "Updated question text"
)
```

#### Delete Question
```python
api.delete_question(survey_id, question_id)
```

#### Get Question Details
```python
question = api.get_question(survey_id, question_id)
print(question)
```

#### Get All Questions in Survey
```python
questions = api.get_survey_questions(survey_id)
for question in questions:
    print(question['QuestionText'])
```

### Block Management

#### Create New Block
```python
block = api.create_block(survey_id, "Demographics")
block_id = block['BlockID']
```

#### Get All Blocks
```python
blocks = api.get_blocks(survey_id)
```

### Display Logic (Conditional Questions)

Display logic allows you to show or hide questions based on respondent answers, creating dynamic, adaptive surveys.

**Important:** For display logic to work correctly:
1. Questions must be in **separate blocks** (blocks create automatic page breaks)
2. The source question must be answered before the conditional question is evaluated

#### Simple Display Logic
```python
# Show Q2 only if "Yes" (choice 1) is selected in Q1
api.add_display_logic(
    survey_id=survey_id,
    question_id="QID2",
    source_question_id="QID1",
    operator="Selected",
    choice_locator="q://QID1/SelectableChoice/1"
)
```

#### Numeric Comparisons
```python
# Show follow-up question if satisfaction score < 50
api.add_display_logic(
    survey_id=survey_id,
    question_id="QID4",
    source_question_id="QID3",  # Slider question
    operator="LessThan",
    value=50
)
```

#### Multiple Conditions (AND/OR)
```python
# Show Q6 only if both Product A AND Product B are selected in Q5
api.add_display_logic_multiple(
    survey_id=survey_id,
    question_id="QID6",
    conditions=[
        {
            "source_question_id": "QID5",
            "operator": "Selected",
            "choice_locator": "q://QID5/SelectableChoice/1"  # Product A
        },
        {
            "source_question_id": "QID5",
            "operator": "Selected",
            "choice_locator": "q://QID5/SelectableChoice/2"  # Product B
        }
    ],
    conjunction="AND"  # or "OR"
)
```

#### Helper Methods
```python
# Semantic alias for clarity
api.show_only_if(
    survey_id=survey_id,
    question_id="QID2",
    source_question_id="QID1",
    operator="Selected",
    choice_locator="q://QID1/SelectableChoice/1"
)

# Skip logic (inverse of display logic)
api.skip_if(
    survey_id=survey_id,
    question_id="QID3",
    source_question_id="QID2",
    operator="Selected",
    choice_locator="q://QID2/SelectableChoice/2"  # "No"
)
```

#### Supported Operators
- **Choice-based:** `Selected`, `NotSelected`, `Displayed`, `NotDisplayed`
- **Numeric:** `EqualTo`, `NotEqualTo`, `GreaterThan`, `LessThan`, `GreaterOrEqual`, `LessOrEqual`
- **Text:** `Contains`, `DoesNotContain`, `MatchesRegex`, `Empty`, `NotEmpty`

#### Get and Delete Display Logic
```python
# Get display logic for a question
logic = api.get_display_logic(survey_id, question_id)

# Remove display logic
api.delete_display_logic(survey_id, question_id)
```

### Embedded Data

#### Set Individual Embedded Data Field
```python
# Define a field that will receive values from URL parameters
api.set_embedded_data(survey_id, "customer_id", field_type="text")

# Set a field with a default value
api.set_embedded_data(survey_id, "source", field_type="text", value="direct")
```

#### Set Multiple Embedded Data Fields
```python
api.set_embedded_data_fields(
    survey_id,
    fields={
        "user_id": {"type": "text"},
        "department": {"type": "text"},
        "score": {"type": "number"},
        "signup_date": {"type": "date"}
    }
)
```

#### Dynamic Values (Random Numbers, Piped Text)
```python
# Set at START of flow (evaluated before questions)
api.set_embedded_data_fields(
    survey_id,
    fields={
        "lottery_number": {"type": "text", "value": "${rand://int/1:1000}"},
        "random_group": {"type": "text", "value": "${rand://int/1:3}"}
    },
    position="start"
)

# Capture question answers at END of flow
api.set_embedded_data_fields(
    survey_id,
    fields={
        "user_role": {"type": "text", "value": "${q://QID1/ChoiceGroup/SelectedChoices}"},
        "user_name": {"type": "text", "value": "${q://QID2/ChoiceTextEntryValue}"}
    },
    position="end"
)
```

#### Generate Personalized Survey URL
```python
url = api.get_survey_url_with_embedded_data(
    survey_id,
    embedded_data={
        "customer_id": "CUST-12345",
        "source": "email_campaign"
    }
)
# Returns: https://datacenter.qualtrics.com/jfe/form/SV_xxx?customer_id=CUST-12345&source=email_campaign
```

#### Get and Delete Embedded Data
```python
# Get all embedded data fields
fields = api.get_embedded_data(survey_id)

# Delete a field
api.delete_embedded_data(survey_id, "field_to_remove")
```

### Custom JavaScript

Add custom JavaScript to questions for advanced interactivity, timers, validation, and more.

#### Add Custom JavaScript to a Question
```python
# Add custom JavaScript to a question
api.add_question_javascript(
    survey_id,
    question_id,
    '''
    Qualtrics.SurveyEngine.addOnload(function() {
        console.log('Question loaded!');
    });

    Qualtrics.SurveyEngine.addOnReady(function() {
        // Manipulate the DOM
        var container = this.getQuestionContainer();
        container.style.backgroundColor = '#f5f5f5';
    });
    '''
)
```

#### Auto-Advance Questions
```python
# Auto-advance after 5 seconds (useful for timed displays)
api.add_auto_advance(survey_id, question_id, delay_ms=5000)
```

#### Countdown Timer Display
```python
# Add visible countdown timer that auto-advances
api.add_timer_display(
    survey_id, question_id,
    duration_seconds=30,
    auto_advance=True,
    timer_position='top'  # or 'bottom'
)
```

#### Custom Input Validation
```python
# Validate ZIP code format
api.add_input_validation(
    survey_id, question_id,
    regex=r"^\d{5}$",
    error_message="Please enter a valid 5-digit ZIP code"
)

# Validate email format
api.add_input_validation(
    survey_id, question_id,
    regex=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
    error_message="Please enter a valid email address"
)
```

#### Embed iframes (Videos, External Content)
```python
# Embed a YouTube video
api.add_iframe(
    survey_id, question_id,
    iframe_url="https://www.youtube.com/embed/VIDEO_ID",
    width="560px",
    height="315px",
    position="top"  # or 'bottom'
)
```

#### Modify Next Button
```python
# Change button text
api.add_next_button_modification(
    survey_id, question_id,
    button_text="Continue to Next Section"
)

# Hide button for 5 seconds then show
api.add_next_button_modification(
    survey_id, question_id,
    hide_button=True,
    show_after_ms=5000
)

# Style the button
api.add_next_button_modification(
    survey_id, question_id,
    button_text="Submit",
    custom_style="background-color: #4CAF50; color: white; font-weight: bold;"
)
```

#### Style Response Choices
```python
# Add custom styling to multiple choice options
api.add_choice_style(
    survey_id, question_id,
    background_color="#f5f5f5",
    border_radius="8px",
    hover_color="#e0e0e0",
    selected_color="#bbdefb"
)
```

#### Get and Remove JavaScript
```python
# Get JavaScript from a question
js = api.get_question_javascript(survey_id, question_id)

# Remove all JavaScript from a question
api.remove_question_javascript(survey_id, question_id)
```

## Running the Example

The `main.py` file contains a comprehensive example that creates a survey with all question types:

```bash
source venv/bin/activate
python main.py
```

This will:
1. Create a new survey
2. Add examples of all question types
3. Print the survey URL
4. Display the survey ID for further manipulation

## API Reference

### QualtricsAPI Class

#### Initialization
```python
api = QualtricsAPI(api_token: str, data_center: str)
```

#### Survey Operations
- `create_survey(survey_name, language="EN", project_category="CORE")` - Create a new survey
- `get_survey(survey_id)` - Get survey details
- `delete_survey(survey_id)` - Delete a survey
- `list_surveys()` - List all surveys
- `update_survey_name(survey_id, new_name)` - Update survey name
- `get_survey_url(survey_id)` - Get the public survey URL

#### Question Operations
- `create_multiple_choice_question(survey_id, question_text, choices, selector)` - Create MC question
- `create_text_entry_question(survey_id, question_text, text_type)` - Create text entry
- `create_matrix_question(survey_id, question_text, statements, scale_points)` - Create matrix
- `create_slider_question(survey_id, question_text, min_value, max_value, ...)` - Create slider
- `create_rank_order_question(survey_id, question_text, items)` - Create rank order
- `create_nps_question(survey_id, question_text)` - Create NPS question
- `create_descriptive_text(survey_id, text)` - Add descriptive text
- `update_question(survey_id, question_id, question_data)` - Update question
- `update_question_text(survey_id, question_id, new_text)` - Update question text
- `delete_question(survey_id, question_id)` - Delete question
- `get_question(survey_id, question_id)` - Get question details
- `get_survey_questions(survey_id)` - Get all questions

#### Block Operations
- `create_block(survey_id, block_name)` - Create a new block
- `get_blocks(survey_id)` - Get all blocks

#### Embedded Data Operations
- `set_embedded_data(survey_id, field_name, field_type, value, position)` - Set individual field
- `set_embedded_data_fields(survey_id, fields, position)` - Set multiple fields at once
- `get_embedded_data(survey_id)` - Get all embedded data fields
- `delete_embedded_data(survey_id, field_name)` - Delete a field
- `get_survey_url_with_embedded_data(survey_id, embedded_data)` - Generate personalized URL
- `get_survey_flow(survey_id)` - Get the survey flow structure

#### JavaScript Operations
- `add_question_javascript(survey_id, question_id, javascript_code, append)` - Add custom JavaScript
- `get_question_javascript(survey_id, question_id)` - Get JavaScript from a question
- `remove_question_javascript(survey_id, question_id)` - Remove all JavaScript
- `add_auto_advance(survey_id, question_id, delay_ms)` - Auto-advance after delay
- `add_timer_display(survey_id, question_id, duration_seconds, auto_advance, timer_position)` - Add countdown timer
- `add_input_validation(survey_id, question_id, regex, error_message)` - Add regex validation
- `add_iframe(survey_id, question_id, iframe_url, width, height, position)` - Embed iframe
- `add_next_button_modification(survey_id, question_id, button_text, hide_button, show_after_ms, custom_style)` - Modify next button
- `add_choice_style(survey_id, question_id, background_color, border_radius, hover_color, selected_color)` - Style choices

**Note:** All question creation methods accept an optional `block_id` parameter to specify which block to add the question to. See [docs/BLOCKS_GUIDE.md](docs/BLOCKS_GUIDE.md) for details.

## Question Type Reference

### Multiple Choice Selectors
- `"SAVR"` - Single Answer Vertical (Radio buttons)
- `"SAHR"` - Single Answer Horizontal
- `"MAVR"` - Multiple Answer Vertical (Checkboxes)
- `"MAHR"` - Multiple Answer Horizontal
- `"DL"` - Dropdown List

### Text Entry Types
- `"SL"` - Single Line
- `"ML"` - Multi-Line (Essay)
- `"Form"` - Form Field

## Error Handling

All methods will raise an `Exception` with descriptive error messages if the API request fails:

```python
try:
    survey = api.create_survey("My Survey")
except Exception as e:
    print(f"Error: {e}")
```

## Notes

- Your API credentials are loaded from the `.env` file
- All survey operations are performed directly on your Qualtrics account
- Survey IDs and Question IDs are returned by the API and needed for subsequent operations
- The module uses Qualtrics REST API v3

## License

This is a utility module for working with the Qualtrics API.

## Support

For Qualtrics API documentation, visit: https://api.qualtrics.com/
