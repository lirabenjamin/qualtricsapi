# Qualtrics SDK Roadmap

This document outlines the planned features and improvements for the Qualtrics SDK.

## Version Status

**Current Version:** 0.1.0  
**Status:** Initial Development (Pre-1.0)  
**Last Updated:** 2026-02-01

---

## Version 0.1.0 ✅ COMPLETED (2026-02-01)

### Features Implemented
- ✅ Survey operations (CRUD)
- ✅ Question types:
  - Multiple choice (radio, dropdown)
  - Text entry (single-line, essay)
  - Matrix/Likert scale
  - Slider
  - Rank order
  - NPS
  - Descriptive text
- ✅ Question management (create, update, delete)
- ✅ Block operations
- ✅ Secure credential management (.env)
- ✅ Comprehensive documentation
- ✅ Working examples

---

## Version 0.2.0 (Target: 2026-03-01)

### Priority: HIGH - Essential Survey Features

#### Embedded Data Support 🎯
**Status:** Planned  
**Priority:** HIGH  
**Issue:** #TBD

Embedded data allows you to pass custom data into surveys (user IDs, metadata, etc.)

**Planned API:**
```python
# Add embedded data fields
api.add_embedded_data(survey_id, {
    "user_id": "${e://Field/user_id}",
    "source": "email_campaign",
    "segment": "premium_users"
})

# Get embedded data fields
fields = api.get_embedded_data(survey_id)

# Update embedded data
api.update_embedded_data(survey_id, field_name, new_value)

# Delete embedded data field
api.delete_embedded_data(survey_id, field_name)
```

**Use Cases:**
- Track respondent metadata
- Pre-fill form fields
- Segment analysis
- Integration with external systems

---

#### Survey Flow Support 🎯
**Status:** Planned  
**Priority:** HIGH  
**Issue:** #TBD

Control survey logic, branching, and flow.

**Planned API:**
```python
# Get survey flow
flow = api.get_survey_flow(survey_id)

# Add branch logic
api.add_branch(survey_id, {
    "condition": "Q1 == 'Yes'",
    "true_action": "show_block_2",
    "false_action": "skip_to_end"
})

# Add randomization
api.add_randomizer(survey_id, block_ids=[
    "block_1", "block_2", "block_3"
], randomize_type="random", evenly_present=True)

# Update survey flow
api.update_survey_flow(survey_id, flow_definition)
```

**Use Cases:**
- A/B testing
- Skip logic
- Question randomization
- Block randomization

---

## Version 0.3.0 (Target: 2026-04-01)

### Priority: HIGH - Advanced Question Features

#### Custom JavaScript for Questions 🎯
**Status:** Planned  
**Priority:** MEDIUM  
**Issue:** #TBD

Add custom JavaScript to questions for advanced interactivity.

**Planned API:**
```python
# Add JavaScript to question
api.add_question_javascript(
    survey_id,
    question_id,
    javascript_code="""
    Qualtrics.SurveyEngine.addOnReady(function() {
        // Custom JavaScript here
        console.log('Question loaded');
    });
    """
)

# Common presets
api.add_auto_advance(survey_id, question_id, delay_ms=3000)
api.add_input_validation(survey_id, question_id, regex=r"^\d{5}$")
```

**Use Cases:**
- Custom validation
- Auto-advance questions
- Hide/show elements
- Custom interactions

---

#### Loop and Merge Support 🎯
**Status:** Planned  
**Priority:** MEDIUM  
**Issue:** #TBD

Create repeated questions with piped data.

**Planned API:**
```python
# Create loop and merge
api.create_loop_and_merge(survey_id, {
    "name": "Product Ratings",
    "fields": ["product_name", "product_id"],
    "data": [
        ["Laptop", "P001"],
        ["Mouse", "P002"],
        ["Keyboard", "P003"]
    ]
})

# Use in questions with piping
api.create_question_with_piping(
    survey_id,
    "How would you rate ${lm://Field/product_name}?"
)
```

**Use Cases:**
- Product rating surveys
- Multiple item evaluations
- Repeated measures

---

#### Quota Support 🎯
**Status:** Planned  
**Priority:** MEDIUM  
**Issue:** #TBD

Set response limits and quotas.

**Planned API:**
```python
# Create quota
api.create_quota(survey_id, {
    "name": "Age 18-25",
    "logic": "Q_age >= 18 AND Q_age <= 25",
    "quota": 100,
    "action": "end_survey",
    "message": "Thank you, we've reached our quota."
})

# Get quota status
status = api.get_quota_status(survey_id, quota_id)
# Returns: {"responses": 87, "quota": 100, "remaining": 13}
```

**Use Cases:**
- Sample stratification
- Budget management
- Representative sampling

---

## Version 0.4.0 (Target: 2026-05-01)

### Priority: MEDIUM - Distribution & Response Collection

#### Distribution Management 🎯
**Status:** Planned  
**Priority:** MEDIUM  
**Issue:** #TBD

Manage survey distributions and invitations.

**Planned API:**
```python
# Create distribution
dist = api.create_distribution(
    survey_id,
    mailing_list_id,
    message_id,
    send_date="2026-05-01T10:00:00Z"
)

# Create email distribution
api.send_email_distribution(
    survey_id,
    recipients=["user@example.com"],
    from_email="surveys@company.com",
    from_name="Research Team",
    subject="Please take our survey",
    message="We value your feedback..."
)

# Get distribution stats
stats = api.get_distribution_stats(distribution_id)
```

**Use Cases:**
- Email surveys
- Panel management
- Response tracking

---

#### Response Management 🎯
**Status:** Planned  
**Priority:** HIGH  
**Issue:** #TBD

Retrieve and manage survey responses.

**Planned API:**
```python
# Get responses
responses = api.get_responses(survey_id, format="json")

# Export responses
api.export_responses(
    survey_id,
    file_format="csv",
    output_path="responses.csv"
)

# Get individual response
response = api.get_response(survey_id, response_id)

# Update response
api.update_response(survey_id, response_id, updates={
    "Q1": "Updated answer"
})

# Delete response
api.delete_response(survey_id, response_id)
```

**Use Cases:**
- Data download
- Data cleaning
- Response management
- Real-time monitoring

---

## Version 0.5.0 (Target: 2026-06-01)

### Priority: MEDIUM - Advanced Question Types & Features

#### Additional Question Types 🎯
**Status:** Planned  
**Priority:** LOW  
**Issue:** #TBD

**New Question Types:**
- Heat map questions
- Graphic slider
- Pick, group, and rank
- Drill down
- Highlight
- Slider with text entry
- Constant sum
- Side-by-side questions

**Planned API:**
```python
# Heat map
api.create_heatmap_question(survey_id, "Click areas of interest", image_url="...")

# Constant sum
api.create_constant_sum_question(
    survey_id,
    "Allocate 100 points:",
    items=["Quality", "Price", "Service"],
    total=100
)
```

---

#### Question Display Logic 🎯
**Status:** Planned  
**Priority:** MEDIUM  
**Issue:** #TBD

Control when questions appear based on previous answers.

**Planned API:**
```python
# Add display logic to question
api.add_display_logic(survey_id, question_id, {
    "condition": "Q1 == 'Yes' AND Q2 > 5",
    "conjunction": "AND"
})

# Add skip logic
api.add_skip_logic(survey_id, question_id, {
    "if": "Q3 == 'No'",
    "then": "skip_to_end"
})
```

---

## Version 0.6.0 (Target: 2026-07-01)

### Priority: MEDIUM - Collaboration & Management

#### User & Permission Management 🎯
**Status:** Planned  
**Priority:** LOW  
**Issue:** #TBD

Manage users and permissions.

**Planned API:**
```python
# Get users in account
users = api.get_users()

# Add user permission to survey
api.add_user_permission(survey_id, user_id, permissions=["edit", "view"])

# Create collaborator
api.add_collaborator(survey_id, email="colleague@example.com")
```

---

#### Library Management 🎯
**Status:** Planned  
**Priority:** LOW  
**Issue:** #TBD

Manage reusable messages, blocks, and questions.

**Planned API:**
```python
# Save block to library
api.save_block_to_library(survey_id, block_id, "Demographics Block")

# Load block from library
api.load_block_from_library(survey_id, library_block_id)

# Manage message library
api.create_library_message("Thank You", "Thank you for participating!")
```

---

## Version 1.0.0 (Target: 2026-09-01)

### 🎉 First Stable Release

**Requirements for 1.0.0:**
- ✅ All core features implemented (v0.1 - v0.6)
- ✅ Comprehensive test coverage (>80%)
- ✅ Full API documentation
- ✅ Multiple real-world case studies
- ✅ Migration guide from v0.x
- ✅ Stable API (no breaking changes after 1.0)
- ✅ Community feedback incorporated
- ✅ Production-ready performance

---

## Future Versions (Post-1.0)

### Version 1.x Series - Enhancements

#### Mailing List Management (1.1.0)
- Create and manage contact lists
- Import contacts from CSV
- Segment management
- Unsubscribe handling

#### XM Directory Integration (1.2.0)
- Contact management
- Directory attributes
- Mailing lists sync

#### Workflow Automation (1.3.0)
- Event-based triggers
- Email notifications
- Data actions
- Integration webhooks

#### Advanced Analytics (1.4.0)
- Response analytics
- Dashboard creation
- Report generation
- Data visualization helpers

#### Multi-language Support (1.5.0)
- Translation management
- Multi-language surveys
- Language detection
- RTL language support

### Version 2.0 - Major Architecture Update

**Potential Features:**
- Async/await API support
- WebSocket support for real-time updates
- GraphQL API integration
- Built-in caching layer
- Plugin system for extensions
- CLI tool for common tasks

---

## Feature Request Process

### How to Request a Feature

1. **Check existing issues** - Maybe it's already planned!
2. **Open an issue** with template:
   ```markdown
   **Feature:** Brief description
   **Use Case:** Why you need it
   **Proposed API:** Example code
   **Priority:** How urgent is it?
   ```
3. **Discuss with community** - Get feedback
4. **Vote with 👍** - Popular features get prioritized
5. **Contribute!** - Submit a PR if you can implement it

### Feature Prioritization

Features are prioritized based on:
1. **User demand** (GitHub reactions/comments)
2. **Importance** (Core vs. nice-to-have)
3. **Complexity** (Easy wins first)
4. **Dependencies** (What's needed first)
5. **Maintainer bandwidth**

---

## Release Schedule

### Planned Cadence

- **Minor releases (0.x.0):** Monthly
- **Patch releases (0.x.y):** As needed (bug fixes)
- **Major milestones:** Quarterly review

### Release Process

1. Feature development in branches
2. Merge to `main` when ready
3. Beta testing period (1-2 weeks)
4. Release candidate (if major)
5. Official release + announcement
6. Update documentation
7. Create GitHub release

---

## Contributing to Roadmap

We welcome community input on the roadmap!

### Ways to Contribute

1. **Vote on features** - React to issues with 👍
2. **Suggest features** - Open feature request issues
3. **Implement features** - Submit PRs for planned features
4. **Test betas** - Help test pre-releases
5. **Write documentation** - Help document new features

### Get Involved

- **GitHub Discussions:** Share ideas and feedback
- **Issues:** Report bugs and request features
- **Pull Requests:** Contribute code
- **Discord/Slack:** Join community discussions (links TBD)

---

## Questions?

- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development guidelines
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution process
- Open an issue for questions about the roadmap

---

**Note:** This roadmap is a living document and may change based on:
- Community feedback
- Qualtrics API updates
- Technical constraints
- Shifting priorities

Last updated: 2026-02-01
