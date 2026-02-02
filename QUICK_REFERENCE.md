# Qualtrics API Quick Reference

## Setup

```python
import os
from dotenv import load_dotenv
from qualtrics_api import QualtricsAPI

# Load from .env file
load_dotenv()

api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)
```

## Common Operations

### Create a Survey
```python
survey = api.create_survey("My Survey Name")
survey_id = survey['SurveyID']
```

### Delete a Survey
```python
api.delete_survey(survey_id)
```

### List All Surveys
```python
surveys = api.list_surveys()
for survey in surveys:
    print(f"{survey['name']} - {survey['id']}")
```

### Get Survey URL
```python
url = api.get_survey_url(survey_id)
```

## Question Types Cheat Sheet

### 1. Radio Buttons (Single Choice)
```python
api.create_multiple_choice_question(
    survey_id,
    "What is your role?",
    choices=["Student", "Faculty", "Staff"],
    selector="SAVR"  # Vertical
)
```

### 2. Dropdown List
```python
api.create_multiple_choice_question(
    survey_id,
    "Select your department:",
    choices=["Engineering", "Business", "Arts"],
    selector="DL"
)
```

### 3. Single-Line Text
```python
api.create_text_entry_question(
    survey_id,
    "What is your email?",
    text_type="SL"
)
```

### 4. Essay (Multi-Line Text)
```python
api.create_text_entry_question(
    survey_id,
    "Please share your feedback:",
    text_type="ML"
)
```

### 5. Likert Scale / Matrix
```python
api.create_matrix_question(
    survey_id,
    "Rate your satisfaction:",
    statements=["Quality", "Service", "Value"],
    scale_points=["Poor", "Fair", "Good", "Excellent"]
)
```

### 6. Slider
```python
api.create_slider_question(
    survey_id,
    "Rate your experience:",
    min_value=0,
    max_value=100
)
```

### 7. Rank Order
```python
api.create_rank_order_question(
    survey_id,
    "Rank your priorities:",
    items=["Price", "Quality", "Speed"]
)
```

### 8. Net Promoter Score (NPS)
```python
api.create_nps_question(
    survey_id,
    "How likely are you to recommend us?"
)
```

### 9. Descriptive Text / Instructions
```python
api.create_descriptive_text(
    survey_id,
    "<h2>Welcome!</h2><p>Please answer all questions.</p>"
)
```

## Question Management

### Update Question Text
```python
api.update_question_text(survey_id, question_id, "New text")
```

### Delete Question
```python
api.delete_question(survey_id, question_id)
```

### Get Question Details
```python
question = api.get_question(survey_id, question_id)
```

### Get All Questions
```python
questions = api.get_survey_questions(survey_id)
```

## Selector Options for Multiple Choice

- `"SAVR"` - Single Answer Vertical (Radio - Vertical)
- `"SAHR"` - Single Answer Horizontal (Radio - Horizontal)
- `"DL"` - Dropdown List
- `"MAVR"` - Multiple Answer Vertical (Checkboxes - use `allow_multiple=True`)
- `"MAHR"` - Multiple Answer Horizontal (Checkboxes - use `allow_multiple=True`)

## Text Entry Types

- `"SL"` - Single Line
- `"ML"` - Multi-Line (Essay)
- `"Form"` - Form Field

## Error Handling

```python
try:
    survey = api.create_survey("My Survey")
    survey_id = survey['SurveyID']
except Exception as e:
    print(f"Error: {e}")
```

## Complete Example: Build a Customer Feedback Survey

```python
import os
from dotenv import load_dotenv
from qualtrics_api import QualtricsAPI

# Load credentials
load_dotenv()

api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)

# Create survey
survey = api.create_survey("Customer Feedback Survey")
sid = survey['SurveyID']

# Add welcome message
api.create_descriptive_text(sid, "<h2>Welcome!</h2><p>Your feedback matters.</p>")

# Add demographic question
api.create_multiple_choice_question(
    sid, "What is your age group?",
    choices=["18-24", "25-34", "35-44", "45-54", "55+"],
    selector="DL"
)

# Add satisfaction matrix
api.create_matrix_question(
    sid, "Rate your satisfaction:",
    statements=["Product Quality", "Customer Service", "Value for Money"],
    scale_points=["Very Poor", "Poor", "Fair", "Good", "Excellent"]
)

# Add NPS
api.create_nps_question(sid)

# Add open feedback
api.create_text_entry_question(
    sid, "Additional comments:",
    text_type="ML"
)

# Get survey URL
print(f"Survey created: {api.get_survey_url(sid)}")
```

## Tips

1. **DataExportTag**: Some question types require it - the API will auto-generate if not provided
2. **Question IDs**: Returned when you create questions - save them if you need to update/delete later
3. **Survey Testing**: Always test your survey after creation using the returned URL
4. **Batch Operations**: You can create multiple surveys/questions in a loop
5. **Error Messages**: The API provides detailed validation errors - read them carefully

## File Structure

```
qualtricsapi/
├── qualtrics_api.py      # Main API module
├── main.py               # Example with all question types
├── .env                  # Your credentials
├── requirements.txt      # Dependencies
├── README.md             # Full documentation
└── QUICK_REFERENCE.md    # This file
```

## Need Help?

- Full API docs: See [README.md](README.md)
- Qualtrics API docs: https://api.qualtrics.com/
- Example code: See [main.py](main.py)
