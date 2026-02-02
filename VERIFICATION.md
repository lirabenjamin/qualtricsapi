# Verification Instructions for Randomization Feature (#2)

This document provides instructions to verify that the randomization feature implementation is working correctly before merging to main.

## Quick Verification Checklist

- [ ] All unit tests pass
- [ ] Code imports without errors
- [ ] Example script runs (with API credentials)
- [ ] Randomization methods are available on QualtricsAPI

## 1. Run Unit Tests

The unit tests use mocks and don't require API credentials.

```bash
# Install test dependencies
pip install pytest

# Run all randomization tests
pytest tests/test_randomization.py -v

# Expected output: All tests should pass
# You should see tests for:
# - TestRandomizeBlocks (5 tests)
# - TestRandomizeQuestionsInBlock (5 tests)
# - TestRandomizeQuestionChoices (6 tests)
# - TestGetRandomizationSettings (2 tests)
```

**Expected Result:** All 18 tests should pass (integration tests are skipped by default).

## 2. Verify Code Imports

```bash
# Open Python REPL
python3

# Test imports
>>> from qualtrics_sdk import QualtricsAPI
>>>
>>> # Verify randomization methods exist
>>> hasattr(QualtricsAPI, 'randomize_blocks')
True
>>> hasattr(QualtricsAPI, 'randomize_questions_in_block')
True
>>> hasattr(QualtricsAPI, 'randomize_question_choices')
True
>>> hasattr(QualtricsAPI, 'get_randomization_settings')
True
```

**Expected Result:** All `hasattr` calls return `True`.

## 3. Run Example Script (Requires API Credentials)

If you have valid Qualtrics API credentials in your `.env` file:

```bash
# Run the randomization example
python examples/randomization_example.py
```

**Expected Output:**
- Creates a test survey
- Creates 3 blocks with questions
- Applies randomization settings
- Prints a summary of applied randomization
- Provides a survey URL to verify in Qualtrics

**Note:** This will create a real survey in your Qualtrics account. You can delete it after verification.

## 4. Manual Code Review

Check the following files for proper implementation:

### Core Implementation
- `qualtrics_sdk/core/randomization.py` - Main implementation (~300 lines)
  - `RandomizationMixin` class with 4 methods
  - Proper docstrings and type hints
  - Error handling for invalid inputs

### Integration
- `qualtrics_sdk/core/client.py` - Should import and include `RandomizationMixin`

### Tests
- `tests/test_randomization.py` - Unit tests with mocks

### Documentation
- `README.md` - Features section updated, API reference added
- `QUICK_REFERENCE.md` - Randomization examples added
- `CHANGELOG.md` - Unreleased section updated with feature

### Examples
- `examples/randomization_example.py` - Working example script

## 5. Integration Test (Optional - Requires API Credentials)

To run the full integration test:

```bash
# Ensure .env file has valid credentials
pytest tests/test_randomization.py -v -m integration
```

**Note:** This creates and deletes a real survey in your Qualtrics account.

## Summary of Changes

### New Files
1. `qualtrics_sdk/core/randomization.py` - RandomizationMixin class
2. `tests/__init__.py` - Test package init
3. `tests/test_randomization.py` - Unit tests
4. `examples/randomization_example.py` - Working example
5. `VERIFICATION.md` - This file

### Modified Files
1. `qualtrics_sdk/core/client.py` - Added RandomizationMixin to inheritance
2. `README.md` - Added features, code organization, API reference
3. `QUICK_REFERENCE.md` - Added randomization examples
4. `CHANGELOG.md` - Added unreleased changes

## Feature Summary

The implementation provides:

| Method | Description |
|--------|-------------|
| `randomize_blocks()` | Block-level randomization with even presentation and subset support |
| `randomize_questions_in_block()` | Question-level randomization within a block |
| `randomize_question_choices()` | Choice-level randomization with anchor options |
| `get_randomization_settings()` | Retrieve all randomization settings for a survey |

### Randomization Strategies Supported
- ✅ Simple randomization
- ✅ Even presentation (balanced distribution)
- ✅ Subset randomization (show N of M items)
- ✅ Anchor options (keep specific items fixed)
- ✅ Latin square / balanced designs (via `randomization_type="balanced"`)

## Merge Decision

**Merge to main if:**
- All unit tests pass (18 tests)
- Code imports without errors
- Documentation is updated correctly

**Do not merge if:**
- Any unit tests fail
- Import errors occur
- Missing documentation updates
