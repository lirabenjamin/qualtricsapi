# Code Organization Strategy

## Current vs Proposed Structure

### Current (Monolithic)
```
qualtrics_sdk/core/client.py (600+ lines)
└── QualtricsAPI class
    ├── Survey operations (create, get, delete, list, update)
    ├── Question operations (9 types × create methods)
    ├── Question management (update, delete, get)
    ├── Block operations
    └── Helper methods
```

### Proposed (Modular with Mixins)
```
qualtrics_sdk/
├── core/
│   ├── base.py              # Base API client (auth, requests)
│   ├── surveys.py           # Survey CRUD operations
│   ├── questions.py         # Question creation (all types)
│   ├── question_management.py # Question update/delete/get
│   ├── blocks.py            # Block operations
│   └── client.py            # Main client (combines all mixins)
├── models/
│   ├── survey.py            # Survey data models (future)
│   └── question.py          # Question data models (future)
└── utils/
    ├── validators.py        # Input validation (future)
    └── helpers.py           # Helper functions (future)
```

## Design Pattern: Mixins

### What are Mixins?

Mixins are a way to share functionality between classes. Instead of one huge class, we create small, focused classes that each handle one responsibility.

### Benefits

1. **Separation of Concerns** - Each file has one clear purpose
2. **Easier to Navigate** - Find survey methods in surveys.py
3. **Easier to Test** - Test each module independently
4. **Easier to Extend** - Add new features in new files
5. **Better Collaboration** - Multiple people can work on different modules
6. **Clearer Code Reviews** - Smaller files, focused changes

### How It Works

```python
# base.py - Core API functionality
class APIBase:
    def __init__(self, api_token, data_center):
        self.api_token = api_token
        self.base_url = f'https://{data_center}/API/v3'
        # ...
    
    def _make_request(self, method, endpoint, data=None):
        """Internal method for making API requests"""
        # Shared request logic
        pass

# surveys.py - Survey operations mixin
class SurveyMixin:
    """Mixin for survey operations"""
    
    def create_survey(self, survey_name, ...):
        """Create a survey"""
        # Implementation
        pass
    
    def get_survey(self, survey_id):
        """Get survey"""
        pass
    
    def delete_survey(self, survey_id):
        """Delete survey"""
        pass

# questions.py - Question creation mixin
class QuestionMixin:
    """Mixin for creating questions"""
    
    def create_multiple_choice_question(self, ...):
        """Create MC question"""
        pass
    
    def create_text_entry_question(self, ...):
        """Create text question"""
        pass

# client.py - Combine everything
class QualtricsAPI(APIBase, SurveyMixin, QuestionMixin, ...):
    """Main API client combining all functionality"""
    pass
```

## Module Responsibilities

### 1. `base.py` - Base API Client
**Purpose:** Core API communication  
**Size:** ~100 lines

**Responsibilities:**
- Initialize connection (token, data center, headers)
- Make HTTP requests (GET, POST, PUT, DELETE)
- Handle errors
- Parse responses

**Methods:**
- `__init__(api_token, data_center)`
- `_make_request(method, endpoint, data=None)`
- `_handle_response(response)`
- `_handle_error(error)`

---

### 2. `surveys.py` - Survey Operations
**Purpose:** Survey CRUD operations  
**Size:** ~150 lines

**Responsibilities:**
- Create surveys
- Get survey details
- Update surveys
- Delete surveys
- List surveys
- Get survey URL

**Methods:**
- `create_survey(survey_name, language, project_category)`
- `get_survey(survey_id)`
- `update_survey_name(survey_id, new_name)`
- `delete_survey(survey_id)`
- `list_surveys()`
- `get_survey_url(survey_id)`

---

### 3. `questions.py` - Question Creation
**Purpose:** Creating all types of questions  
**Size:** ~400 lines (largest module)

**Responsibilities:**
- Create multiple choice questions
- Create text entry questions
- Create matrix questions
- Create slider questions
- Create rank order questions
- Create NPS questions
- Create descriptive text

**Methods:**
- `create_multiple_choice_question(...)`
- `create_text_entry_question(...)`
- `create_matrix_question(...)`
- `create_slider_question(...)`
- `create_rank_order_question(...)`
- `create_nps_question(...)`
- `create_descriptive_text(...)`

**Internal helpers:**
- `_generate_data_export_tag(question_text)`
- `_build_choices_dict(choices)`

---

### 4. `question_management.py` - Question Management
**Purpose:** Managing existing questions  
**Size:** ~100 lines

**Responsibilities:**
- Get question details
- Update questions
- Delete questions
- Get all questions in survey

**Methods:**
- `get_question(survey_id, question_id)`
- `update_question(survey_id, question_id, question_data)`
- `update_question_text(survey_id, question_id, new_text)`
- `delete_question(survey_id, question_id)`
- `get_survey_questions(survey_id)`

---

### 5. `blocks.py` - Block Operations
**Purpose:** Block management  
**Size:** ~80 lines

**Responsibilities:**
- Get blocks
- Create blocks
- Update blocks (future)
- Delete blocks (future)

**Methods:**
- `get_blocks(survey_id)`
- `create_block(survey_id, block_name)`
- `update_block(survey_id, block_id, data)` (future)
- `delete_block(survey_id, block_id)` (future)

---

### 6. `client.py` - Main Client
**Purpose:** Combine all mixins  
**Size:** ~50 lines

**Responsibilities:**
- Import all mixins
- Create combined client class
- Provide single entry point

```python
from .base import APIBase
from .surveys import SurveyMixin
from .questions import QuestionMixin
from .question_management import QuestionManagementMixin
from .blocks import BlockMixin

class QualtricsAPI(
    APIBase,
    SurveyMixin,
    QuestionMixin,
    QuestionManagementMixin,
    BlockMixin
):
    """
    Main Qualtrics API client.
    
    Combines all functionality from mixins:
    - Survey operations
    - Question creation
    - Question management
    - Block operations
    """
    pass
```

---

## Future Modules (v0.2.0+)

### `embedded_data.py` - Embedded Data (v0.2.0)
```python
class EmbeddedDataMixin:
    def add_embedded_data(self, survey_id, fields): pass
    def get_embedded_data(self, survey_id): pass
    def update_embedded_data(self, survey_id, field, value): pass
    def delete_embedded_data(self, survey_id, field): pass
```

### `survey_flow.py` - Survey Flow (v0.2.0)
```python
class SurveyFlowMixin:
    def get_survey_flow(self, survey_id): pass
    def update_survey_flow(self, survey_id, flow): pass
    def add_branch(self, survey_id, condition, actions): pass
    def add_randomizer(self, survey_id, blocks): pass
```

### `distributions.py` - Distributions (v0.4.0)
```python
class DistributionMixin:
    def create_distribution(self, survey_id, ...): pass
    def get_distribution_stats(self, distribution_id): pass
```

### `responses.py` - Response Management (v0.4.0)
```python
class ResponseMixin:
    def get_responses(self, survey_id): pass
    def export_responses(self, survey_id, format): pass
    def delete_response(self, survey_id, response_id): pass
```

---

## Migration Strategy

### Step 1: Create Module Files
Create new files without breaking existing code:
- `base.py`
- `surveys.py`
- `questions.py`
- `question_management.py`
- `blocks.py`

### Step 2: Move Code
Copy (don't cut yet) methods from `client.py` to appropriate modules.

### Step 3: Update Main Client
Update `client.py` to use mixins.

### Step 4: Test Everything
Run all examples and tests to ensure nothing broke.

### Step 5: Update Imports
Users still import the same way:
```python
from qualtrics_sdk import QualtricsAPI  # Still works!
```

### Step 6: Document
Update documentation to reflect new structure.

---

## File Size Guidelines

**Goal:** Keep files under 500 lines

- ✅ **50-150 lines** - Excellent, very focused
- ✅ **150-300 lines** - Good, well-organized
- ⚠️ **300-500 lines** - OK, but consider splitting
- ❌ **500+ lines** - Too large, definitely split

**Current:**
- `client.py`: 600+ lines ❌ → Split into 5 files

**After refactor:**
- `base.py`: ~100 lines ✅
- `surveys.py`: ~150 lines ✅
- `questions.py`: ~400 lines ✅ (largest, but cohesive)
- `question_management.py`: ~100 lines ✅
- `blocks.py`: ~80 lines ✅
- `client.py`: ~50 lines ✅

---

## Import Strategy

### Internal Imports (within package)
```python
# In surveys.py
from .base import APIBase

class SurveyMixin:
    # Can access self.base_url from APIBase
    pass
```

### External Imports (users)
```python
# Users still use simple import
from qualtrics_sdk import QualtricsAPI

# Everything still works the same!
api = QualtricsAPI(token="...", data_center="...")
api.create_survey("My Survey")  # Works!
api.create_multiple_choice_question(...)  # Works!
```

---

## Testing Strategy

### Module-Level Tests
```python
# tests/test_surveys.py
from qualtrics_sdk.core.surveys import SurveyMixin

class TestSurveys:
    def test_create_survey(self): pass
    def test_delete_survey(self): pass

# tests/test_questions.py
from qualtrics_sdk.core.questions import QuestionMixin

class TestQuestions:
    def test_create_mc_question(self): pass
    def test_create_text_question(self): pass
```

### Integration Tests
```python
# tests/test_integration.py
from qualtrics_sdk import QualtricsAPI

class TestIntegration:
    def test_full_survey_creation(self):
        """Test creating survey with questions"""
        api = QualtricsAPI(...)
        survey = api.create_survey("Test")
        api.create_multiple_choice_question(...)
        # Full workflow test
```

---

## Benefits Summary

### Before (Monolithic)
```
❌ One 600-line file
❌ Hard to navigate
❌ Merge conflicts likely
❌ All-or-nothing testing
❌ Unclear organization
```

### After (Modular)
```
✅ 6 focused files (~100-400 lines each)
✅ Easy to find methods (surveys.py = survey methods!)
✅ Less merge conflicts (work on different files)
✅ Test modules independently
✅ Crystal-clear organization
✅ Easy to add new features (just add new mixin!)
```

---

## Example: Adding New Feature

### Before (Monolithic)
```python
# Add to bottom of 600-line client.py
def add_embedded_data(self, ...):
    # 50 more lines
    pass
```
File is now 650 lines, harder to navigate.

### After (Modular)
```python
# Create new file: embedded_data.py (clean separation!)
class EmbeddedDataMixin:
    def add_embedded_data(self, ...):
        pass

# Update client.py (just add one line)
class QualtricsAPI(
    APIBase,
    SurveyMixin,
    QuestionMixin,
    EmbeddedDataMixin,  # <-- Just add this!
    ...
):
    pass
```

---

## Best Practices

1. **One responsibility per module** - surveys.py only does surveys
2. **Keep mixins independent** - Don't reference other mixins directly
3. **Use APIBase for shared logic** - Don't duplicate request code
4. **Clear naming** - `SurveyMixin`, `QuestionMixin` (not `Mixin1`, `Mixin2`)
5. **Group related methods** - All question creation in one place
6. **Document each module** - Clear docstring at top of file

---

## Conclusion

This modular structure:
- ✅ Scales better as package grows
- ✅ Easier to maintain and navigate
- ✅ Clearer separation of concerns
- ✅ Better for collaboration
- ✅ Easier to test
- ✅ Professional industry standard

**Recommended:** Make this change now while package is still young!
