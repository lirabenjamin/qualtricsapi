# GitHub Issue Templates Summary

## Overview

Created comprehensive GitHub issue templates for planned features. These templates provide detailed specifications for implementing key Qualtrics API functionality.

## Created Templates

### 1. Embedded Data Support
**File:** `.github/ISSUE_TEMPLATE/embedded-data.md`
**Priority:** Medium-High | **Version:** v0.2.0

#### Key Features
- Set/get/remove embedded data fields
- Generate survey URLs with embedded data parameters
- Support multiple data types (text, number, date)
- Bulk operations for multiple fields

#### API Preview
```python
api.set_embedded_data(survey_id, field_name="user_id", field_type="text")
api.get_embedded_data_fields(survey_id)
url = api.get_survey_url_with_embedded_data(
    survey_id,
    embedded_data={"user_id": "12345", "department": "Engineering"}
)
```

#### Implementation Needs
- New module: `qualtrics_sdk/core/embedded_data.py`
- Documentation: `docs/EMBEDDED_DATA_GUIDE.md`
- Example: `examples/embedded_data_example.py`

---

### 2. Randomization Support
**File:** `.github/ISSUE_TEMPLATE/randomization.md`
**Priority:** Medium | **Version:** v0.2.0

#### Key Features
- Block randomization
- Question randomization within blocks
- Choice randomization with anchoring options
- Advanced designs (Latin Square, balanced presentation)
- Subset randomization (show N of M elements)

#### API Preview
```python
api.randomize_blocks(survey_id, block_ids=["BL_1", "BL_2", "BL_3"])
api.randomize_questions_in_block(survey_id, block_id)
api.randomize_question_choices(
    survey_id,
    question_id,
    anchor_last="Other"  # Keep "Other" at the end
)
```

#### Implementation Needs
- New module: `qualtrics_sdk/core/randomization.py`
- Documentation: `docs/RANDOMIZATION_GUIDE.md`
- Examples:
  - `examples/block_randomization_example.py`
  - `examples/choice_randomization_example.py`

---

### 3. Conditional Display / Display Logic
**File:** `.github/ISSUE_TEMPLATE/conditional-display.md`
**Priority:** High | **Version:** v0.2.0

#### Key Features
- Simple skip logic (if X then show Y)
- Multi-condition logic (AND/OR operators)
- Nested conditions
- Embedded data conditions
- Helper methods for common patterns

#### API Preview
```python
# Simple
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

# Helpers
api.skip_if(survey_id, skip_element_id="QID5",
            if_question_id="QID1", if_choice_id="2")

api.show_only_if(survey_id, show_element_id="QID10",
                 if_question_id="QID3", if_operator="GreaterThan",
                 if_value="50")
```

#### Implementation Needs
- New module: `qualtrics_sdk/core/display_logic.py`
- Optional: Logic builder class for complex conditions
- Documentation: `docs/DISPLAY_LOGIC_GUIDE.md`
- Examples:
  - `examples/simple_skip_logic.py`
  - `examples/complex_branching.py`
  - `examples/screening_survey.py`

---

### 4. Response Management
**File:** `.github/ISSUE_TEMPLATE/response-management.md`
**Priority:** High | **Version:** v0.4.0

#### Key Features
- List and retrieve responses with pagination
- Export responses in multiple formats (CSV, JSON, SPSS, XML)
- Delete and update responses
- Response statistics and monitoring
- Integration with pandas for analysis

#### API Preview
```python
# Get responses
count = api.get_response_count(survey_id)
responses = api.list_responses(survey_id, status="Complete")

# Export
api.export_responses(
    survey_id,
    format="csv",
    save_to="responses.csv",
    wait_for_completion=True
)

# Management
api.delete_response(survey_id, response_id)
stats = api.get_response_statistics(survey_id)
```

#### Implementation Needs
- New module: `qualtrics_sdk/core/responses.py`
- Export manager with async polling
- Data parsers for multiple formats
- Documentation: `docs/RESPONSE_MANAGEMENT_GUIDE.md`
- Examples:
  - `examples/export_responses.py`
  - `examples/response_monitoring.py`
  - `examples/data_cleaning.py`

---

### 5. Bug Report Template
**File:** `.github/ISSUE_TEMPLATE/bug-report.md`

Standard bug report template with sections for:
- Description
- Steps to reproduce
- Expected vs actual behavior
- Error messages
- Environment details

---

## File Structure

```
.github/
└── ISSUE_TEMPLATE/
    ├── README.md                  # Guide to using templates
    ├── config.yml                 # Template configuration
    ├── bug-report.md             # Bug report template
    ├── embedded-data.md          # Feature: Embedded data
    ├── randomization.md          # Feature: Randomization
    ├── conditional-display.md    # Feature: Display logic
    └── response-management.md    # Feature: Response management
```

## Implementation Roadmap

### Phase 1: v0.2.0 - Survey Flow & Logic
1. **Embedded Data** - Foundation for personalization and logic
2. **Conditional Display** - Essential for sophisticated surveys
3. **Randomization** - Important for research validity

### Phase 2: v0.4.0 - Data Collection
4. **Response Management** - Access and analyze survey data

## Using the Templates

### On GitHub
When creating a new issue:
1. Click "New Issue"
2. Select the appropriate template
3. Fill in all sections
4. Submit

### Locally
```bash
# View templates
ls .github/ISSUE_TEMPLATE/

# Create issue from template (with GitHub CLI)
gh issue create --template embedded-data.md
```

## Template Features

Each feature template includes:

✅ **Clear description** of functionality
✅ **Use cases** and scenarios
✅ **Proposed API** with code examples
✅ **Technical details** (endpoints, data structures)
✅ **Implementation requirements** (files, modules, docs)
✅ **Testing requirements** with checklist
✅ **Documentation needs**
✅ **Acceptance criteria**
✅ **Related features** and dependencies
✅ **Resources** (Qualtrics docs, API refs)
✅ **Priority** and **version target**

## Benefits

1. **Planning**: Detailed specs guide implementation
2. **Communication**: Clear requirements for contributors
3. **Tracking**: Monitor progress against acceptance criteria
4. **Documentation**: Templates become reference docs
5. **Quality**: Comprehensive testing requirements ensure robust implementation

## Next Steps

### For Maintainers
1. Review templates for accuracy
2. Adjust priorities if needed
3. Create actual GitHub issues from templates
4. Assign to milestones (v0.2.0, v0.4.0)
5. Add to project board

### For Contributors
1. Check existing issues before starting work
2. Reference templates when implementing features
3. Ensure all acceptance criteria met
4. Create tests based on testing requirements
5. Write documentation as specified

## Notes

- Templates are version-controlled and can be updated
- Issues created from templates can be customized
- Templates help maintain consistency across features
- Each template is self-contained with full context

---

**Created:** 2024-02-01
**Last Updated:** 2024-02-01
**Status:** Ready for use
