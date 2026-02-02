# Code Refactoring Plan: Monolithic → Modular

## Overview

**Goal:** Split the 600+ line `client.py` into focused, maintainable modules  
**Method:** Mixin pattern (industry standard for this use case)  
**Impact:** Zero breaking changes - all imports work the same  
**Benefit:** Much easier to navigate, test, and extend

---

## Current Structure (❌ Monolithic)

```
qualtrics_sdk/core/client.py             (600+ lines)
└── class QualtricsAPI:
    ├── __init__()                        # Setup
    ├── create_survey()                   # Survey ops
    ├── get_survey()                      # (15 methods)
    ├── delete_survey()                   # 
    ├── list_surveys()                    #
    ├── update_survey_name()              #
    ├── create_multiple_choice_question() # Question creation
    ├── create_text_entry_question()      # (9 types)
    ├── create_matrix_question()          # (lots of code)
    ├── create_slider_question()          #
    ├── create_rank_order_question()      #
    ├── create_nps_question()             #
    ├── create_descriptive_text()         #
    ├── update_question()                 # Question management
    ├── update_question_text()            # (5 methods)
    ├── delete_question()                 #
    ├── get_question()                    #
    ├── get_survey_questions()            #
    ├── get_blocks()                      # Block ops
    ├── create_block()                    # (2 methods)
    └── get_survey_url()                  # Helpers
```

**Problems:**
- 600+ lines in one file (hard to navigate)
- All concerns mixed together
- Hard to find specific methods
- Difficult to test individual features
- Merge conflicts likely in team settings

---

## Proposed Structure (✅ Modular)

```
qualtrics_sdk/core/
├── base.py                    (~100 lines)
│   └── class APIBase
│       ├── __init__()        # Auth setup
│       └── _make_request()   # HTTP requests
│
├── surveys.py                 (~150 lines)
│   └── class SurveyMixin
│       ├── create_survey()
│       ├── get_survey()
│       ├── delete_survey()
│       ├── list_surveys()
│       ├── update_survey_name()
│       └── get_survey_url()
│
├── questions.py               (~400 lines)
│   └── class QuestionMixin
│       ├── create_multiple_choice_question()
│       ├── create_text_entry_question()
│       ├── create_matrix_question()
│       ├── create_slider_question()
│       ├── create_rank_order_question()
│       ├── create_nps_question()
│       ├── create_descriptive_text()
│       └── _generate_data_export_tag()  # Helper
│
├── question_management.py     (~100 lines)
│   └── class QuestionManagementMixin
│       ├── get_question()
│       ├── update_question()
│       ├── update_question_text()
│       ├── delete_question()
│       └── get_survey_questions()
│
├── blocks.py                  (~80 lines)
│   └── class BlockMixin
│       ├── get_blocks()
│       └── create_block()
│
└── client.py                  (~50 lines)
    └── class QualtricsAPI(APIBase, SurveyMixin, 
                            QuestionMixin, QuestionManagementMixin,
                            BlockMixin)
        """Combines all mixins into one client"""
        pass  # All methods inherited from mixins!
```

**Benefits:**
- ✅ Small, focused files (100-400 lines each)
- ✅ Crystal clear organization (surveys.py = survey methods!)
- ✅ Easy to find methods
- ✅ Test modules independently
- ✅ Less merge conflicts
- ✅ Easy to extend (just add new mixin!)

---

## Step-by-Step Refactoring Process

### Step 1: Create Backup ✅
```bash
cp qualtrics_sdk/core/client.py qualtrics_sdk/core/client_backup.py
```

### Step 2: Create `base.py` ✅

**File:** `qualtrics_sdk/core/base.py`

```python
"""Base API client - core functionality"""

import requests
from typing import Dict, Any, Optional


class APIBase:
    """Base class for API communication"""

    def __init__(self, api_token: str, data_center: str):
        """Initialize API client"""
        self.api_token = api_token
        self.data_center = data_center
        self.base_url = f'https://{data_center}/API/v3'
        self.headers = {
            'X-API-TOKEN': api_token,
            'Content-Type': 'application/json'
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """Make HTTP request to API"""
        url = f'{self.base_url}{endpoint}'
        
        if method == 'GET':
            return requests.get(url, headers=self.headers)
        elif method == 'POST':
            return requests.post(url, headers=self.headers, json=data)
        elif method == 'PUT':
            return requests.put(url, headers=self.headers, json=data)
        elif method == 'DELETE':
            return requests.delete(url, headers=self.headers)
```

### Step 3: Create `surveys.py`

**File:** `qualtrics_sdk/core/surveys.py`

```python
"""Survey operations mixin"""

from typing import Dict, List, Any


class SurveyMixin:
    """Mixin providing survey CRUD operations"""

    def create_survey(
        self, survey_name: str, language: str = "EN",
        project_category: str = "CORE"
    ) -> Dict[str, Any]:
        """Create a new survey"""
        survey_data = {
            "SurveyName": survey_name,
            "Language": language,
            "ProjectCategory": project_category
        }

        response = self._make_request('POST', '/survey-definitions', survey_data)

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to create survey: {response.text}")

    def get_survey(self, survey_id: str) -> Dict[str, Any]:
        """Get survey details"""
        response = self._make_request('GET', f'/survey-definitions/{survey_id}')

        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"Failed to get survey: {response.text}")

    def delete_survey(self, survey_id: str) -> bool:
        """Delete a survey"""
        response = self._make_request('DELETE', f'/survey-definitions/{survey_id}')

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to delete survey: {response.text}")

    def list_surveys(self) -> List[Dict[str, Any]]:
        """List all surveys"""
        response = self._make_request('GET', '/surveys')

        if response.status_code == 200:
            return response.json()['result']['elements']
        else:
            raise Exception(f"Failed to list surveys: {response.text}")

    def update_survey_name(self, survey_id: str, new_name: str) -> bool:
        """Update survey name"""
        update_data = {"SurveyName": new_name}
        
        response = self._make_request(
            'PUT', f'/survey-definitions/{survey_id}', update_data
        )

        if response.status_code == 200:
            return True
        else:
            raise Exception(f"Failed to update survey name: {response.text}")

    def get_survey_url(self, survey_id: str) -> str:
        """Get the public URL for a survey"""
        return f"https://{self.data_center}/jfe/form/{survey_id}"
```

### Step 4: Create `questions.py`

**Extract all `create_*_question` methods** → Move to `questions.py`

### Step 5: Create `question_management.py`

**Extract question update/delete methods** → Move to `question_management.py`

### Step 6: Create `blocks.py`

**Extract block methods** → Move to `blocks.py`

### Step 7: Update `client.py`

**File:** `qualtrics_sdk/core/client.py`

```python
"""
Main Qualtrics API Client
Combines all functionality through mixins
"""

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
    - APIBase: Core API communication
    - SurveyMixin: Survey CRUD operations  
    - QuestionMixin: Question creation (all types)
    - QuestionManagementMixin: Question updates/deletes
    - BlockMixin: Block operations
    
    Usage:
        >>> api = QualtricsAPI(token="xxx", data_center="yyy")
        >>> survey = api.create_survey("My Survey")
        >>> api.create_multiple_choice_question(...)
    """
    pass  # All methods inherited from mixins!
```

### Step 8: Test Everything

```bash
# Run examples to verify
python examples/quick_start.py
python examples/comprehensive_example.py

# Run tests
pytest tests/
```

### Step 9: Update Documentation

Update `docs/CODE_ORGANIZATION.md` and `claude.md` with new structure.

---

## Backward Compatibility

**✅ Users' code doesn't need to change!**

```python
# This still works exactly the same:
from qualtrics_sdk import QualtricsAPI

api = QualtricsAPI(token="xxx", data_center="yyy")
api.create_survey("Test")                    # Still works!
api.create_multiple_choice_question(...)      # Still works!
api.get_blocks(survey_id)                     # Still works!
```

The only thing that changed is **internal organization** - the public API stays identical.

---

## Testing Strategy

### Before Refactoring
```bash
# Run all examples to establish baseline
python examples/quick_start.py          # Should work
python examples/comprehensive_example.py # Should work
```

### After Each Module Creation
```bash
# Test incrementally
python -c "from qualtrics_sdk import QualtricsAPI; print('Import works!')"
python examples/quick_start.py
```

### After Complete Refactoring
```bash
# Full test suite
python examples/quick_start.py
python examples/comprehensive_example.py
pytest tests/  # When tests exist
```

---

## Future Expansion Example

When adding embedded data (v0.2.0):

### Before (Monolithic)
```python
# Add to 600+ line client.py at the bottom
def add_embedded_data(self, survey_id, fields):
    # 50 more lines
    pass
```
Now client.py is 650+ lines!

### After (Modular)
```python
# Create new file: embedded_data.py
class EmbeddedDataMixin:
    def add_embedded_data(self, survey_id, fields):
        # Implementation
        pass

# Update client.py - just add one line!
class QualtricsAPI(
    APIBase,
    SurveyMixin,
    QuestionMixin,
    QuestionManagementMixin,
    BlockMixin,
    EmbeddedDataMixin,  # <-- Add this!
):
    pass
```

Clean and organized!

---

## Files to Create

1. ✅ `qualtrics_sdk/core/base.py` - Done (example above)
2. ⏳ `qualtrics_sdk/core/surveys.py` - Done (example above)
3. ⏳ `qualtrics_sdk/core/questions.py` - Need to extract
4. ⏳ `qualtrics_sdk/core/question_management.py` - Need to extract
5. ⏳ `qualtrics_sdk/core/blocks.py` - Need to extract
6. ⏳ Update `qualtrics_sdk/core/client.py` - Need to update

---

## Recommendation

**✅ Do this refactoring NOW** while the package is still young (v0.1.0).

**Why now?**
- Package is still small (one file)
- No users depending on internal structure yet
- Sets good foundation for growth
- Much harder to do later when package is bigger

**Benefits immediately:**
- Easier to navigate code
- Easier to review changes
- Professional structure
- Ready for team collaboration

---

## Next Steps

1. **Review this plan** - Understand the approach
2. **Create backup** - Safety first!
3. **Create new modules** - One at a time
4. **Test incrementally** - After each module
5. **Update client.py** - Combine mixins
6. **Final testing** - Run all examples
7. **Update docs** - Document new structure
8. **Commit** - "Refactor: Split client into modular structure"

---

**Need help with implementation?** Just ask! I can:
- Create each module file
- Extract methods from client.py
- Test everything works
- Update documentation
