# Project Organization Guide

A complete guide to understanding how this project is structured and organized.

## Quick Navigation

- **New to the project?** Start with [README.md](../README.md)
- **Want to contribute?** Read [CONTRIBUTING.md](CONTRIBUTING.md)
- **Looking for features?** Check [ROADMAP.md](ROADMAP.md)
- **Need dev help?** See [DEVELOPMENT.md](DEVELOPMENT.md)

---

## Directory Structure

```
qualtricsapi/                   # Project root
│
├── qualtrics_sdk/              # 📦 MAIN PACKAGE (your code)
│   ├── __init__.py            #    Package initialization, version info
│   ├── core/                  #    Core functionality
│   │   ├── __init__.py
│   │   └── client.py          #    Main API client class
│   ├── models/                #    Data models (future)
│   │   └── __init__.py
│   └── utils/                 #    Utility functions (future)
│       └── __init__.py
│
├── examples/                   # 📚 EXAMPLE SCRIPTS
│   ├── quick_start.py         #    Simple usage example
│   └── comprehensive_example.py    Complete feature demo
│
├── tests/                      # 🧪 TESTS
│   └── test_client.py         #    Unit tests
│
├── docs/                       # 📖 DOCUMENTATION
│   ├── DEVELOPMENT.md         #    Development guide (versioning, releases)
│   ├── ROADMAP.md             #    Feature roadmap and plans
│   ├── CONTRIBUTING.md        #    How to contribute
│   ├── PROJECT_ORGANIZATION.md#    This file
│   └── SECURITY.md            #    Security best practices
│
├── venv/                       # 🐍 VIRTUAL ENVIRONMENT (not in git)
│   └── ...                    #    Python dependencies installed here
│
├── .github/                    # ⚙️ GITHUB CONFIG (future)
│   ├── workflows/             #    CI/CD automation
│   └── ISSUE_TEMPLATE/        #    Issue templates
│
├── setup.py                    # 📋 PACKAGE SETUP (installation config)
├── pyproject.toml             # 📋 MODERN PYTHON CONFIG
├── requirements.txt           # 📋 DEPENDENCIES LIST
├── MANIFEST.in                # 📋 PACKAGE MANIFEST
│
├── README.md                   # 📄 MAIN DOCUMENTATION
├── CHANGELOG.md               # 📄 VERSION HISTORY
├── LICENSE                    # 📄 MIT LICENSE
├── QUICK_REFERENCE.md         # 📄 QUICK REFERENCE GUIDE
│
├── .env                       # 🔒 YOUR CREDENTIALS (not in git!)
├── .env.example               # 📄 CREDENTIALS TEMPLATE (safe to share)
└── .gitignore                 # 🚫 FILES TO IGNORE IN GIT
```

---

## What Each Directory Does

### `/qualtrics_sdk/` - The Main Package

This is where all the actual code lives. When someone installs your package with `pip install`, they get this directory.

**Files:**
- `__init__.py` - Makes this a Python package. Exports the public API.
- `core/client.py` - Main `QualtricsAPI` class with all methods

**Future expansion:**
```
qualtrics_sdk/
├── core/
│   ├── client.py          # Main API client
│   ├── responses.py       # Response handling
│   └── distributions.py   # Distribution management
├── models/
│   ├── survey.py          # Survey data models
│   ├── question.py        # Question data models
│   └── embedded_data.py   # Embedded data models
└── utils/
    ├── validators.py      # Input validation
    ├── formatters.py      # Data formatting
    └── helpers.py         # Helper functions
```

### `/examples/` - Example Scripts

Working code that shows users how to use your package.

**Current:**
- `quick_start.py` - Simple 5-minute example
- `comprehensive_example.py` - All features demo

**Future examples:**
- `embedded_data_example.py`
- `survey_flow_example.py`
- `batch_operations_example.py`
- `advanced_questions_example.py`

### `/tests/` - Automated Tests

Unit tests to ensure code works correctly.

**Structure:**
```
tests/
├── test_client.py         # Test main client
├── test_surveys.py        # Test survey operations
├── test_questions.py      # Test question operations
├── test_embedded_data.py  # Test embedded data (future)
├── conftest.py            # Pytest configuration
└── fixtures/              # Test data files
    └── sample_survey.json
```

### `/docs/` - Documentation

Extended documentation beyond the README.

**Current files:**
- `DEVELOPMENT.md` - How to develop and release
- `ROADMAP.md` - Future plans
- `CONTRIBUTING.md` - Contribution guide
- `PROJECT_ORGANIZATION.md` - This file
- `SECURITY.md` - Security practices

**Future additions:**
- API reference (generated from docstrings)
- Tutorials and guides
- Use case examples
- Architecture diagrams

---

## Configuration Files

### `setup.py` - Package Installation

Tells Python how to install your package.

**Key sections:**
```python
setup(
    name="qualtrics-sdk",           # Package name
    version="0.1.0",                # Current version
    packages=find_packages(),        # Auto-find all packages
    install_requires=[...],          # Dependencies
    python_requires=">=3.8",         # Minimum Python version
)
```

### `pyproject.toml` - Modern Python Configuration

Modern way to configure Python projects. Includes:
- Package metadata
- Dependencies
- Build system config
- Tool configurations (Black, Pytest, Mypy)

### `requirements.txt` - Dependency List

Simple list of dependencies:
```
requests>=2.25.0
python-dotenv>=0.19.0
```

### `.gitignore` - Files NOT in Version Control

Tells Git to ignore certain files:
```
.env              # Your credentials
venv/             # Virtual environment
__pycache__/      # Python cache
*.pyc             # Compiled Python
.DS_Store         # Mac OS files
```

---

## File Naming Conventions

### Python Files
- `lowercase_with_underscores.py` - Python modules
- `test_*.py` - Test files (must start with test_)
- `__init__.py` - Package initialization

### Documentation
- `UPPERCASE.md` - Important docs (README, LICENSE, CHANGELOG)
- `PascalCase.md` - Guide docs (CONTRIBUTING, DEVELOPMENT)

### Example Files
- `descriptive_name.py` - Clear, descriptive names
- `quick_start.py` ✓ Good
- `example1.py` ✗ Bad (not descriptive)

---

## Import Structure

### How Imports Work

```python
# When you do this:
from qualtrics_sdk import QualtricsAPI

# Python looks for:
# 1. qualtrics_sdk/__init__.py (reads this first)
# 2. Imports QualtricsAPI from that file
# 3. QualtricsAPI is imported from core/client.py
```

### Package `__init__.py`
```python
# qualtrics_sdk/__init__.py
"""Qualtrics SDK - Python wrapper for Qualtrics API"""

__version__ = "0.1.0"

# Import main API class
from qualtrics_sdk.core.client import QualtricsAPI

# Export public API
__all__ = ["QualtricsAPI"]
```

### In Your Code
```python
# User code
from qualtrics_sdk import QualtricsAPI

api = QualtricsAPI(token="xxx", data_center="yyy")
api.create_survey("My Survey")
```

---

## Development Workflow

### 1. Making Changes

```
┌──────────────┐
│ Create Branch│
└──────┬───────┘
       │
       v
┌──────────────┐
│  Make Changes│
└──────┬───────┘
       │
       v
┌──────────────┐
│  Write Tests │
└──────┬───────┘
       │
       v
┌──────────────┐
│ Update Docs  │
└──────┬───────┘
       │
       v
┌──────────────┐
│    Commit    │
└──────┬───────┘
       │
       v
┌──────────────┐
│ Create PR    │
└──────────────┘
```

### 2. Release Process

```
┌──────────────────┐
│ Update Version   │
│ - __init__.py    │
│ - pyproject.toml │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Update CHANGELOG │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Commit & Tag     │
│ git tag v0.2.0   │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ GitHub Release   │
└────────┬─────────┘
         │
         v
┌──────────────────┐
│ Publish to PyPI  │
│ (optional)       │
└──────────────────┘
```

---

## File Relationships

### Code Flow

```
User's Script
     │
     │ imports
     ├─────────────────> qualtrics_sdk/__init__.py
     │                        │
     │                        │ imports
     │                        └────────────> core/client.py
     │                                            │
     │                                            │ contains
     │                                            └────────> QualtricsAPI class
     │
     │ calls
     └─────────────────> api.create_survey()
```

### Documentation Flow

```
User arrives at project
     │
     └─> README.md (start here)
           │
           ├─> Quick Start?
           │     └─> examples/quick_start.py
           │
           ├─> Want to contribute?
           │     └─> docs/CONTRIBUTING.md
           │           └─> docs/DEVELOPMENT.md
           │
           ├─> What's planned?
           │     └─> docs/ROADMAP.md
           │
           └─> Need API details?
                 └─> QUICK_REFERENCE.md
                       └─> README.md API section
```

---

## Version Control Strategy

### Branch Structure

```
main                     # Production-ready code
  │
  ├─ feature/*          # New features
  │    ├─ feature/embedded-data
  │    └─ feature/survey-flow
  │
  ├─ bugfix/*           # Bug fixes
  │    └─ bugfix/slider-error
  │
  ├─ hotfix/*           # Emergency fixes
  │    └─ hotfix/critical-auth
  │
  └─ docs/*             # Documentation updates
       └─ docs/improve-readme
```

### Tag Strategy

```
v0.1.0     # Initial release
v0.1.1     # Patch release (bug fix)
v0.2.0     # Minor release (new features)
v1.0.0     # Major release (stable API)
```

---

## Adding New Features

### Example: Adding Embedded Data Support

#### 1. Create Feature Branch
```bash
git checkout -b feature/embedded-data
```

#### 2. Add Code
**File: `qualtrics_sdk/core/client.py`**
```python
def add_embedded_data(self, survey_id: str, fields: Dict[str, str]) -> bool:
    """Add embedded data fields to survey."""
    # Implementation
```

#### 3. Add Tests
**File: `tests/test_embedded_data.py`**
```python
def test_add_embedded_data():
    """Test adding embedded data"""
    # Test implementation
```

#### 4. Update Documentation
- Add to README.md features list
- Add example to `examples/embedded_data_example.py`
- Update CHANGELOG.md

#### 5. Commit and PR
```bash
git add .
git commit -m "Add embedded data support"
git push origin feature/embedded-data
```

---

## Best Practices

### Code Organization
✅ **DO:**
- Keep related code together
- Use clear, descriptive names
- Follow the existing structure
- Add tests for new features
- Update documentation

❌ **DON'T:**
- Put everything in one file
- Use cryptic names
- Skip tests
- Forget documentation
- Mix concerns (separate API calls from business logic)

### File Organization
✅ **DO:**
- One main class per file (usually)
- Group related functionality
- Use subpackages for major features
- Keep files focused and manageable (<500 lines)

❌ **DON'T:**
- Create 5000-line files
- Mix unrelated functionality
- Create unnecessarily deep nesting
- Duplicate code across files

---

## Summary

### Quick Orientation

**I want to...**
- **Use the SDK** → See `examples/`
- **Contribute code** → Read `docs/CONTRIBUTING.md`
- **Understand development** → Read `docs/DEVELOPMENT.md`
- **See what's planned** → Read `docs/ROADMAP.md`
- **Report a bug** → Create GitHub Issue
- **Suggest a feature** → Check ROADMAP, then create Issue

### Key Files to Know

1. `README.md` - Start here
2. `qualtrics_sdk/core/client.py` - Main code
3. `docs/DEVELOPMENT.md` - Development guide
4. `docs/ROADMAP.md` - Future plans
5. `CHANGELOG.md` - What's changed

---

**Questions?** Open an issue or start a discussion!
