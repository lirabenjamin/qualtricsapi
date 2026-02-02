# Contributing to Qualtrics SDK

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Coding Standards](#coding-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation](#documentation)
8. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

### Our Pledge

Be respectful, inclusive, and collaborative. We welcome contributors of all skill levels!

### Expected Behavior

- Be kind and respectful
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Help newcomers feel welcome

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal attacks
- Publishing others' private information

---

## How Can I Contribute?

### 1. Report Bugs 🐛

Found a bug? Please report it!

**Before submitting:**
- Check if it's already reported in [Issues](../../issues)
- Make sure you're using the latest version

**Submit a bug report:**
1. Go to Issues → New Issue → Bug Report
2. Use this template:

```markdown
**Bug Description**
Clear description of what's wrong

**To Reproduce**
Steps to reproduce:
1. Call `api.create_survey(...)`
2. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- Package version: 0.1.0
- Python version: 3.10
- OS: macOS/Windows/Linux

**Additional Context**
Error messages, screenshots, etc.
```

### 2. Suggest Features ✨

Have an idea? We'd love to hear it!

**Before suggesting:**
- Check the [ROADMAP](ROADMAP.md) - might already be planned!
- Check existing feature requests

**Submit feature request:**
1. Go to Issues → New Issue → Feature Request
2. Use this template:

```markdown
**Feature Name**
Brief name for the feature

**Problem/Use Case**
What problem does this solve?

**Proposed Solution**
How should it work?

**API Design (if applicable)**
```python
# Example of how you envision using it
api.new_feature(param1, param2)
```

**Alternatives Considered**
Other ways to solve this

**Priority**
How important is this to you? (High/Medium/Low)
```

### 3. Improve Documentation 📝

Documentation is crucial! You can help by:
- Fixing typos
- Clarifying confusing sections
- Adding examples
- Translating documentation

### 4. Write Code 💻

Ready to contribute code? Awesome!

**Good first issues:**
Look for issues labeled `good first issue` - these are perfect for newcomers.

**What to work on:**
1. Check [ROADMAP](ROADMAP.md) for planned features
2. Look for `help wanted` issues
3. Ask in discussions what would be helpful

---

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub (click Fork button)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/qualtrics-sdk.git
cd qualtrics-sdk

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/qualtrics-sdk.git
```

### 2. Set Up Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Verify installation
python -c "from qualtrics_sdk import QualtricsAPI; print('Success!')"
```

### 3. Create Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions:**
- `feature/add-embedded-data` - New feature
- `bugfix/fix-slider-error` - Bug fix
- `docs/update-readme` - Documentation
- `refactor/simplify-client` - Code refactoring
- `test/add-survey-tests` - Adding tests

---

## Making Changes

### 1. Code Your Feature

```bash
# Make your changes
# Edit files in qualtrics_sdk/

# Test as you go
python examples/quick_start.py
```

### 2. Add Tests

**Every new feature needs tests!**

**File: `tests/test_your_feature.py`**
```python
import pytest
from qualtrics_sdk import QualtricsAPI

def test_your_new_feature():
    """Test description"""
    api = QualtricsAPI(token="test", data_center="test.com")
    
    # Test your feature
    result = api.your_new_method()
    
    # Assert expectations
    assert result is not None
    assert result['status'] == 'success'
```

**Run tests:**
```bash
# Run all tests
pytest

# Run your specific test
pytest tests/test_your_feature.py

# Run with coverage
pytest --cov=qualtrics_sdk
```

### 3. Update Documentation

**Update docstrings:**
```python
def your_new_method(self, param1: str, param2: int = 5) -> dict:
    """
    Brief description of what this does.
    
    Longer description with more details about the method's behavior,
    edge cases, and usage notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 5)
        
    Returns:
        Dictionary containing result data
        
    Raises:
        ValueError: If param1 is empty
        Exception: If API request fails
        
    Example:
        >>> api = QualtricsAPI(token="xxx", data_center="yyy")
        >>> result = api.your_new_method("test")
        >>> print(result['status'])
        'success'
        
    Note:
        This method requires admin permissions.
    """
    # Implementation
```

**Update README if needed:**
- Add to feature list
- Add usage example
- Update table of contents

### 4. Commit Changes

**Write good commit messages:**
```bash
# Good commit message format
git commit -m "Add embedded data support

- Implement add_embedded_data() method
- Add get_embedded_data() method
- Add tests for embedded data operations
- Update README with examples

Closes #42"
```

**Commit message guidelines:**
- First line: Brief summary (50 chars max)
- Blank line
- Detailed description (wrap at 72 chars)
- Reference related issues

**Commit types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `test:` Adding/updating tests
- `refactor:` Code change that neither fixes bug nor adds feature
- `style:` Formatting changes
- `chore:` Maintenance tasks

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications.

**Use Black for formatting:**
```bash
# Format your code
black qualtrics_sdk/

# Check what would change (don't modify)
black --check qualtrics_sdk/
```

**Use Flake8 for linting:**
```bash
# Check code quality
flake8 qualtrics_sdk/
```

### Code Style Examples

**Good:**
```python
def create_survey(
    self,
    survey_name: str,
    language: str = "EN",
    project_category: str = "CORE"
) -> Dict[str, Any]:
    """Create a new survey."""
    
    if not survey_name:
        raise ValueError("survey_name cannot be empty")
    
    survey_data = {
        "SurveyName": survey_name,
        "Language": language,
        "ProjectCategory": project_category
    }
    
    response = requests.post(
        f'{self.base_url}/survey-definitions',
        headers=self.headers,
        json=survey_data
    )
    
    if response.status_code == 200:
        return response.json()['result']
    else:
        raise Exception(f"Failed to create survey: {response.text}")
```

**Bad:**
```python
def create_survey(self,survey_name,language="EN"):  # No type hints
    surveyData={"SurveyName":survey_name,"Language":language}  # Bad naming
    r=requests.post(self.base_url+'/survey-definitions',headers=self.headers,json=surveyData)  # Too long
    return r.json()['result']  # No error handling
```

### Type Hints

Always use type hints:
```python
from typing import Dict, List, Optional, Any

def create_question(
    self,
    survey_id: str,
    question_text: str,
    choices: List[str],
    required: bool = False
) -> Dict[str, Any]:
    """Create a question."""
    pass
```

### Error Handling

Always handle errors gracefully:
```python
def api_call(self):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
```

---

## Testing Guidelines

### Test Coverage

- Aim for **80%+ coverage** minimum
- Test happy paths AND error cases
- Test edge cases and boundary conditions

### Test Structure

```python
# Organize tests by feature
tests/
├── test_surveys.py          # Survey operations
├── test_questions.py        # Question operations
├── test_embedded_data.py    # Embedded data
└── test_utils.py            # Utility functions

# Use descriptive test names
def test_create_survey_with_valid_name():
    """Test survey creation with valid name succeeds"""
    
def test_create_survey_with_empty_name_raises_error():
    """Test survey creation with empty name raises ValueError"""
    
def test_create_survey_with_special_characters():
    """Test survey creation handles special characters correctly"""
```

### Testing Best Practices

**Use fixtures for common setup:**
```python
@pytest.fixture
def api_client():
    """Create API client for testing"""
    return QualtricsAPI(token="test", data_center="test.com")

def test_create_survey(api_client):
    """Test with fixture"""
    result = api_client.create_survey("Test")
    assert result is not None
```

**Mock external API calls:**
```python
from unittest.mock import Mock, patch

@patch('requests.post')
def test_create_survey_api_call(mock_post):
    """Test API call is made correctly"""
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        'result': {'SurveyID': 'SV_123'}
    }
    
    api = QualtricsAPI(token="test", data_center="test.com")
    result = api.create_survey("Test")
    
    assert result['SurveyID'] == 'SV_123'
    mock_post.assert_called_once()
```

---

## Documentation

### What to Document

1. **Code (docstrings)** - Every public function
2. **README** - Overview and quick start
3. **Examples** - Working code samples
4. **API Reference** - Detailed function docs
5. **Guides** - How-to tutorials

### Documentation Standards

- Use clear, simple language
- Include examples for complex features
- Link to related documentation
- Keep documentation up-to-date with code

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Tests pass: `pytest`
- [ ] Code formatted: `black qualtrics_sdk/`
- [ ] Code linted: `flake8 qualtrics_sdk/`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for features/fixes)
- [ ] No merge conflicts with main
- [ ] Commits are clean and well-described

### Submitting PR

1. **Push your branch:**
```bash
git push origin feature/your-feature-name
```

2. **Create Pull Request on GitHub:**
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Fill out the template

3. **PR Description Template:**
```markdown
## Description
Brief summary of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Related Issues
Closes #42
Related to #38

## Changes Made
- Added `add_embedded_data()` method
- Added tests for embedded data
- Updated README with examples

## Testing
Describe how you tested this:
- Added unit tests
- Tested with real Qualtrics API
- Verified examples work

## Checklist
- [x] Tests pass
- [x] Code follows style guidelines
- [x] Documentation updated
- [x] No breaking changes (or documented if so)
```

### Review Process

1. **Automated checks** run (tests, linting)
2. **Maintainer reviews** your code
3. **Feedback** may be provided - address it!
4. **Approval** - PR gets merged!

### After PR is Merged

```bash
# Update your local main
git checkout main
git pull upstream main

# Delete your feature branch
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

---

## Questions?

- **General questions:** Open a [Discussion](../../discussions)
- **Bug reports:** Open an [Issue](../../issues)
- **Feature ideas:** Check [ROADMAP](ROADMAP.md) first, then open an issue
- **Development help:** Read [DEVELOPMENT.md](DEVELOPMENT.md)

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in our hearts ❤️

Thank you for contributing!
