# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Embedded data support** (#1)
  - `set_embedded_data()` - Configure individual embedded data fields with type specifications (text, number, date)
  - `set_embedded_data_fields()` - Configure multiple fields simultaneously via dictionary, with `position` parameter for flow placement ("start" or "end")
  - `get_embedded_data()` - Retrieve all embedded data fields configured in a survey
  - `delete_embedded_data()` - Delete an embedded data field from a survey
  - `get_survey_url_with_embedded_data()` - Generate survey links pre-populated with embedded data values
  - `get_survey_flow()` - Retrieve the full survey flow structure
  - Support for dynamic values: random numbers (`${rand://int/min:max}`), piped text from questions (`${q://QID/ChoiceTextEntryValue}`), dates, etc.
- New `EmbeddedDataMixin` module following the existing mixin pattern
- Example file: `examples/embedded_data_example.py` with 5 comprehensive examples
- Unit tests for embedded data functionality (17 tests)

### Planned
- Survey flow management
- Loop and merge functionality
- Custom JavaScript for questions
- Distribution management
- Response data retrieval

## [0.2.0] - 2026-02-02

### Added
- **Conditional Display / Display Logic Support** (#3)
  - `add_display_logic()` - Add single condition display logic to questions
  - `add_display_logic_multiple()` - Add multiple conditions with AND/OR operators
  - `show_only_if()` - Helper method for clearer display logic
  - `skip_if()` - Helper method for skip logic (inverse display logic)
  - `add_embedded_data_logic()` - Display logic based on embedded data fields
  - `get_display_logic()` - Retrieve display logic for a question
  - `delete_display_logic()` - Remove display logic from a question
  - `add_page_break()` - Helper method to add page breaks before conditional questions
- New `DisplayLogicMixin` class in modular architecture
- Supported operators: Selected, NotSelected, EqualTo, NotEqualTo, GreaterThan, LessThan, GreaterOrEqual, LessOrEqual, Contains, DoesNotContain, MatchesRegex, Empty, NotEmpty, Displayed, NotDisplayed
- Example scripts:
  - `display_logic_example.py` - Comprehensive display logic demonstrations
  - `debug_display_logic.py` - Diagnostic tool for testing display logic
  - `compare_logic.py` - Tool to compare display logic structures
  - `delete_surveys.py` - Batch delete test surveys

### Fixed
- Display logic now works correctly in live surveys (not just in API responses)
- Added required `DataExportTag` field when updating questions with display logic
- Added `QuestionIDFromLocator` and `LeftOperand` fields to display logic conditions to match Qualtrics API expectations
- Added `ChoiceOrder` to multiple choice questions (was missing, now properly included)
- Fixed `Conjunction` spelling and capitalization (now "And"/"Or" instead of "AND"/"OR")
- Removed invalid `Description` field from display logic structure
- Fixed slider questions to only show min/max labels by setting `GridLines: 0`
- Updated display logic example to use separate blocks for proper page breaks

### Changed
- Updated `QualtricsAPI` client to include `DisplayLogicMixin`
- Multiple choice questions now include `ChoiceOrder` field
- Display logic example now creates questions in separate blocks for automatic page breaks
- Slider questions now have cleaner formatting with only min/max labels visible

## [0.1.0] - 2026-02-01

### Added
- Initial release of Qualtrics SDK
- Survey operations (create, read, update, delete, list)
- Question types:
  - Multiple choice (radio buttons, dropdown lists)
  - Text entry (single-line and multi-line/essay)
  - Matrix/Likert scale questions
  - Slider questions
  - Rank order (drag and drop)
  - Net Promoter Score (NPS)
  - Descriptive text blocks
- Question management operations (create, update, delete, get)
- Block operations (create, get blocks)
- Secure credential management via .env file
- Comprehensive documentation:
  - README.md with full API reference
  - QUICK_REFERENCE.md for common operations
  - SECURITY.md for best practices
  - Example scripts (quick_start.py, comprehensive_example.py)
- Python package structure with setup.py and pyproject.toml
- Development guides:
  - DEVELOPMENT.md - Complete development guide
  - ROADMAP.md - Feature roadmap and future plans
  - CONTRIBUTING.md - Contribution guidelines
  - CODE_ORGANIZATION.md - Modular design explanation
  - REFACTORING_PLAN.md - Code organization guide
  - claude.md - Complete project context for AI

### Changed
- **Refactored monolithic client.py (629 lines) into modular structure**
  - Split into 6 focused modules using mixin pattern
  - base.py (32 lines) - Core API and authentication
  - surveys.py (150 lines) - Survey CRUD operations
  - questions.py (395 lines) - All question type creation
  - question_management.py (124 lines) - Question management
  - blocks.py (60 lines) - Block operations
  - client.py (44 lines) - Combines all mixins
- Improved code organization and maintainability
- Zero breaking changes - all imports work identically

### Security
- API credentials stored in .env file (not in code)
- .env included in .gitignore
- .env.example template provided

### Documentation
- Complete API documentation with docstrings
- Usage examples for all question types
- Security best practices guide
- Development workflow documentation
- Semantic versioning guide
- Issue tracking guide
- Release process documentation

---

## Changelog Format

### Types of Changes

- **Added** - New features
- **Changed** - Changes in existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Now removed features
- **Fixed** - Bug fixes
- **Security** - Security updates

### Version Header Format

```markdown
## [Version] - YYYY-MM-DD

### Added
- Feature description

### Fixed
- Bug fix description
```

---

## How to Update This File

When making a release:

1. **Move items from [Unreleased] to new version section**
2. **Add version number and date**
3. **Categorize changes** (Added, Changed, Fixed, etc.)
4. **Link issues** using `(#issue-number)`

Example:
```markdown
## [0.2.0] - 2026-03-01

### Added
- Embedded data support (#42)
- New `add_embedded_data()` method
- New `get_embedded_data()` method

### Fixed
- Slider question range validation (#45)
- NPS question export tag generation (#47)

### Changed
- Improved error messages for API failures
```

---

## Version Links

[Unreleased]: https://github.com/yourusername/qualtrics-sdk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/qualtrics-sdk/releases/tag/v0.1.0
