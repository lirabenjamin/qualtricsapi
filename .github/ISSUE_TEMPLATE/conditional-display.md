---
name: Feature Request - Conditional Display / Display Logic
about: Add support for conditional display of questions and blocks based on responses
title: '[FEATURE] Add Conditional Display / Display Logic Support'
labels: enhancement, v0.2.0
assignees: ''
---

## Feature Request: Conditional Display / Display Logic

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
# Simple display logic - show block if condition met
api.set_display_logic(
    survey_id,
    element_id="BL_xxx",  # Block or question ID
    element_type="Block",  # or "Question"
    condition={
        "question_id": "QID1",
        "operator": "Selected",  # or "NotSelected", "Equals", etc.
        "choice_id": "1"
    }
)

# Multiple conditions with AND/OR
api.set_display_logic(
    survey_id,
    element_id="BL_xxx",
    element_type="Block",
    conditions=[
        {
            "question_id": "QID1",
            "operator": "Selected",
            "choice_id": "1"
        },
        {
            "question_id": "QID2",
            "operator": "GreaterThan",
            "value": "5"
        }
    ],
    logic_type="AND"  # or "OR"
)

# Embedded data conditions
api.set_display_logic_embedded_data(
    survey_id,
    element_id="BL_xxx",
    element_type="Block",
    condition={
        "field": "user_type",
        "operator": "Equals",
        "value": "faculty"
    }
)

# Complex nested conditions
api.set_display_logic_advanced(
    survey_id,
    element_id="BL_xxx",
    element_type="Block",
    logic={
        "type": "AND",
        "conditions": [
            {
                "question_id": "QID1",
                "operator": "Selected",
                "choice_id": "1"
            },
            {
                "type": "OR",
                "conditions": [
                    {"question_id": "QID2", "operator": "Equals", "value": "Yes"},
                    {"question_id": "QID3", "operator": "Equals", "value": "Yes"}
                ]
            }
        ]
    }
)

# Get display logic for element
logic = api.get_display_logic(survey_id, element_id="BL_xxx")

# Remove display logic
api.remove_display_logic(survey_id, element_id="BL_xxx")

# Helper: Skip question if another question answered specific way
api.skip_if(
    survey_id,
    skip_element_id="QID5",
    if_question_id="QID1",
    if_choice_id="2"  # Skip QID5 if QID1 chose option 2
)

# Helper: Show question only if...
api.show_only_if(
    survey_id,
    show_element_id="QID10",
    if_question_id="QID3",
    if_operator="GreaterThan",
    if_value="50"
)
```

### Technical Details

**Qualtrics API Endpoints:**
- `GET /survey-definitions/{surveyId}/flow` - Get survey flow including display logic
- `PUT /survey-definitions/{surveyId}/flow` - Update survey flow with display logic

**Display Logic Structure in Survey Flow:**
```json
{
  "Type": "Block",
  "ID": "BL_xxx",
  "FlowID": "FL_xxx",
  "Autofill": [],
  "DisplayLogic": {
    "0": {
      "0": {
        "LogicType": "Question",
        "QuestionID": "QID1",
        "QuestionIsInLoop": "no",
        "ChoiceLocator": "q://QID1/SelectableChoice/1",
        "Operator": "Selected",
        "QuestionIDFromLocator": "QID1",
        "LeftOperand": "q://QID1/SelectableChoice/1",
        "Type": "Expression",
        "Description": "<span class=\"ConjDesc\">If</span> <span class=\"LeftOpDesc\">Q1 Choice 1</span> <span class=\"OpDesc\">Is Selected</span>"
      },
      "Type": "If"
    },
    "Type": "BooleanExpression"
  }
}
```

**Supported Operators:**
- `Selected` / `NotSelected` - For multiple choice
- `Equals` / `NotEquals` - For text/number comparisons
- `GreaterThan` / `LessThan` / `GreaterThanOrEqual` / `LessThanOrEqual` - Numeric
- `Contains` / `DoesNotContain` - Text matching
- `IsDisplayed` / `IsNotDisplayed` - Based on question display
- `IsAnswered` / `IsNotAnswered` - Based on response completion

**Implementation Requirements:**

1. New module: `qualtrics_sdk/core/display_logic.py` with `DisplayLogicMixin`
2. Methods for setting display logic:
   - Simple single-condition logic
   - Multi-condition logic (AND/OR)
   - Nested logic
   - Embedded data conditions
3. Helper methods for common patterns:
   - Skip if
   - Show only if
   - Hide unless
4. Logic builder class for complex conditions
5. Update `QualtricsAPI` class to include `DisplayLogicMixin`
6. Documentation in `docs/DISPLAY_LOGIC_GUIDE.md`
7. Example scripts:
   - `examples/simple_skip_logic.py`
   - `examples/complex_branching.py`
   - `examples/screening_survey.py`

### Logic Builder Pattern

For complex logic, consider a builder pattern:

```python
from qualtrics_sdk import DisplayLogicBuilder

logic = (DisplayLogicBuilder()
    .if_question("QID1").selected("1")
    .and_question("QID2").greater_than(5)
    .or_nested(
        lambda b: b
            .if_question("QID3").equals("Yes")
            .or_question("QID4").equals("Yes")
    )
    .build()
)

api.set_display_logic(survey_id, "BL_xxx", "Block", logic=logic)
```

### Documentation Needs

- Complete guide on display logic concepts
- Visual flowcharts showing branching patterns
- Examples for common scenarios:
  - Simple skip logic
  - Multi-path branching
  - Screening surveys
  - Follow-up questions
  - Embedded data conditions
- Best practices:
  - Testing branching logic
  - Avoiding dead ends
  - Handling complex conditions
  - Performance considerations

### Testing Requirements

- [ ] Set simple display logic (single condition)
- [ ] Set multi-condition logic (AND)
- [ ] Set multi-condition logic (OR)
- [ ] Set nested conditions
- [ ] Test all operator types
- [ ] Display logic based on embedded data
- [ ] Display logic for blocks
- [ ] Display logic for individual questions
- [ ] Retrieve existing display logic
- [ ] Modify existing display logic
- [ ] Remove display logic
- [ ] Test helper methods (skip_if, show_only_if)

### Related Features

- Survey Flow API (display logic is part of flow)
- Embedded Data (can be used in conditions)
- Branch Logic (similar but different - branches to different blocks)
- Quotas (related conditional logic)

### Priority

**High** - Display logic is essential for creating sophisticated, adaptive surveys

### Version Target

v0.2.0 (as specified in ROADMAP.md)

### Resources

- [Qualtrics Display Logic Documentation](https://www.qualtrics.com/support/survey-platform/survey-module/question-options/display-logic/)
- [Qualtrics Skip Logic Guide](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/branch-logic/)
- [Qualtrics API - Survey Flow](https://api.qualtrics.com/6b00592b9c013-get-flow)

### Acceptance Criteria

- [ ] Can set simple display logic via API
- [ ] Can set complex multi-condition logic
- [ ] Support for all common operators
- [ ] Can nest conditions (AND within OR, etc.)
- [ ] Can use embedded data in conditions
- [ ] Works for both blocks and individual questions
- [ ] Can retrieve existing display logic
- [ ] Can modify/remove display logic
- [ ] Helper methods for common patterns work correctly
- [ ] All methods have proper error handling
- [ ] Comprehensive documentation with flowcharts
- [ ] Multiple working example scripts
- [ ] Tests pass successfully

---

**Additional Notes:**

Display logic is one of the most powerful features in Qualtrics. Implementation should be flexible enough to handle simple cases easily while supporting complex nested conditions for advanced users. Consider providing both a simple API for common cases and a builder pattern for complex logic.

The logic structure in Qualtrics can be quite complex - implementation should validate logic before sending to API and provide clear error messages when logic is invalid.
