"""
Test: Block Targeting with block_id Parameter
Tests adding questions to specific blocks using the blockId query parameter
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from qualtrics_sdk import QualtricsAPI

load_dotenv()
api = QualtricsAPI(
    api_token=os.getenv('QUALTRICS_API_TOKEN'),
    data_center=os.getenv('QUALTRICS_DATA_CENTER')
)

# Create survey
print("Creating survey...")
survey = api.create_survey("Block Targeting Test")
sid = survey['SurveyID']
print(f"✓ Survey: {sid}")

# Get default block
blocks = api.get_blocks(sid)
default_block_id = None
for bid, binfo in blocks['Elements'].items():
    if binfo['Type'] == 'Default':
        default_block_id = bid
        break
print(f"✓ Default block: {default_block_id}")

# Create new blocks
print("\nCreating blocks...")
demo_block = api.create_block(sid, "Demographics")
demo_block_id = demo_block['BlockID']
print(f"✓ Demographics block: {demo_block_id}")

feedback_block = api.create_block(sid, "Feedback")
feedback_block_id = feedback_block['BlockID']
print(f"✓ Feedback block: {feedback_block_id}")

# Add questions to specific blocks
print("\n" + "="*60)
print("Adding questions to specific blocks using block_id parameter")
print("="*60)

print("\n1. Adding to DEFAULT block...")
q1 = api.create_multiple_choice_question(
    sid,
    "Welcome! Are you ready to start?",
    choices=["Yes", "No"],
    block_id=default_block_id
)
print(f"   ✓ Question created: {q1['QuestionID']}")

print("\n2. Adding to DEMOGRAPHICS block...")
q2 = api.create_multiple_choice_question(
    sid,
    "What is your age group?",
    choices=["18-24", "25-34", "35-44", "45+"],
    selector="DL",
    block_id=demo_block_id
)
print(f"   ✓ Question created: {q2['QuestionID']}")

q3 = api.create_multiple_choice_question(
    sid,
    "What is your role?",
    choices=["Student", "Faculty", "Staff", "Other"],
    block_id=demo_block_id
)
print(f"   ✓ Question created: {q3['QuestionID']}")

print("\n3. Adding to FEEDBACK block...")
q4 = api.create_matrix_question(
    sid,
    "Rate your satisfaction:",
    statements=["Quality", "Service"],
    scale_points=["Poor", "Fair", "Good", "Excellent"],
    block_id=feedback_block_id
)
print(f"   ✓ Question created: {q4['QuestionID']}")

q5 = api.create_text_entry_question(
    sid,
    "Additional comments:",
    text_type="ML",
    block_id=feedback_block_id
)
print(f"   ✓ Question created: {q5['QuestionID']}")

# Check final structure
print("\n" + "="*60)
print("FINAL SURVEY STRUCTURE")
print("="*60)

blocks = api.get_blocks(sid)
for bid, binfo in blocks['Elements'].items():
    desc = binfo.get('Description', 'Default Block')
    btype = binfo['Type']
    num = len(binfo.get('BlockElements', []))

    if btype != 'Trash':
        print(f"\n{desc}:")
        print(f"  ID: {bid}")
        print(f"  Type: {btype}")
        print(f"  Questions: {num}")

print("\n" + "="*60)
print(f"\nSurvey URL: {api.get_survey_url(sid)}")
print(f"Survey ID: {sid}")
print("\nOpen the survey to verify questions are in the correct blocks!")
