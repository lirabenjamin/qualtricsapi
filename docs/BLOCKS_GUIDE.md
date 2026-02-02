# Working with Blocks in Qualtrics

## Overview

Qualtrics surveys are organized into **blocks**. Each block is a section that contains multiple questions. Blocks are useful for:

- Organizing related questions together
- Controlling survey flow and randomization
- Creating different paths through your survey
- Making surveys easier to maintain and navigate

## Creating Blocks

Create a new block in your survey:

```python
block = api.create_block(survey_id, "Demographics")
block_id = block['BlockID']
print(f"Block created: {block_id}")
```

## Adding Questions to Specific Blocks

All question creation methods support an optional `block_id` parameter that lets you specify which block to add the question to:

```python
# Add question to specific block
api.create_multiple_choice_question(
    survey_id,
    "What is your age group?",
    choices=["18-24", "25-34", "35-44", "45+"],
    block_id=block_id  # ← Specify the block
)
```

### Without block_id

If you don't specify `block_id`, questions are added to the default block:

```python
# Goes to default block
api.create_multiple_choice_question(
    survey_id,
    "What is your role?",
    choices=["Student", "Faculty", "Staff"]
)
```

## Complete Example: Multi-Section Survey

Here's a complete example showing how to create a survey with multiple organized sections:

```python
import os
from dotenv import load_dotenv
from qualtrics_sdk import QualtricsAPI

load_dotenv()
api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)

# Create survey
survey = api.create_survey("Customer Feedback Survey")
sid = survey['SurveyID']

# Get default block ID
blocks = api.get_blocks(sid)
default_block_id = None
for bid, binfo in blocks['Elements'].items():
    if binfo['Type'] == 'Default':
        default_block_id = bid
        break

# Add welcome to default block
api.create_descriptive_text(
    sid,
    "<h2>Welcome!</h2><p>Thank you for your feedback.</p>",
    block_id=default_block_id
)

# Create Demographics block
demo_block = api.create_block(sid, "Demographics")
demo_block_id = demo_block['BlockID']

# Add demographics questions
api.create_multiple_choice_question(
    sid,
    "What is your age group?",
    choices=["18-24", "25-34", "35-44", "45+"],
    selector="DL",
    block_id=demo_block_id
)

api.create_multiple_choice_question(
    sid,
    "How often do you use our service?",
    choices=["Daily", "Weekly", "Monthly", "Rarely"],
    block_id=demo_block_id
)

# Create Feedback block
feedback_block = api.create_block(sid, "Your Feedback")
feedback_block_id = feedback_block['BlockID']

# Add feedback questions
api.create_matrix_question(
    sid,
    "Please rate the following:",
    statements=["Quality", "Service", "Value"],
    scale_points=["Poor", "Fair", "Good", "Excellent"],
    block_id=feedback_block_id
)

api.create_nps_question(
    sid,
    "How likely are you to recommend us?",
    block_id=feedback_block_id
)

api.create_text_entry_question(
    sid,
    "What can we improve?",
    text_type="ML",
    block_id=feedback_block_id
)

print(f"Survey created: {api.get_survey_url(sid)}")
```

## Getting Block Information

Retrieve all blocks and their contents:

```python
blocks = api.get_blocks(survey_id)

for block_id, block_info in blocks['Elements'].items():
    block_name = block_info.get('Description', 'Default Block')
    block_type = block_info['Type']
    num_questions = len(block_info.get('BlockElements', []))

    print(f"{block_name}:")
    print(f"  ID: {block_id}")
    print(f"  Type: {block_type}")
    print(f"  Questions: {num_questions}")
```

## Block Types

Qualtrics surveys have different block types:

- **Default**: The initial block created with every survey
- **Standard**: Regular blocks you create
- **Trash**: Holds deleted questions (can be recovered)

## All Question Types Support block_id

Every question creation method accepts the `block_id` parameter:

```python
# Multiple choice
api.create_multiple_choice_question(..., block_id=block_id)

# Text entry
api.create_text_entry_question(..., block_id=block_id)

# Matrix/Likert
api.create_matrix_question(..., block_id=block_id)

# Slider
api.create_slider_question(..., block_id=block_id)

# Rank order
api.create_rank_order_question(..., block_id=block_id)

# NPS
api.create_nps_question(..., block_id=block_id)

# Descriptive text
api.create_descriptive_text(..., block_id=block_id)
```

## Best Practices

### 1. Plan Your Structure

Before creating questions, plan your survey structure:

```python
# Define your blocks upfront
blocks_plan = {
    'welcome': 'Default',
    'demographics': 'About You',
    'experience': 'Your Experience',
    'feedback': 'Final Thoughts'
}
```

### 2. Store Block IDs

Keep track of block IDs for reference:

```python
# Create and store block IDs
blocks = {}
blocks['demographics'] = api.create_block(sid, "Demographics")['BlockID']
blocks['feedback'] = api.create_block(sid, "Feedback")['BlockID']

# Use them later
api.create_multiple_choice_question(
    sid, "Age?", ["18-24", "25+"],
    block_id=blocks['demographics']
)
```

### 3. Use Descriptive Names

Make block names clear and descriptive:

```python
# Good block names
api.create_block(sid, "Part 1: Demographics")
api.create_block(sid, "Part 2: Experience Questions")
api.create_block(sid, "Part 3: Open Feedback")

# Less helpful
api.create_block(sid, "Block 1")
api.create_block(sid, "Questions")
```

### 4. Add Section Headers

Use descriptive text to introduce each block:

```python
api.create_descriptive_text(
    sid,
    "<h3>Part 1: About You</h3>"
    "<p>First, we'd like to know a bit about you.</p>",
    block_id=demographics_block_id
)
```

### 5. Group Related Questions

Keep related questions in the same block:

```python
# Demographics block
demo_block = api.create_block(sid, "Demographics")['BlockID']
api.create_multiple_choice_question(sid, "Age?", [...], block_id=demo_block)
api.create_multiple_choice_question(sid, "Role?", [...], block_id=demo_block)
api.create_multiple_choice_question(sid, "Department?", [...], block_id=demo_block)

# Satisfaction block
sat_block = api.create_block(sid, "Satisfaction")['BlockID']
api.create_matrix_question(sid, "Rate...", [...], block_id=sat_block)
api.create_nps_question(sid, block_id=sat_block)
```

## Common Patterns

### Pattern 1: Welcome + Sections + Thank You

```python
# Welcome in default block
default_id = get_default_block_id(survey_id)
api.create_descriptive_text(sid, "<h2>Welcome!</h2>", block_id=default_id)

# Multiple content sections
for section_name in ["Demographics", "Experience", "Feedback"]:
    block_id = api.create_block(sid, section_name)['BlockID']
    # Add questions to block_id...

# Thank you at the end
api.create_descriptive_text(sid, "<h2>Thank You!</h2>")
```

### Pattern 2: Conditional Sections

```python
# Main questions in default block
# ...

# Optional section for specific respondents
advanced_block = api.create_block(sid, "Advanced Questions")['BlockID']
# Add advanced questions to advanced_block...
# Use Survey Flow in Qualtrics UI to add display logic
```

### Pattern 3: Randomized Blocks

```python
# Create multiple similar blocks
for i in range(1, 4):
    block = api.create_block(sid, f"Scenario {i}")
    block_id = block['BlockID']
    # Add questions to this block...
# Use Survey Flow in Qualtrics UI to randomize block order
```

## Advanced: Survey Flow

While blocks organize your questions, the **Survey Flow** in Qualtrics controls:

- The order blocks are presented
- Display logic (show/hide blocks based on answers)
- Randomization of blocks
- Branch logic

After creating your blocks with the API, you can configure Survey Flow in the Qualtrics web interface:

1. Go to your survey in Qualtrics
2. Click "Survey Flow" in the left sidebar
3. Drag and drop blocks to reorder
4. Add display logic, randomization, etc.
5. Save your changes

## Helper Function: Get Default Block ID

Since you often need the default block ID, here's a helper:

```python
def get_default_block_id(api, survey_id):
    """Get the ID of the default block"""
    blocks = api.get_blocks(survey_id)
    for block_id, block_info in blocks['Elements'].items():
        if block_info['Type'] == 'Default':
            return block_id
    return None

# Usage
default_id = get_default_block_id(api, survey_id)
api.create_descriptive_text(sid, "Welcome!", block_id=default_id)
```

## See Also

- [CODE_ORGANIZATION.md](CODE_ORGANIZATION.md) - Overall SDK structure
- [ROADMAP.md](ROADMAP.md) - Future block-related features (flow, randomization)
- [Qualtrics API Documentation](https://api.qualtrics.com/) - Official API docs
- [examples/test_block_targeting.py](../examples/test_block_targeting.py) - Working example
