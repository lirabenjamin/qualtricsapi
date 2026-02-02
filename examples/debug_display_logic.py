"""
Debug Display Logic
Compare programmatic vs manual display logic structures
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
print("DISPLAY LOGIC DIAGNOSTIC")
print("="*80)

# Create a minimal test survey
print("\nCreating test survey...")
survey = api.create_survey("Display Logic Debug Test")
sid = survey['SurveyID']
print(f"Survey created: {sid}")

# Create two simple questions in separate blocks
print("\nCreating Block 1...")
block1 = api.create_block(sid, "Block 1")
block1_id = block1['BlockID']

print("Creating Q1 (source question)...")
q1 = api.create_multiple_choice_question(
    sid,
    "Do you want to see Q2?",
    choices=["Yes", "No"],
    block_id=block1_id
)
q1_id = q1['QuestionID']
print(f"Q1 created: {q1_id}")

print("\nCreating Block 2...")
block2 = api.create_block(sid, "Block 2")
block2_id = block2['BlockID']

print("Creating Q2 (conditional question)...")
q2 = api.create_text_entry_question(
    sid,
    "You said yes! Please tell us more:",
    text_type="SL",
    block_id=block2_id
)
q2_id = q2['QuestionID']
print(f"Q2 created: {q2_id}")

# Get Q1 details to see the choices structure
print("\n" + "="*80)
print("Q1 STRUCTURE (SOURCE QUESTION)")
print("="*80)
q1_data = api.get_question(sid, q1_id)
print(f"\nQuestion ID: {q1_id}")
print(f"Question Type: {q1_data['QuestionType']}")
print(f"Selector: {q1_data['Selector']}")
print(f"\nChoices:")
print(json.dumps(q1_data.get('Choices', {}), indent=2))
print(f"\nChoiceOrder:")
print(json.dumps(q1_data.get('ChoiceOrder', []), indent=2))

# Add display logic
print("\n" + "="*80)
print("ADDING DISPLAY LOGIC")
print("="*80)
choice_locator = f"q://{q1_id}/SelectableChoice/1"
print(f"\nChoice locator: {choice_locator}")
print(f"Operator: Selected")

api.add_display_logic(
    survey_id=sid,
    question_id=q2_id,
    source_question_id=q1_id,
    operator="Selected",
    choice_locator=choice_locator
)
print("✓ Display logic added")

# Get Q2 with display logic
print("\n" + "="*80)
print("Q2 STRUCTURE (WITH DISPLAY LOGIC)")
print("="*80)
q2_data = api.get_question(sid, q2_id)
print(f"\nQuestion ID: {q2_id}")
print(f"\nFull DisplayLogic structure:")
print(json.dumps(q2_data.get('DisplayLogic', {}), indent=2))

# Extract the condition details
if 'DisplayLogic' in q2_data:
    dl = q2_data['DisplayLogic']
    if '0' in dl and '0' in dl['0']:
        condition = dl['0']['0']
        print("\n" + "-"*80)
        print("CONDITION DETAILS:")
        print("-"*80)
        for key, value in condition.items():
            print(f"{key}: {value}")

print("\n" + "="*80)
print("TESTING INSTRUCTIONS")
print("="*80)
print(f"""
1. Open survey in browser:
   {api.get_survey_url(sid)}

2. Test the display logic:
   - Select "Yes" in Q1 → Q2 should appear
   - Select "No" in Q1 → Q2 should NOT appear

3. If it doesn't work:
   - Go to survey editor
   - Click on Q2
   - Check "Display Logic" in left panel
   - Note what's different from the structure above
   - Edit and re-save the logic in the UI
   - Then use this script to get Q2 again and compare

4. To get Q2 structure after manual edit:
   python -c "from qualtrics_sdk import QualtricsAPI; import os; from dotenv import load_dotenv; import json; load_dotenv(); api = QualtricsAPI(os.getenv('QUALTRICS_API_TOKEN'), os.getenv('QUALTRICS_DATA_CENTER')); q2 = api.get_question('{sid}', '{q2_id}'); print(json.dumps(q2.get('DisplayLogic', {{}}), indent=2))"

Survey ID: {sid}
Q1 ID: {q1_id}
Q2 ID: {q2_id}
""")

print("\nWould you like to delete this test survey? (y/n): ", end='')
response = input().strip().lower()
if response == 'y':
    api.delete_survey(sid)
    print("✓ Survey deleted")
else:
    print("Survey kept for testing")
