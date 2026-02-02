# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Embedded data support
- Survey flow management
- Loop and merge functionality
- Custom JavaScript for questions
- Distribution management
- Response data retrieval

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
