"""
Test Slider Display Logic
Create a minimal test with slider and see what works
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from qualtrics_sdk import QualtricsAPI
import json

load_dotenv()
api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)

print("="*80)
print("SLIDER DISPLAY LOGIC TEST")
print("="*80)

# Create survey
print("\nCreating survey...")
survey = api.create_survey("Slider Logic Test")
sid = survey['SurveyID']
print(f"Survey ID: {sid}")

# Create blocks
print("\nCreating blocks...")
b1 = api.create_block(sid, "Slider Question")
b1_id = b1['BlockID']
b2 = api.create_block(sid, "Conditional Question")
b2_id = b2['BlockID']

# Create slider
print("\nCreating slider question...")
q1 = api.create_slider_question(
    sid,
    "On a scale of 0-100, how satisfied are you?",
    min_value=0,
    max_value=100,
    block_id=b1_id
)
q1_id = q1['QuestionID']
print(f"Slider created: {q1_id}")

# Get full slider structure
q1_full = api.get_question(sid, q1_id)
print("\nSlider Question Structure:")
print(f"  QuestionType: {q1_full['QuestionType']}")
print(f"  Selector: {q1_full['Selector']}")
print(f"  Choices: {json.dumps(q1_full.get('Choices', {}), indent=4)}")

# Create conditional question
print("\nCreating conditional question...")
q2 = api.create_text_entry_question(
    sid,
    "We're sorry to hear that. What could we improve?",
    text_type="ML",
    block_id=b2_id
)
q2_id = q2['QuestionID']
print(f"Conditional question created: {q2_id}")

# Add display logic
print("\nAdding display logic (show Q2 if slider < 50)...")
api.add_display_logic(
    survey_id=sid,
    question_id=q2_id,
    source_question_id=q1_id,
    operator="LessThan",
    value=50
)
print("✓ Display logic added")

# Get display logic
q2_full = api.get_question(sid, q2_id)
print("\n" + "="*80)
print("DISPLAY LOGIC STRUCTURE (PROGRAMMATIC)")
print("="*80)
print(json.dumps(q2_full.get('DisplayLogic', {}), indent=2))

# Extract condition
if 'DisplayLogic' in q2_full:
    dl = q2_full['DisplayLogic']
    if '0' in dl and '0' in dl['0']:
        condition = dl['0']['0']
        print("\n" + "-"*80)
        print("CONDITION FIELDS:")
        print("-"*80)
        for key, value in sorted(condition.items()):
            print(f"  {key:25s}: {value}")

print("\n" + "="*80)
print("TESTING INSTRUCTIONS")
print("="*80)
print(f"""
1. Test the programmatic version:
   {api.get_survey_url(sid)}

   - Set slider to 40 (< 50) → Q2 should appear
   - Set slider to 60 (> 50) → Q2 should NOT appear

2. If it doesn't work:
   a. Go to survey editor
   b. Click on Q2
   c. Look at Display Logic in left panel
   d. Take note of what fields you see
   e. Manually edit and re-save the display logic

3. Run comparison script:
   python examples/compare_logic.py

   Survey ID: {sid}
   Question ID: {q2_id}

4. Compare the structures and tell me what's different!

Survey ID: {sid}
Q1 (Slider): {q1_id}
Q2 (Conditional): {q2_id}
""")

response = input("\nDelete test survey? (y/n): ").strip().lower()
if response == 'y':
    api.delete_survey(sid)
    print("✓ Survey deleted")
else:
    print("Survey kept for testing")
