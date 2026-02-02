# Display Logic Guide

This guide covers how to use the conditional display / display logic features in the Qualtrics SDK.

## Overview

Display logic allows you to dynamically show or hide survey questions based on respondent answers, enabling adaptive survey experiences. This feature supports:

- **Skip Logic**: Omit irrelevant questions following specific answers
- **Branching**: Route respondents through different survey paths
- **Screening**: Display follow-up items only to qualified participants
- **Personalization**: Tailor survey flow to individual responses
- **Complex Logic**: Support combined conditions with AND/OR operators

## Quick Start

```python
from qualtrics_sdk import QualtricsAPI

api = QualtricsAPI(api_token="your_token", data_center="your_datacenter.qualtrics.com")

# Create a survey with questions
survey = api.create_survey("My Survey")
sid = survey['SurveyID']

q1 = api.create_multiple_choice_question(sid, "Continue?", ["Yes", "No"])
q2 = api.create_text_entry_question(sid, "Please elaborate:")

# Show Q2 only if "Yes" selected in Q1
api.add_display_logic(
    survey_id=sid,
    question_id=q2['QuestionID'],
    source_question_id=q1['QuestionID'],
    operator="Selected",
    choice_locator=f"q://{q1['QuestionID']}/SelectableChoice/1"  # "Yes" is choice 1
)
```

## Available Methods

### Core Methods

#### `add_display_logic()`

Add display logic with a single condition.

```python
api.add_display_logic(
    survey_id: str,
    question_id: str,          # Question to show/hide
    source_question_id: str,   # Question to evaluate
    operator: str,             # Comparison operator
    choice_locator: str = None,# For multi-choice questions
    value: Any = None          # For comparison operators
)
```

**Example - Show if choice selected:**
```python
api.add_display_logic(
    survey_id=sid,
    question_id="QID2",
    source_question_id="QID1",
    operator="Selected",
    choice_locator="q://QID1/SelectableChoice/1"
)
```

**Example - Show if value greater than threshold:**
```python
api.add_display_logic(
    survey_id=sid,
    question_id="QID_improvement",
    source_question_id="QID_rating",
    operator="LessThan",
    value=50
)
```

#### `add_display_logic_multiple()`

Add display logic with multiple conditions combined by AND/OR.

```python
api.add_display_logic_multiple(
    survey_id: str,
    question_id: str,
    conditions: List[Dict],    # List of condition dictionaries
    conjunction: str = "AND"   # "AND" or "OR"
)
```

**Example - Show if both conditions met:**
```python
api.add_display_logic_multiple(
    survey_id=sid,
    question_id="QID_comparison",
    conditions=[
        {
            "source_question_id": "QID_products",
            "operator": "Selected",
            "choice_locator": "q://QID_products/SelectableChoice/1"  # Product A
        },
        {
            "source_question_id": "QID_products",
            "operator": "Selected",
            "choice_locator": "q://QID_products/SelectableChoice/2"  # Product B
        }
    ],
    conjunction="AND"
)
```

**Example - Show if any condition met:**
```python
api.add_display_logic_multiple(
    survey_id=sid,
    question_id="QID_discount_info",
    conditions=[
        {"source_question_id": "QID_age", "operator": "LessThan", "value": 25},
        {"source_question_id": "QID_status", "operator": "Selected",
         "choice_locator": "q://QID_status/SelectableChoice/3"}  # "Student"
    ],
    conjunction="OR"
)
```

### Helper Methods

#### `show_only_if()`

Semantic alias for `add_display_logic()` - makes code more readable.

```python
api.show_only_if(
    survey_id=sid,
    question_id="QID_followup",
    source_question_id="QID_interested",
    operator="Selected",
    choice_locator="q://QID_interested/SelectableChoice/1"  # "Yes"
)
```

#### `skip_if()`

Skip a question when condition is met (inverts the logic).

```python
# Skip the detailed question if user selects "No, keep it brief"
api.skip_if(
    survey_id=sid,
    question_id="QID_detailed",
    source_question_id="QID_preference",
    operator="Selected",
    choice_locator="q://QID_preference/SelectableChoice/2"  # "No" option
)
```

### Embedded Data Logic

#### `add_embedded_data_logic()`

Show questions based on embedded data values passed to the survey.

```python
# Show premium-only question if user_type is "premium"
api.add_embedded_data_logic(
    survey_id=sid,
    question_id="QID_premium_features",
    field_name="user_type",
    operator="EqualTo",
    value="premium"
)
```

### Management Methods

#### `get_display_logic()`

Retrieve the display logic for a question.

```python
logic = api.get_display_logic(survey_id, question_id)
if logic:
    print(f"Display logic type: {logic['Type']}")
else:
    print("No display logic set")
```

#### `delete_display_logic()`

Remove display logic from a question.

```python
api.delete_display_logic(survey_id, question_id)
```

## Supported Operators

| Operator | Description | Use Case |
|----------|-------------|----------|
| `Selected` | Choice is selected | Multiple choice questions |
| `NotSelected` | Choice is not selected | Inverse selection |
| `EqualTo` | Value equals | Text/numeric comparison |
| `NotEqualTo` | Value does not equal | Exclusion logic |
| `GreaterThan` | Value is greater than | Numeric thresholds |
| `LessThan` | Value is less than | Numeric thresholds |
| `GreaterOrEqual` | Value is >= | Inclusive thresholds |
| `LessOrEqual` | Value is <= | Inclusive thresholds |
| `Contains` | Value contains substring | Text matching |
| `DoesNotContain` | Value doesn't contain substring | Text exclusion |
| `MatchesRegex` | Value matches regex pattern | Advanced text matching |
| `Empty` | Answer is empty/blank | Completion checks |
| `NotEmpty` | Answer is not empty | Required answers |
| `Displayed` | Question was displayed | Flow logic |
| `NotDisplayed` | Question was not displayed | Flow logic |

## Choice Locators

For multiple choice questions, you need to specify which choice to check using a choice locator:

```
q://QUESTION_ID/SelectableChoice/CHOICE_NUMBER
```

- `QUESTION_ID`: The question ID (e.g., QID1, QID2)
- `CHOICE_NUMBER`: 1-indexed choice number

**Example:**
```python
# For a question with choices: ["Yes", "No", "Maybe"]
# "Yes" = SelectableChoice/1
# "No" = SelectableChoice/2
# "Maybe" = SelectableChoice/3

choice_locator = f"q://{question_id}/SelectableChoice/1"  # "Yes"
```

## Common Use Cases

### 1. Screening Questions

Show follow-up only for qualified respondents:

```python
# Q1: "Are you 18 or older?"
q1 = api.create_multiple_choice_question(sid, "Are you 18 or older?", ["Yes", "No"])

# Q2: Main survey (only for 18+)
q2 = api.create_matrix_question(sid, "Rate your experience:", ...)

api.show_only_if(
    survey_id=sid,
    question_id=q2['QuestionID'],
    source_question_id=q1['QuestionID'],
    operator="Selected",
    choice_locator=f"q://{q1['QuestionID']}/SelectableChoice/1"
)
```

### 2. Satisfaction Follow-up

Ask for improvement suggestions only for dissatisfied users:

```python
# Q1: Satisfaction slider (0-100)
q1 = api.create_slider_question(sid, "How satisfied are you?", 0, 100)

# Q2: Improvement question
q2 = api.create_text_entry_question(sid, "How can we improve?", text_type="ML")

api.show_only_if(
    survey_id=sid,
    question_id=q2['QuestionID'],
    source_question_id=q1['QuestionID'],
    operator="LessThan",
    value=50
)
```

### 3. Product Comparison

Show comparison only when multiple products are used:

```python
# Q1: Multi-select product usage
q1 = api.create_multiple_choice_question(
    sid, "Which products do you use?",
    ["Product A", "Product B", "Product C"],
    selector="MAVR"  # Multiple answer
)

# Q2: Comparison matrix
q2 = api.create_matrix_question(sid, "Compare products:", ...)

api.add_display_logic_multiple(
    survey_id=sid,
    question_id=q2['QuestionID'],
    conditions=[
        {
            "source_question_id": q1['QuestionID'],
            "operator": "Selected",
            "choice_locator": f"q://{q1['QuestionID']}/SelectableChoice/1"
        },
        {
            "source_question_id": q1['QuestionID'],
            "operator": "Selected",
            "choice_locator": f"q://{q1['QuestionID']}/SelectableChoice/2"
        }
    ],
    conjunction="AND"
)
```

### 4. Personalized by User Type

Show different questions based on embedded data:

```python
# Premium users see advanced features question
q_premium = api.create_matrix_question(sid, "Rate premium features:", ...)
api.add_embedded_data_logic(
    survey_id=sid,
    question_id=q_premium['QuestionID'],
    field_name="user_tier",
    operator="EqualTo",
    value="premium"
)

# Free users see upgrade interest question
q_free = api.create_multiple_choice_question(
    sid, "Interested in upgrading?", ["Yes", "No", "Maybe"]
)
api.add_embedded_data_logic(
    survey_id=sid,
    question_id=q_free['QuestionID'],
    field_name="user_tier",
    operator="EqualTo",
    value="free"
)
```

## Running the Example

A complete working example is provided in `examples/display_logic_example.py`:

```bash
# Set up credentials in .env file first
cd examples
python display_logic_example.py
```

This creates a survey demonstrating:
- Simple display logic (show if choice selected)
- Numeric comparison (show if value < threshold)
- Multiple conditions with AND conjunction
- Getting and verifying display logic

## Testing

Unit tests are available in `tests/test_display_logic.py`:

```bash
# Run all display logic tests
pytest tests/test_display_logic.py -v

# Run with coverage
pytest tests/test_display_logic.py -v --cov=qualtrics_sdk.core.display_logic
```

## Troubleshooting

### Display logic not working?

1. **Verify question IDs**: Ensure you're using the correct QID values
2. **Check choice locators**: Choice numbers are 1-indexed
3. **Verify the survey**: Open in Qualtrics to see if logic was applied
4. **Check API response**: The methods raise exceptions on failure

### Common errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid operator` | Typo in operator name | Use exact operator from list above |
| `Failed to add display logic` | API rejection | Check question IDs exist |
| `conjunction must be 'AND' or 'OR'` | Wrong conjunction value | Use uppercase AND or OR |

## API Reference

For complete API documentation, see the docstrings in `qualtrics_sdk/core/display_logic.py`.
