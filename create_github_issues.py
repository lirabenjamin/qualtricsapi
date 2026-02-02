#!/usr/bin/env python3
"""
Script to create GitHub issues programmatically using the GitHub CLI
Prerequisites:
    1. Install GitHub CLI: https://cli.github.com/
    2. Authenticate: gh auth login
    3. Initialize git repo with GitHub remote
"""

import subprocess
import sys
from typing import Dict, List

def check_prerequisites() -> bool:
    """Check if prerequisites are met"""
    print("=" * 60)
    print("Creating GitHub Issues for Qualtrics SDK")
    print("=" * 60)
    print()

    # Check if gh is installed
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitHub CLI (gh) is not installed.")
        print("Install it from: https://cli.github.com/")
        print("macOS: brew install gh")
        print("Ubuntu: sudo apt install gh")
        return False

    # Check if authenticated
    try:
        subprocess.run(["gh", "auth", "status"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("❌ Not authenticated with GitHub CLI.")
        print("Run: gh auth login")
        return False

    # Check if in git repo
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Not in a git repository.")
        print("Initialize with: git init && git remote add origin <github-url>")
        return False

    print("✅ Prerequisites checked")
    print()
    return True

def create_issue(title: str, body: str, labels: List[str], milestone: str = None) -> bool:
    """Create a GitHub issue using gh CLI"""
    cmd = [
        "gh", "issue", "create",
        "--title", title,
        "--body", body,
        "--label", ",".join(labels)
    ]

    if milestone:
        cmd.extend(["--milestone", milestone])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        if "milestone" in e.stderr.lower():
            print(f"Note: Milestone '{milestone}' may need to be created first")
            # Try without milestone
            cmd_no_milestone = [c for c in cmd if c not in ["--milestone", milestone]]
            try:
                result = subprocess.run(cmd_no_milestone, capture_output=True, text=True, check=True)
                print(result.stdout)
                return True
            except subprocess.CalledProcessError:
                print(f"❌ Failed to create issue: {e.stderr}")
                return False
        else:
            print(f"❌ Failed to create issue: {e.stderr}")
            return False

def main():
    """Main function to create all issues"""
    if not check_prerequisites():
        sys.exit(1)

    issues = [
        {
            "title": "[FEATURE] Add Embedded Data Support",
            "body": """## Feature Request: Embedded Data Support

### Description
Add functionality to set and manage embedded data fields in Qualtrics surveys. Embedded data allows you to store and pass custom data with survey responses, enabling personalization and advanced data collection.

### Use Cases

1. **Personalization**: Pass respondent information (name, ID, department) to customize survey experience
2. **Data Collection**: Capture external data (source, campaign, referral code) with responses
3. **Conditional Logic**: Use embedded data to control survey flow and display logic
4. **Data Analysis**: Include additional variables for segmentation and analysis

### Proposed API

```python
# Set embedded data field
api.set_embedded_data(
    survey_id,
    field_name="user_id",
    field_type="text"  # text, number, date
)

# Set multiple embedded data fields
api.set_embedded_data_fields(
    survey_id,
    fields={
        "user_id": {"type": "text"},
        "department": {"type": "text"},
        "enrollment_year": {"type": "number"}
    }
)

# Generate survey link with embedded data
url = api.get_survey_url_with_embedded_data(
    survey_id,
    embedded_data={
        "user_id": "12345",
        "department": "Engineering"
    }
)
```

### Technical Details

**Implementation Requirements:**
1. New module: `qualtrics_sdk/core/embedded_data.py` with `EmbeddedDataMixin`
2. Methods for CRUD operations on embedded data fields
3. Helper for generating survey URLs with embedded data parameters
4. Documentation in `docs/EMBEDDED_DATA_GUIDE.md`
5. Example script: `examples/embedded_data_example.py`

### Priority
**Medium-High** - Embedded data is essential for many advanced survey use cases

### Version Target
v0.2.0 (as specified in ROADMAP.md)

### Resources
- [Qualtrics Embedded Data Documentation](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/embedded-data/)
- [Qualtrics API - Survey Flow](https://api.qualtrics.com/6b00592b9c013-get-flow)

See full specification in: `.github/ISSUE_TEMPLATE/embedded-data.md`
""",
            "labels": ["enhancement", "v0.2.0"],
            "milestone": "v0.2.0"
        },
        {
            "title": "[FEATURE] Add Randomization Support",
            "body": """## Feature Request: Randomization Support

### Description
Add functionality to randomize blocks, questions within blocks, and answer choices within questions. Randomization helps reduce bias and order effects in surveys.

### Use Cases

1. **Block Randomization**: Present survey sections in random order
2. **Question Randomization**: Randomize question order within a block
3. **Choice Randomization**: Randomize answer options (MC, matrix, rank order)
4. **Experimental Design**: Create randomized experimental conditions
5. **Attention Checks**: Randomly insert attention check questions

### Proposed API

```python
# Randomize blocks in survey flow
api.randomize_blocks(
    survey_id,
    block_ids=["BL_xxx", "BL_yyy", "BL_zzz"],
    evenly_present=True  # Ensures even distribution
)

# Randomize questions within a block
api.randomize_questions_in_block(
    survey_id,
    block_id="BL_xxx",
    question_ids=["QID1", "QID2", "QID3"]
)

# Randomize answer choices for a question
api.randomize_question_choices(
    survey_id,
    question_id="QID1",
    anchor_last="Other"  # Keep "Other" at the end
)
```

### Randomization Types

1. **Simple Randomization**: Random order, no constraints
2. **Even Presentation**: Equal distribution across respondents
3. **Latin Square**: Balanced experimental design
4. **Subset Randomization**: Show random subset (e.g., 3 out of 5)

### Technical Details

**Implementation Requirements:**
1. New module: `qualtrics_sdk/core/randomization.py` with `RandomizationMixin`
2. Support for different randomization types
3. Documentation in `docs/RANDOMIZATION_GUIDE.md`
4. Example scripts for block and choice randomization

### Priority
**Medium** - Important for research quality and reducing bias

### Version Target
v0.2.0 (as specified in ROADMAP.md)

### Resources
- [Qualtrics Randomization Documentation](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/randomizer/)
- [Qualtrics API - Survey Flow](https://api.qualtrics.com/6b00592b9c013-get-flow)

See full specification in: `.github/ISSUE_TEMPLATE/randomization.md`
""",
            "labels": ["enhancement", "v0.2.0"],
            "milestone": "v0.2.0"
        },
        {
            "title": "[FEATURE] Add Conditional Display / Display Logic Support",
            "body": """## Feature Request: Conditional Display / Display Logic

### Description
Add functionality to show or hide questions and blocks based on previous responses (display logic/skip logic). This enables dynamic, adaptive surveys that tailor the experience to each respondent.

### Use Cases

1. **Skip Logic**: Skip irrelevant questions based on earlier answers
2. **Branching**: Direct respondents down different paths
3. **Screening**: Show follow-up questions only to qualified respondents
4. **Personalization**: Customize survey flow based on responses
5. **Complex Logic**: Combine multiple conditions with AND/OR operators

### Proposed API

```python
# Simple display logic
api.set_display_logic(
    survey_id,
    element_id="BL_xxx",
    element_type="Block",
    condition={
        "question_id": "QID1",
        "operator": "Selected",
        "choice_id": "1"
    }
)

# Multiple conditions with AND/OR
api.set_display_logic(
    survey_id,
    element_id="BL_xxx",
    element_type="Block",
    conditions=[
        {"question_id": "QID1", "operator": "Selected", "choice_id": "1"},
        {"question_id": "QID2", "operator": "GreaterThan", "value": "5"}
    ],
    logic_type="AND"
)

# Helper methods
api.skip_if(survey_id, skip_element_id="QID5",
            if_question_id="QID1", if_choice_id="2")

api.show_only_if(survey_id, show_element_id="QID10",
                 if_question_id="QID3", if_operator="GreaterThan",
                 if_value="50")
```

### Supported Operators
- Selected / NotSelected
- Equals / NotEquals
- GreaterThan / LessThan / GreaterThanOrEqual / LessThanOrEqual
- Contains / DoesNotContain
- IsAnswered / IsNotAnswered

### Technical Details

**Implementation Requirements:**
1. New module: `qualtrics_sdk/core/display_logic.py` with `DisplayLogicMixin`
2. Methods for simple and complex display logic
3. Helper methods for common patterns
4. Optional: Logic builder class for complex conditions
5. Documentation in `docs/DISPLAY_LOGIC_GUIDE.md`
6. Example scripts for common branching patterns

### Priority
**High** - Display logic is essential for creating sophisticated, adaptive surveys

### Version Target
v0.2.0 (as specified in ROADMAP.md)

### Resources
- [Qualtrics Display Logic Documentation](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/display-logic/)
- [Qualtrics API - Survey Flow](https://api.qualtrics.com/6b00592b9c013-get-flow)

See full specification in: `.github/ISSUE_TEMPLATE/conditional-display.md`
""",
            "labels": ["enhancement", "v0.2.0"],
            "milestone": "v0.2.0"
        },
        {
            "title": "[FEATURE] Add Response Management and Export Support",
            "body": """## Feature Request: Response Management and Export

### Description
Add functionality to retrieve, export, and manage survey responses. This enables programmatic access to response data for analysis, reporting, and integration with other systems.

### Use Cases

1. **Data Retrieval**: Download survey responses for analysis
2. **Real-time Monitoring**: Check response counts and completion rates
3. **Data Export**: Export responses in various formats (CSV, JSON, SPSS)
4. **Data Cleaning**: Delete test responses or duplicates
5. **Integration**: Feed response data into other systems automatically
6. **Reporting**: Generate automated reports from response data

### Proposed API

```python
# Get response count
count = api.get_response_count(survey_id)

# List responses
responses = api.list_responses(
    survey_id,
    start_date="2024-01-01",
    status="Complete",
    limit=100
)

# Export responses
api.export_responses(
    survey_id,
    format="csv",
    save_to="responses.csv",
    wait_for_completion=True
)

# Delete response
api.delete_response(survey_id, response_id)

# Get statistics
stats = api.get_response_statistics(survey_id)
```

### Export Formats
- CSV (Comma-separated values)
- JSON (JavaScript Object Notation)
- SPSS (Statistical Package for Social Sciences)
- XML (Extensible Markup Language)

### Technical Details

**Implementation Requirements:**
1. New module: `qualtrics_sdk/core/responses.py` with `ResponseMixin`
2. Export manager with async polling for export completion
3. Methods for listing, retrieving, deleting responses
4. Response statistics and monitoring
5. Documentation in `docs/RESPONSE_MANAGEMENT_GUIDE.md`
6. Example scripts for common workflows

### Priority
**High** - Response data is the primary output of surveys; accessing it programmatically is essential

### Version Target
v0.4.0 (as specified in ROADMAP.md)

### Resources
- [Qualtrics Response API Documentation](https://api.qualtrics.com/ZG9jOjg3NzY3MA-getting-survey-responses-via-the-new-export-ap-is)
- [Qualtrics Export API Guide](https://api.qualtrics.com/6b00592b9c013-create-response-export)

See full specification in: `.github/ISSUE_TEMPLATE/response-management.md`
""",
            "labels": ["enhancement", "v0.4.0"],
            "milestone": "v0.4.0"
        }
    ]

    success_count = 0
    for i, issue in enumerate(issues, 1):
        print(f"Creating Issue #{i}: {issue['title']}...")
        if create_issue(issue["title"], issue["body"], issue["labels"], issue.get("milestone")):
            print(f"✅ Issue #{i} created")
            success_count += 1
        else:
            print(f"❌ Issue #{i} failed")
        print()

    print("=" * 60)
    print(f"✅ {success_count}/{len(issues)} Issues Created Successfully!")
    print("=" * 60)
    print()
    print("View issues with: gh issue list")
    print("View a specific issue: gh issue view <number>")
    print()

    if success_count < len(issues):
        print("Note: Some issues failed to create.")
        print("If milestones don't exist yet, create them on GitHub:")
        print("  - Repository → Issues → Milestones → New milestone")
        print("  - Create 'v0.2.0' and 'v0.4.0' milestones")
        print("  - Then run: gh issue edit <number> --milestone 'v0.2.0'")

if __name__ == "__main__":
    main()
