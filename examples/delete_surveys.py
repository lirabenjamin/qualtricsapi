"""
Delete Surveys Example
Simple script to delete test surveys

This example shows how to:
1. List all surveys
2. Filter surveys by name pattern
3. Delete selected surveys
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

print("="*60)
print("DELETE SURVEYS")
print("="*60)

# Get all surveys
print("\nFetching all surveys...")
surveys = api.list_surveys()
print(f"Found {len(surveys)} total surveys")

# Filter for example/test surveys
# Modify this pattern to match your test surveys
test_patterns = [
    "Display Logic Demo",
    "Test Survey",
    "Example Survey",
    # Add more patterns as needed
]

test_surveys = []
for survey in surveys:
    for pattern in test_patterns:
        if pattern.lower() in survey['name'].lower():
            test_surveys.append(survey)
            break

if not test_surveys:
    print("\nNo test surveys found matching patterns:")
    for pattern in test_patterns:
        print(f"  - {pattern}")
    print("\nExiting...")
    sys.exit(0)

print(f"\nFound {len(test_surveys)} test surveys to delete:")
print("-" * 60)
for i, survey in enumerate(test_surveys, 1):
    print(f"{i}. {survey['name']} (ID: {survey['id']})")

# Confirm deletion
print("\n" + "="*60)
print("WARNING: This will permanently delete these surveys!")
print("="*60)
response = input("\nType 'DELETE' to confirm deletion: ")

if response.strip() != 'DELETE':
    print("\nDeletion cancelled. Exiting...")
    sys.exit(0)

# Delete surveys
print("\nDeleting surveys...")
deleted_count = 0
failed_count = 0

for survey in test_surveys:
    try:
        api.delete_survey(survey['id'])
        print(f"✓ Deleted: {survey['name']} (ID: {survey['id']})")
        deleted_count += 1
    except Exception as e:
        print(f"✗ Failed to delete {survey['name']}: {str(e)}")
        failed_count += 1

print("\n" + "="*60)
print(f"SUMMARY")
print("="*60)
print(f"Deleted: {deleted_count}")
print(f"Failed: {failed_count}")
print(f"Total: {len(test_surveys)}")
print("\nDone!")
