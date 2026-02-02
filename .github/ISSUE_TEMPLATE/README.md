# GitHub Issue Templates

This directory contains issue templates for the Qualtrics SDK project.

## Available Templates

### Feature Requests

#### 1. Embedded Data Support (`embedded-data.md`)
**Priority:** Medium-High | **Target:** v0.2.0

Add functionality to set and manage embedded data fields in surveys. Embedded data enables:
- Survey personalization
- External data collection
- Conditional logic based on external variables
- Advanced data analysis

**Key Features:**
- Set/get/delete embedded data fields
- Generate survey URLs with embedded data
- Support for multiple data types (text, number, date)

---

#### 2. Randomization Support (`randomization.md`)
**Priority:** Medium | **Target:** v0.2.0

Add support for randomizing blocks, questions, and answer choices to reduce bias and order effects.

**Key Features:**
- Block randomization
- Question randomization within blocks
- Choice randomization with anchoring
- Advanced designs (Latin Square, balanced presentation)
- Subset randomization (show N of M)

---

#### 3. Conditional Display / Display Logic (`conditional-display.md`)
**Priority:** High | **Target:** v0.2.0

Add functionality for conditional display of questions and blocks based on previous responses.

**Key Features:**
- Simple skip logic
- Multi-condition branching (AND/OR)
- Nested conditions
- Embedded data conditions
- Helper methods for common patterns

---

#### 4. Response Management (`response-management.md`)
**Priority:** High | **Target:** v0.4.0

Add support for retrieving, exporting, and managing survey responses.

**Key Features:**
- List and retrieve responses
- Export in multiple formats (CSV, JSON, SPSS, XML)
- Delete and update responses
- Response statistics
- Pagination for large datasets
- Integration with pandas/analysis tools

---

### Bug Reports (`bug-report.md`)

Use this template to report bugs or unexpected behavior. Please include:
- Clear description
- Minimal code to reproduce
- Expected vs actual behavior
- Full error message
- Environment details

---

## Using These Templates

### On GitHub
When creating a new issue on GitHub, you'll see these templates as options. Select the appropriate template and fill in the details.

### Locally
You can also reference these templates when planning development:

```bash
# View a template
cat .github/ISSUE_TEMPLATE/embedded-data.md

# Create an issue based on a template
gh issue create --template embedded-data.md
```

---

## Implementation Priority

Based on ROADMAP.md:

### v0.2.0 - Survey Flow & Logic
1. **Embedded Data** ⭐ Foundation for other features
2. **Conditional Display** ⭐⭐ High priority
3. **Randomization** ⭐ Important for research

### v0.4.0 - Data Collection
4. **Response Management** ⭐⭐ Essential for data analysis

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on:
- Submitting feature requests
- Reporting bugs
- Contributing code
- Code style and testing requirements

---

## Feature Request Guidelines

When submitting a feature request, please:

1. **Check existing issues** - Search for similar requests first
2. **Use the template** - Fill in all sections thoroughly
3. **Provide examples** - Show how you'd like to use the feature
4. **Explain use cases** - Why is this feature important?
5. **Consider scope** - Is this a core feature or edge case?

### What Makes a Good Feature Request?

✅ **Good Example:**
```markdown
## Feature: Add support for question piping

### Use Case
I want to reference answers from previous questions in later question text.
For example: "You said you prefer {q1_answer}. Why is that?"

### Proposed API
api.create_text_entry_question(
    survey_id,
    "You said you prefer {QID1}. Why is that?",
    enable_piping=True
)

### Technical Details
Uses Qualtrics piped text syntax ${q://QID1/ChoiceGroup/SelectedChoices}
```

❌ **Needs Improvement:**
```markdown
## Feature: Make surveys better

### Use Case
I need better surveys

### Proposed API
Just make it work
```

---

## Issue Labels

Issues created from these templates will be automatically labeled:

- `enhancement` - New feature or improvement
- `bug` - Something isn't working
- `v0.2.0`, `v0.4.0`, etc. - Target version
- `documentation` - Documentation improvements needed
- `good first issue` - Good for newcomers

---

## Questions?

- Check the [Documentation](../../docs/)
- Open a [Discussion](https://github.com/yourusername/qualtrics-sdk/discussions)
- Contact the maintainers

---

**Last Updated:** 2024-02-01
