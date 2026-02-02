"""
Example: Survey Randomization Features
Demonstrates block, question, and choice randomization capabilities
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
print("Creating survey for randomization demo...")
survey = api.create_survey("Randomization Demo Survey")
sid = survey['SurveyID']
print(f"✓ Survey: {sid}")

# Create blocks for randomization
print("\nCreating blocks...")
block1 = api.create_block(sid, "Section A - Products")
block1_id = block1['BlockID']
print(f"✓ Block 1: {block1_id}")

block2 = api.create_block(sid, "Section B - Services")
block2_id = block2['BlockID']
print(f"✓ Block 2: {block2_id}")

block3 = api.create_block(sid, "Section C - Experience")
block3_id = block3['BlockID']
print(f"✓ Block 3: {block3_id}")

# Add questions to each block
print("\nAdding questions to blocks...")

# Block 1 questions
q1 = api.create_multiple_choice_question(
    sid,
    "How satisfied are you with our products?",
    choices=["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"],
    block_id=block1_id
)
print(f"✓ Q1 added to Block 1: {q1['QuestionID']}")

q2 = api.create_multiple_choice_question(
    sid,
    "Which product features do you use most?",
    choices=["Feature A", "Feature B", "Feature C", "Feature D", "Other"],
    allow_multiple=True,
    block_id=block1_id
)
print(f"✓ Q2 added to Block 1: {q2['QuestionID']}")

# Block 2 questions
q3 = api.create_matrix_question(
    sid,
    "Rate our services:",
    statements=["Support Quality", "Response Time", "Expertise"],
    scale_points=["Poor", "Fair", "Good", "Excellent"],
    block_id=block2_id
)
print(f"✓ Q3 added to Block 2: {q3['QuestionID']}")

# Block 3 questions
q4 = api.create_multiple_choice_question(
    sid,
    "How likely are you to recommend us?",
    choices=["Extremely Likely", "Likely", "Neutral", "Unlikely", "Extremely Unlikely", "Not Applicable"],
    block_id=block3_id
)
print(f"✓ Q4 added to Block 3: {q4['QuestionID']}")

# ===========================================
# RANDOMIZATION DEMOS
# ===========================================

print("\n" + "="*60)
print("RANDOMIZATION EXAMPLES")
print("="*60)

# Example 1: Block-level randomization
print("\n1. BLOCK RANDOMIZATION")
print("-" * 40)
print("Randomizing blocks with even presentation...")
try:
    result = api.randomize_blocks(
        sid,
        block_ids=[block1_id, block2_id, block3_id],
        evenly_present=True
    )
    print("✓ Block randomization enabled!")
    print("  - Blocks will be presented in random order")
    print("  - Even presentation ensures balanced distribution")
except Exception as e:
    print(f"  Note: {e}")

# Example 2: Question-level randomization
print("\n2. QUESTION RANDOMIZATION")
print("-" * 40)
print(f"Randomizing questions in Block 1 ({block1_id})...")
try:
    result = api.randomize_questions_in_block(
        sid,
        block_id=block1_id,
        randomize=True
    )
    print("✓ Question randomization enabled for Block 1!")
    print("  - Questions will appear in random order")
except Exception as e:
    print(f"  Note: {e}")

# Example 3: Choice-level randomization
print("\n3. CHOICE RANDOMIZATION")
print("-" * 40)
print(f"Randomizing choices for Q4 ({q4['QuestionID']}) with anchor...")
try:
    result = api.randomize_question_choices(
        sid,
        question_id=q4['QuestionID'],
        randomize=True,
        anchor_last=True  # Keep "Not Applicable" at the end
    )
    print("✓ Choice randomization enabled!")
    print("  - Choices will be randomized")
    print("  - Last choice ('Not Applicable') is anchored")
except Exception as e:
    print(f"  Note: {e}")

# Example 4: Subset randomization
print("\n4. SUBSET RANDOMIZATION (showing partial questions)")
print("-" * 40)
print("Note: This would show only 2 out of all questions in a block")
print("Example: api.randomize_questions_in_block(sid, block_id, subset_count=2)")

# Get randomization summary
print("\n" + "="*60)
print("RANDOMIZATION SETTINGS SUMMARY")
print("="*60)
try:
    settings = api.get_randomization_settings(sid)

    if settings['block_randomization']:
        print("\nBlock Randomization:")
        for br in settings['block_randomization']:
            print(f"  - Blocks: {br['blocks']}")
            print(f"    Even Presentation: {br['even_presentation']}")
            print(f"    Subset: {br['subset']}")

    if settings['question_randomization']:
        print("\nQuestion Randomization:")
        for block_id, info in settings['question_randomization'].items():
            print(f"  - {info['description']} ({block_id})")
            print(f"    Type: {info['randomization'].get('Type', 'N/A')}")

    if settings['choice_randomization']:
        print("\nChoice Randomization:")
        for qid, info in settings['choice_randomization'].items():
            print(f"  - {info['question_text']}... ({qid})")
            print(f"    Type: {info['randomization'].get('Type', 'N/A')}")

except Exception as e:
    print(f"Could not retrieve settings: {e}")

# Final info
print("\n" + "="*60)
print("SURVEY COMPLETE")
print("="*60)
print(f"\nSurvey URL: {api.get_survey_url(sid)}")
print(f"Survey ID: {sid}")
print("\nOpen the survey in Qualtrics to verify randomization settings!")
print("\nTip: Go to Survey Flow to see block randomization,")
print("     and Block Options to see question randomization.")
