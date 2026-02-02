"""
Display Logic Example
Demonstrates conditional display / display logic features

This example shows how to:
1. Add simple display logic to show/hide questions
2. Add multi-condition display logic with AND/OR operators
3. Use helper methods (skip_if, show_only_if)
4. Add display logic based on embedded data
5. Get and delete display logic
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
survey = api.create_survey("Display Logic Demo")
sid = survey['SurveyID']
print(f"Survey created: {sid}")

print("\n" + "="*60)
print("CREATING QUESTIONS")
print("="*60)

# Create screening question (Q1)
print("\n1. Creating screening question...")
q1 = api.create_multiple_choice_question(
    sid,
    "Are you interested in providing detailed feedback?",
    choices=["Yes, I'd love to help", "No, just the basics"]
)
q1_id = q1['QuestionID']
print(f"   Created: {q1_id}")

# Create follow-up question (Q2) - will show only if Q1 = "Yes"
print("\n2. Creating follow-up question (conditional)...")
q2 = api.create_text_entry_question(
    sid,
    "Great! Please share any initial thoughts:",
    text_type="ML"
)
q2_id = q2['QuestionID']
print(f"   Created: {q2_id}")

# Create satisfaction rating (Q3)
print("\n3. Creating satisfaction rating...")
q3 = api.create_slider_question(
    sid,
    "On a scale of 0-100, how satisfied are you?",
    min_value=0,
    max_value=100
)
q3_id = q3['QuestionID']
print(f"   Created: {q3_id}")

# Create improvement question (Q4) - will show only if satisfaction < 50
print("\n4. Creating improvement question (conditional on rating)...")
q4 = api.create_text_entry_question(
    sid,
    "We're sorry to hear that. What could we improve?",
    text_type="ML"
)
q4_id = q4['QuestionID']
print(f"   Created: {q4_id}")

# Create product usage question (Q5)
print("\n5. Creating product usage question...")
q5 = api.create_multiple_choice_question(
    sid,
    "Which products do you use?",
    choices=["Product A", "Product B", "Product C", "None"],
    allow_multiple=True  # Multiple answer checkboxes
)
q5_id = q5['QuestionID']
print(f"   Created: {q5_id}")

# Create product-specific question (Q6) - shows only if Product A AND Product B selected
print("\n6. Creating product comparison question (multi-condition)...")
q6 = api.create_matrix_question(
    sid,
    "Compare Product A and Product B:",
    statements=["Ease of use", "Value for money", "Features"],
    scale_points=["A is better", "About equal", "B is better"]
)
q6_id = q6['QuestionID']
print(f"   Created: {q6_id}")

print("\n" + "="*60)
print("ADDING DISPLAY LOGIC")
print("="*60)

# Example 1: Simple display logic - show Q2 only if Q1 = "Yes"
print("\n1. Adding display logic: Show Q2 if 'Yes' selected in Q1...")
api.add_display_logic(
    survey_id=sid,
    question_id=q2_id,
    source_question_id=q1_id,
    operator="Selected",
    choice_locator=f"q://{q1_id}/SelectableChoice/1"  # Choice 1 = "Yes"
)
print("   Display logic added to Q2")

# Example 2: Using show_only_if helper (same as add_display_logic but more semantic)
print("\n2. Adding display logic: Show Q4 only if satisfaction < 50...")
api.show_only_if(
    survey_id=sid,
    question_id=q4_id,
    source_question_id=q3_id,
    operator="LessThan",
    value=50
)
print("   Display logic added to Q4")

# Example 3: Multiple conditions with AND
print("\n3. Adding multi-condition logic: Show Q6 if Product A AND Product B selected...")
api.add_display_logic_multiple(
    survey_id=sid,
    question_id=q6_id,
    conditions=[
        {
            "source_question_id": q5_id,
            "operator": "Selected",
            "choice_locator": f"q://{q5_id}/SelectableChoice/1"  # Product A
        },
        {
            "source_question_id": q5_id,
            "operator": "Selected",
            "choice_locator": f"q://{q5_id}/SelectableChoice/2"  # Product B
        }
    ],
    conjunction="AND"
)
print("   Multi-condition display logic added to Q6")

print("\n" + "="*60)
print("VERIFYING DISPLAY LOGIC")
print("="*60)

# Get display logic for each question
print("\nRetrieving display logic for questions...")

q2_logic = api.get_display_logic(sid, q2_id)
print(f"\nQ2 Display Logic: {'Set' if q2_logic else 'None'}")
if q2_logic:
    print(f"   Type: {q2_logic.get('Type', 'N/A')}")

q4_logic = api.get_display_logic(sid, q4_id)
print(f"\nQ4 Display Logic: {'Set' if q4_logic else 'None'}")
if q4_logic:
    print(f"   Type: {q4_logic.get('Type', 'N/A')}")

q6_logic = api.get_display_logic(sid, q6_id)
print(f"\nQ6 Display Logic: {'Set' if q6_logic else 'None'}")
if q6_logic:
    print(f"   Type: {q6_logic.get('Type', 'N/A')}")

print("\n" + "="*60)
print("SURVEY SUMMARY")
print("="*60)

print(f"""
Survey ID: {sid}
Survey URL: {api.get_survey_url(sid)}

Questions:
  {q1_id}: Screening question (no logic)
  {q2_id}: Follow-up text -> Shows if Q1="Yes"
  {q3_id}: Satisfaction slider (no logic)
  {q4_id}: Improvement text -> Shows if Q3 < 50
  {q5_id}: Product usage (no logic)
  {q6_id}: Product comparison -> Shows if Product A AND Product B selected

Test the survey to verify display logic works correctly!
""")

print("\n" + "="*60)
print("OPTIONAL: DELETE DISPLAY LOGIC DEMO")
print("="*60)

# Uncomment below to test deleting display logic
# print("\nDeleting display logic from Q2...")
# api.delete_display_logic(sid, q2_id)
# print("   Display logic removed from Q2")
#
# q2_logic_after = api.get_display_logic(sid, q2_id)
# print(f"\nQ2 Display Logic after deletion: {'Set' if q2_logic_after else 'None (removed)'}")

print("\nExample complete!")
