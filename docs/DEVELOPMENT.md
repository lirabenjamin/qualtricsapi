# Development Guide - Understanding Software Development Basics

This guide teaches you everything you need to know about developing, versioning, releasing, and maintaining a Python package.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Version Numbering (Semantic Versioning)](#version-numbering-semantic-versioning)
3. [Development Workflow](#development-workflow)
4. [Issue Tracking](#issue-tracking)
5. [Making Releases](#making-releases)
6. [Testing](#testing)
7. [Documentation](#documentation)
8. [Git Best Practices](#git-best-practices)

---

## Project Structure

### What is a Python Package?

A Python package is a way to organize related code into a reusable module that others (or you) can install and import.

### Our Package Structure

```
qualtricsapi/
├── qualtrics_sdk/              # Main package directory
│   ├── __init__.py            # Makes this a package, exports main API
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   └── client.py          # Main API client
│   ├── models/                # Data models (future)
│   │   └── __init__.py
│   └── utils/                 # Utility functions (future)
│       └── __init__.py
├── examples/                   # Example scripts
│   ├── quick_start.py
│   └── comprehensive_example.py
├── tests/                      # Unit tests
│   └── test_client.py
├── docs/                       # Documentation
│   ├── DEVELOPMENT.md         # This file
│   ├── ROADMAP.md             # Future plans
│   └── CONTRIBUTING.md        # How to contribute
├── setup.py                    # Package installation config
├── pyproject.toml             # Modern Python project config
├── requirements.txt           # Dependencies
├── .env.example               # Template for environment variables
├── .gitignore                 # Files to ignore in git
├── README.md                  # Main documentation
├── CHANGELOG.md               # Version history
├── LICENSE                    # Software license
└── MANIFEST.in                # Files to include in distribution

```

### Why This Structure?

- **qualtrics_sdk/**: Your actual code goes here. This is what users import.
- **examples/**: Show users how to use your package
- **tests/**: Automated tests to ensure code works correctly
- **docs/**: Extended documentation beyond README
- **setup.py & pyproject.toml**: Tell Python how to install your package

---

## Version Numbering (Semantic Versioning)

### Format: MAJOR.MINOR.PATCH (e.g., 1.2.3)

```
1.2.3
│ │ │
│ │ └─ PATCH: Bug fixes, no new features (1.2.3 → 1.2.4)
│ └─── MINOR: New features, backward compatible (1.2.3 → 1.3.0)
└───── MAJOR: Breaking changes, not backward compatible (1.2.3 → 2.0.0)
```

### Version Stages

#### Pre-1.0.0: Initial Development (We are here!)
- **0.1.0** - First working version
- **0.2.0** - Added new features
- **0.3.0** - More features
- Not stable yet, breaking changes OK

#### 1.0.0: First Stable Release
- Public API is stable
- Ready for production use
- From now on, follow semantic versioning strictly

### When to Bump Versions

#### PATCH (0.1.0 → 0.1.1)
- Fixed a bug
- Improved documentation
- Minor internal changes
- No new features, no breaking changes

**Example:**
```
0.1.0: Initial release
0.1.1: Fixed slider question bug
0.1.2: Fixed NPS question error handling
```

#### MINOR (0.1.5 → 0.2.0)
- Added new features
- Added new question types
- Enhanced existing functionality
- Backward compatible (old code still works)

**Example:**
```
0.1.5: Bug fixes
0.2.0: Added embedded data support ✨ NEW FEATURE
0.3.0: Added randomization support ✨ NEW FEATURE
```

#### MAJOR (0.9.0 → 1.0.0 or 1.5.0 → 2.0.0)
- Breaking changes
- Changed function signatures
- Removed features
- Requires users to update their code

**Example:**
```
0.9.0: Feature complete, ready for 1.0
1.0.0: First stable release! 🎉
1.5.0: Many features added
2.0.0: Rewrote API, breaking changes ⚠️
```

### Pre-release Versions

For testing before official release:

```
1.0.0-alpha.1   # Very early, might crash
1.0.0-beta.1    # Feature complete, testing phase
1.0.0-rc.1      # Release candidate, almost ready
1.0.0           # Official release!
```

---

## Development Workflow

### 1. Set Up Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd qualtricsapi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode (editable)
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

**What is `-e .`?**
- Installs your package in "editable" mode
- Changes to code are immediately available
- No need to reinstall after each change

### 2. Make Changes

```bash
# Create a new branch for your feature
git checkout -b feature/add-embedded-data

# Make your changes
# Edit files in qualtrics_sdk/

# Test your changes
python examples/quick_start.py
pytest tests/

# Commit your changes
git add .
git commit -m "Add embedded data support"
```

### 3. Test Before Committing

```bash
# Run tests
pytest

# Check code style
black qualtrics_sdk/
flake8 qualtrics_sdk/

# Type checking
mypy qualtrics_sdk/
```

### 4. Push and Create Pull Request

```bash
git push origin feature/add-embedded-data
# Then create Pull Request on GitHub
```

---

## Issue Tracking

### What are Issues?

Issues are how you track:
- **Bugs**: Something is broken
- **Features**: Something new to add
- **Enhancements**: Improve existing features
- **Documentation**: Update docs

### Creating Good Issues

#### Bug Report Template
```markdown
**Title:** Slider question fails with min_value > 0

**Description:**
When creating a slider question with min_value > 0, the API returns an error.

**Steps to Reproduce:**
1. Call `api.create_slider_question(survey_id, "Q1", min_value=10, max_value=100)`
2. API returns 400 error

**Expected Behavior:**
Slider should be created with range 10-100

**Actual Behavior:**
API error: "Invalid range"

**Environment:**
- Package version: 0.1.0
- Python version: 3.10
- OS: macOS
```

#### Feature Request Template
```markdown
**Title:** Add support for embedded data

**Description:**
Need ability to add embedded data fields to surveys

**Use Case:**
Want to track user ID, session info, etc.

**Proposed API:**
```python
api.add_embedded_data(survey_id, {
    "user_id": "12345",
    "source": "email"
})
```
```

### Issue Labels

Organize issues with labels:
- `bug` - Something is broken
- `enhancement` - Improve existing feature
- `feature` - New feature request
- `documentation` - Documentation improvements
- `good first issue` - Easy for beginners
- `help wanted` - Need community help
- `priority: high` - Do this soon
- `priority: low` - Nice to have

---

## Making Releases

### Release Checklist

#### 1. Update Version Number

**File: `qualtrics_sdk/__init__.py`**
```python
__version__ = "0.2.0"  # Changed from 0.1.0
```

**File: `pyproject.toml`**
```toml
version = "0.2.0"  # Changed from 0.1.0
```

#### 2. Update CHANGELOG.md

```markdown
# Changelog

## [0.2.0] - 2026-02-15

### Added
- Embedded data support
- New `add_embedded_data()` method
- Examples for embedded data usage

### Fixed
- Slider question bug with custom ranges
- NPS question export tag issue

### Changed
- Improved error messages

## [0.1.0] - 2026-02-01

### Added
- Initial release
- Basic survey operations
- All major question types
```

#### 3. Commit Changes

```bash
git add .
git commit -m "Release version 0.2.0"
git push origin main
```

#### 4. Create Git Tag

```bash
# Create annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0 - Added embedded data support"

# Push tag to remote
git push origin v0.2.0
```

#### 5. Create GitHub Release

1. Go to GitHub → Releases → "Draft a new release"
2. Choose tag: v0.2.0
3. Release title: "v0.2.0 - Embedded Data Support"
4. Description: Copy from CHANGELOG.md
5. Publish release

#### 6. Build and Publish Package (Optional - for PyPI)

```bash
# Install build tools
pip install build twine

# Build distribution files
python -m build

# Test upload to TestPyPI first
twine upload --repository testpypi dist/*

# Upload to real PyPI
twine upload dist/*
```

Now users can install with:
```bash
pip install qualtrics-sdk
```

### Release Types

#### Hotfix Release (Emergency Bug Fix)
```
v1.2.3 (has critical bug) → v1.2.4 (urgent fix)
```

**Process:**
1. Create hotfix branch from main
2. Fix bug
3. Test thoroughly
4. Bump PATCH version
5. Release immediately

#### Regular Release (Planned Features)
```
v1.2.4 → v1.3.0 (new features from roadmap)
```

**Process:**
1. Develop features in feature branches
2. Merge to main when ready
3. Test everything
4. Bump MINOR version
5. Release on schedule (e.g., monthly)

#### Major Release (Breaking Changes)
```
v1.9.5 → v2.0.0 (API redesign)
```

**Process:**
1. Announce breaking changes in advance
2. Provide migration guide
3. Bump MAJOR version
4. Release with detailed notes

---

## Testing

### Why Test?

- Catch bugs before users do
- Ensure new code doesn't break old code
- Document expected behavior
- Enable confident refactoring

### Test Structure

**File: `tests/test_client.py`**
```python
import pytest
from qualtrics_sdk import QualtricsAPI

def test_create_survey():
    """Test survey creation"""
    api = QualtricsAPI(api_token="test", data_center="test.qualtrics.com")
    # Test code here
    
def test_create_question():
    """Test question creation"""
    # Test code here
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=qualtrics_sdk

# Run specific test file
pytest tests/test_client.py

# Run specific test
pytest tests/test_client.py::test_create_survey
```

### Test Coverage

Aim for:
- **80%+ code coverage** - Good
- **90%+ code coverage** - Excellent
- **100% code coverage** - Overkill, but possible

---

## Documentation

### Types of Documentation

1. **README.md** - Quick start and overview
2. **API Reference** - Detailed function descriptions (docstrings)
3. **Guides** - How to accomplish tasks
4. **Examples** - Working code samples
5. **CHANGELOG** - What changed in each version

### Writing Good Docstrings

```python
def create_survey(self, survey_name: str, language: str = "EN") -> Dict[str, Any]:
    """
    Create a new survey in Qualtrics.
    
    Args:
        survey_name: Name of the survey (required)
        language: Survey language code (default: "EN")
        
    Returns:
        Dictionary containing survey details including 'SurveyID'
        
    Raises:
        Exception: If API request fails
        
    Example:
        >>> api = QualtricsAPI(token="xxx", data_center="yyy")
        >>> survey = api.create_survey("Customer Feedback")
        >>> print(survey['SurveyID'])
        'SV_xxxx'
    """
    # Implementation
```

---

## Git Best Practices

### Branch Naming

```
feature/add-embedded-data       # New feature
bugfix/fix-slider-range         # Bug fix
hotfix/critical-auth-issue      # Emergency fix
docs/update-readme              # Documentation
refactor/simplify-client        # Code cleanup
```

### Commit Messages

#### Good Commit Messages
```
Add embedded data support

- Implement add_embedded_data() method
- Add tests for embedded data
- Update documentation with examples

Fixes #42
```

#### Bad Commit Messages
```
fixed stuff
update
asdf
wip
```

### Commit Message Format

```
<type>: <short summary> (50 chars or less)

<detailed description if needed>

<footer with issue references>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding tests
- `refactor`: Code cleanup, no behavior change
- `style`: Formatting, no code change
- `chore`: Maintenance tasks

---

## Quick Reference

### Development Commands

```bash
# Install for development
pip install -e ".[dev]"

# Run examples
python examples/quick_start.py

# Run tests
pytest

# Check code style
black qualtrics_sdk/
flake8 qualtrics_sdk/

# Build package
python -m build

# Install locally
pip install .
```

### Release Commands

```bash
# Update version in code
# Edit qualtrics_sdk/__init__.py and pyproject.toml

# Update CHANGELOG.md

# Commit and tag
git add .
git commit -m "Release v0.2.0"
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin main --tags
```

### Version Decision Tree

```
Did you break backward compatibility?
  YES → Bump MAJOR version (1.x.x → 2.0.0)
  NO  → Continue...

Did you add new features?
  YES → Bump MINOR version (1.2.x → 1.3.0)
  NO  → Continue...

Did you only fix bugs or update docs?
  YES → Bump PATCH version (1.2.3 → 1.2.4)
```

---

## Next Steps

1. Read [ROADMAP.md](ROADMAP.md) for planned features
2. Read [CONTRIBUTING.md](CONTRIBUTING.md) to start contributing
3. Check out [GitHub Issues](issues) for tasks to work on
4. Join discussions on feature requests

---

**Remember:** Good software development is about:
- Clear organization
- Consistent versioning
- Thorough testing
- Great documentation
- Community collaboration

Take your time, follow the practices, and your project will grow sustainably!
