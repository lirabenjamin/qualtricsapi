"""
Compare Display Logic
Get the display logic from a survey where you've manually fixed it in the UI
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
print("COMPARE DISPLAY LOGIC STRUCTURES")
print("="*80)

# Ask for survey ID and question ID
survey_id = input("\nEnter Survey ID: ").strip()
question_id = input("Enter Question ID (the one with display logic): ").strip()

if not survey_id or not question_id:
    print("Error: Survey ID and Question ID are required")
    sys.exit(1)

try:
    # Get the question
    question = api.get_question(survey_id, question_id)

    print("\n" + "="*80)
    print(f"QUESTION: {question_id}")
    print("="*80)
    print(f"Type: {question['QuestionType']}")
    print(f"Selector: {question['Selector']}")
    print(f"Text: {question['QuestionText']}")

    if 'DisplayLogic' in question and question['DisplayLogic']:
        print("\n" + "="*80)
        print("DISPLAY LOGIC (FULL STRUCTURE)")
        print("="*80)
        print(json.dumps(question['DisplayLogic'], indent=2))

        # Analyze the condition
        dl = question['DisplayLogic']
        if '0' in dl and '0' in dl['0']:
            condition = dl['0']['0']
            print("\n" + "="*80)
            print("CONDITION BREAKDOWN")
            print("="*80)
            for key, value in sorted(condition.items()):
                print(f"  {key:20s}: {value}")

            # Check for fields we might be missing
            print("\n" + "="*80)
            print("CHECKING FOR OPTIONAL FIELDS")
            print("="*80)
            optional_fields = [
                'QuestionIDFromLocator',
                'LeftOperand',
                'Description',
                'SetID',
                'RecordedChoices'
            ]
            for field in optional_fields:
                if field in condition:
                    print(f"  ✓ {field}: {condition[field]}")
                else:
                    print(f"  ✗ {field}: Not present")
    else:
        print("\n⚠️  No display logic found on this question")

except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("DONE")
print("="*80)
