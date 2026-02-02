---
name: Feature Request - Embedded Data Support
about: Add support for setting and managing embedded data in surveys
title: '[FEATURE] Add Embedded Data Support'
labels: enhancement, v0.2.0
assignees: ''
---

## Feature Request: Embedded Data Support

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

# Get embedded data fields
fields = api.get_embedded_data_fields(survey_id)

# Remove embedded data field
api.remove_embedded_data_field(survey_id, "field_name")

# Generate survey link with embedded data
url = api.get_survey_url_with_embedded_data(
    survey_id,
    embedded_data={
        "user_id": "12345",
        "department": "Engineering"
    }
)
# Returns: https://...?user_id=12345&department=Engineering
```

### Technical Details

**Qualtrics API Endpoints:**
- `GET /survey-definitions/{surveyId}/flow` - Get survey flow (includes embedded data)
- `PUT /survey-definitions/{surveyId}/flow` - Update survey flow (to add embedded data)
- `POST /survey-definitions/{surveyId}/embeddeddata` - Create embedded data field

**Implementation Requirements:**
1. New module: `qualtrics_sdk/core/embedded_data.py` with `EmbeddedDataMixin`
2. Methods for CRUD operations on embedded data fields
3. Helper for generating survey URLs with embedded data parameters
4. Update `QualtricsAPI` class to include `EmbeddedDataMixin`
5. Documentation in `docs/EMBEDDED_DATA_GUIDE.md`
6. Example script: `examples/embedded_data_example.py`

### Documentation Needs

- Complete guide on using embedded data
- Examples for common use cases:
  - Personalized surveys
  - Panel/longitudinal studies
  - A/B testing with embedded data
  - Integration with external systems
- Best practices for field naming and data types

### Testing Requirements

- [ ] Create survey with embedded data fields
- [ ] Set single and multiple fields
- [ ] Generate URLs with embedded data
- [ ] Retrieve and verify embedded data fields
- [ ] Remove embedded data fields
- [ ] Test different data types (text, number, date)

### Related Features

- Survey Flow API (for conditional display based on embedded data)
- Response collection (embedded data appears in response data)
- Distribution links (embedded data in distribution URLs)

### Priority

**Medium-High** - Embedded data is essential for many advanced survey use cases

### Version Target

v0.2.0 (as specified in ROADMAP.md)

### Resources

- [Qualtrics Embedded Data Documentation](https://www.qualtrics.com/support/survey-platform/survey-module/survey-flow/standard-elements/embedded-data/)
- [Qualtrics API - Survey Flow](https://api.qualtrics.com/6b00592b9c013-get-flow)

### Acceptance Criteria

- [ ] Can create embedded data fields via API
- [ ] Can retrieve list of embedded data fields
- [ ] Can delete embedded data fields
- [ ] Can generate survey URLs with embedded data parameters
- [ ] All methods have proper error handling
- [ ] Comprehensive documentation provided
- [ ] Working examples included
- [ ] Tests pass successfully

---

**Additional Notes:**

Embedded data is foundational for many workflows, so implementation should be robust and well-documented. Consider how this interacts with survey flow and distribution features planned for future versions.
