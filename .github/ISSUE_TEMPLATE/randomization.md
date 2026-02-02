---
name: Feature Request - Randomization Support
about: Add support for randomizing blocks, questions, and answer choices
title: '[FEATURE] Add Randomization Support'
labels: enhancement, v0.2.0
assignees: ''
---

## Feature Request: Randomization Support

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
    evenly_present=True  # Ensures even distribution across respondents
)

# Randomize questions within a block
api.randomize_questions_in_block(
    survey_id,
    block_id="BL_xxx",
    question_ids=["QID1", "QID2", "QID3"]  # Optional: specify which questions
)

# Randomize answer choices for a question
api.randomize_question_choices(
    survey_id,
    question_id="QID1",
    exclude_choices=[],  # Optional: don't randomize certain choices (e.g., "Other", "None")
    anchor_first=None,   # Optional: always show this choice first
    anchor_last=None     # Optional: always show this choice last
)

# Set up advanced randomization (Latin Square, etc.)
api.set_randomization_advanced(
    survey_id,
    randomization_type="LatinSquare",  # or "Simple", "Balanced", etc.
    elements=["BL_xxx", "BL_yyy", "BL_zzz"]
)

# Get randomization settings
settings = api.get_randomization_settings(survey_id)

# Remove randomization
api.remove_randomization(survey_id, element_id="BL_xxx")
```

### Technical Details

**Qualtrics API Endpoints:**
- `GET /survey-definitions/{surveyId}/flow` - Get current survey flow including randomization
- `PUT /survey-definitions/{surveyId}/flow` - Update survey flow to add randomization
- Survey flow JSON includes randomization settings in flow elements

**Implementation Requirements:**

1. New module: `qualtrics_sdk/core/randomization.py` with `RandomizationMixin`
2. Methods for different randomization types:
   - Block randomization
   - Question randomization
   - Choice randomization
3. Support for advanced randomization:
   - Latin Square designs
   - Balanced randomization
   - Evenly present options
4. Update `QualtricsAPI` class to include `RandomizationMixin`
5. Documentation in `docs/RANDOMIZATION_GUIDE.md`
6. Example scripts:
   - `examples/block_randomization_example.py`
   - `examples/choice_randomization_example.py`

### Survey Flow Structure for Randomization

```json
{
  "Type": "BlockRandomizer",
  "FlowID": "FL_xxx",
  "SubSet": 3,
  "EvenPresentation": true,
  "Flow": [
    {
      "Type": "Block",
      "ID": "BL_xxx"
    },
    {
      "Type": "Block",
      "ID": "BL_yyy"
    }
  ]
}
```

### Randomization Types

1. **Simple Randomization**: Random order, no constraints
2. **Even Presentation**: Ensures each element presented to equal number of respondents
3. **Latin Square**: Advanced balanced design for experimental studies
4. **Subset Randomization**: Show random subset of elements (e.g., 3 out of 5 blocks)

### Documentation Needs

- Complete guide on randomization concepts
- Examples for each randomization type
- Visual diagrams showing how randomization works
- Best practices:
  - When to use each randomization type
  - Handling "Other" and "None" options
  - Attention checks placement
  - Experimental design considerations

### Testing Requirements

- [ ] Randomize blocks in survey flow
- [ ] Randomize questions within block
- [ ] Randomize answer choices
- [ ] Test even presentation setting
- [ ] Test subset randomization (show N out of M)
- [ ] Verify anchored choices (first/last)
- [ ] Test Latin Square randomization
- [ ] Retrieve and verify randomization settings
- [ ] Remove randomization settings

### Related Features

- Survey Flow API (randomization is part of flow)
- Block management (blocks can be randomized)
- Question management (questions within blocks can be randomized)

### Priority

**Medium** - Important for research quality and reducing bias, but not needed for basic surveys

### Version Target

v0.2.0 (as specified in ROADMAP.md)

### Resources

- [Qualtrics Randomization Documentation](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/randomizer/)
- [Qualtrics API - Survey Flow](https://api.qualtrics.com/6b00592b9c013-get-flow)
- [Research Design with Qualtrics](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/advanced-randomization/)

### Acceptance Criteria

- [ ] Can randomize blocks via API
- [ ] Can randomize questions within blocks
- [ ] Can randomize answer choices with anchoring
- [ ] Support for even presentation
- [ ] Support for subset randomization (show N of M)
- [ ] Can retrieve current randomization settings
- [ ] Can remove/modify randomization
- [ ] All methods have proper error handling
- [ ] Comprehensive documentation with examples
- [ ] Working example scripts for common patterns
- [ ] Tests pass successfully

---

**Additional Notes:**

Randomization is crucial for research validity. Implementation should support both simple use cases (randomize these blocks) and advanced experimental designs (Latin Square, balanced presentation). Consider adding helper functions for common experimental designs (A/B testing, multi-arm experiments).
