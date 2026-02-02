# Qualtrics SDK - Claude Project Context

This file contains essential information about the Qualtrics SDK project for AI assistants and developers.

---

## 📋 Project Overview

**Name:** Qualtrics SDK  
**Version:** 0.1.0 (Initial Development)  
**Purpose:** Professional Python wrapper for Qualtrics REST API v3  
**License:** MIT  
**Python:** >=3.8  
**Status:** Pre-1.0 (breaking changes acceptable)

---

## 🎯 Project Goals

1. **Primary Goal:** Provide a complete, easy-to-use Python SDK for Qualtrics API
2. **Secondary Goals:**
   - Enable researchers to automate survey creation
   - Support all major Qualtrics features
   - Maintain professional code quality
   - Build a sustainable open-source project

---

## 📦 Package Structure

```
qualtricsapi/
├── qualtrics_sdk/              # Main package
│   ├── __init__.py            # v0.1.0, exports QualtricsAPI
│   ├── core/
│   │   └── client.py          # Main QualtricsAPI class (~600 lines)
│   ├── models/                # Future: Data models
│   └── utils/                 # Future: Utility functions
│
├── examples/                   # Working examples
│   ├── quick_start.py         # Simple 5-min example
│   └── comprehensive_example.py # All features demo
│
├── tests/                      # Test suite (setup, needs expansion)
│
├── docs/                       # Complete documentation
│   ├── DEVELOPMENT.md         # Versioning, releases, workflow
│   ├── ROADMAP.md             # Feature roadmap (v0.1-v1.0)
│   ├── CONTRIBUTING.md        # Contribution guidelines
│   ├── PROJECT_ORGANIZATION.md # Structure guide
│   └── PACKAGE_SUMMARY.md     # Transformation summary
│
├── setup.py                    # Package installation config
├── pyproject.toml             # Modern Python project config
├── requirements.txt           # Dependencies: requests, python-dotenv
├── CHANGELOG.md               # Version 0.1.0 documented
├── LICENSE                    # MIT License
├── README.md                  # Main documentation
├── QUICK_REFERENCE.md         # Quick reference guide
├── .env                       # Credentials (NOT in git)
├── .env.example               # Template (safe to share)
└── .gitignore                 # Protects .env, venv, __pycache__
```

---

## 🔢 Version System (Semantic Versioning)

### Format: MAJOR.MINOR.PATCH (e.g., 1.2.3)

**Current Version:** 0.1.0

### When to Bump Versions

```
PATCH (0.1.0 → 0.1.1)
├─ Bug fixes
├─ Documentation improvements
├─ Minor internal changes
└─ No new features, no breaking changes

MINOR (0.1.5 → 0.2.0)
├─ New features added
├─ New question types
├─ Enhanced functionality
└─ Backward compatible (old code still works)

MAJOR (0.9.0 → 1.0.0 or 1.x.x → 2.0.0)
├─ Breaking changes (API changes)
├─ Removed features
├─ Changed function signatures
└─ First stable release (0.x → 1.0.0)
```

### Pre-1.0 Status
- Currently: **0.1.0** (initial development)
- Breaking changes are acceptable
- API may change between versions
- 1.0.0 = first stable release (API locked)

---

## 🗺️ Feature Roadmap

### ✅ v0.1.0 - COMPLETED (2026-02-01)

**Survey Operations:**
- Create, read, update, delete surveys
- List surveys
- Get survey URL

**Question Types:**
- Multiple choice (radio, dropdown, horizontal)
- Text entry (single-line, essay)
- Matrix/Likert scale
- Slider
- Rank order (drag and drop)
- Net Promoter Score (NPS)
- Descriptive text blocks

**Other:**
- Question management (create, update, delete)
- Block operations
- Secure credential management (.env)
- Complete documentation

### 🎯 v0.2.0 - Planned (Target: 2026-03-01)

**Priority: HIGH - Essential Survey Features**

1. **Embedded Data Support**
   ```python
   api.add_embedded_data(survey_id, {
       "user_id": "${e://Field/user_id}",
       "source": "email_campaign"
   })
   api.get_embedded_data(survey_id)
   api.update_embedded_data(survey_id, field_name, new_value)
   api.delete_embedded_data(survey_id, field_name)
   ```

2. **Survey Flow Support**
   ```python
   api.get_survey_flow(survey_id)
   api.add_branch(survey_id, condition, true_action, false_action)
   api.add_randomizer(survey_id, block_ids, randomize_type)
   api.update_survey_flow(survey_id, flow_definition)
   ```

### 🎯 v0.3.0 - Planned (Target: 2026-04-01)

**Priority: HIGH - Advanced Question Features**

1. **Custom JavaScript for Questions**
   ```python
   api.add_question_javascript(survey_id, question_id, javascript_code)
   api.add_auto_advance(survey_id, question_id, delay_ms)
   api.add_input_validation(survey_id, question_id, regex)
   ```

2. **Loop and Merge Support**
   ```python
   api.create_loop_and_merge(survey_id, name, fields, data)
   api.create_question_with_piping(survey_id, question_with_piping)
   ```

3. **Quota Support**
   ```python
   api.create_quota(survey_id, name, logic, quota, action)
   api.get_quota_status(survey_id, quota_id)
   ```

### 🎯 v0.4.0 - Planned (Target: 2026-05-01)

**Priority: MEDIUM - Distribution & Responses**

1. **Distribution Management**
2. **Response Management**
   ```python
   api.get_responses(survey_id, format="json")
   api.export_responses(survey_id, file_format="csv")
   ```

### 🎯 v0.5.0 - Planned (Target: 2026-06-01)

**Priority: MEDIUM - Additional Question Types**

- Heat map questions
- Constant sum
- Side-by-side questions
- Display logic
- Skip logic

### 🎯 v0.6.0 - Planned (Target: 2026-07-01)

**Priority: LOW - Collaboration Features**

- User & permission management
- Library management (reusable blocks/questions)

### 🎉 v1.0.0 - Planned (Target: 2026-09-01)

**First Stable Release Requirements:**
- All core features implemented (v0.1-v0.6)
- Test coverage >80%
- Full API documentation
- Stable API (no breaking changes after 1.0)
- Production-ready

---

## 🔧 Development Workflow

### Making Changes

1. **Create branch**
   ```bash
   git checkout -b feature/feature-name
   # or: bugfix/bug-name, docs/doc-update
   ```

2. **Make changes**
   - Edit code in `qualtrics_sdk/`
   - Write tests in `tests/`
   - Update docs if needed

3. **Test**
   ```bash
   pytest                    # Run tests
   black qualtrics_sdk/      # Format code
   flake8 qualtrics_sdk/     # Lint code
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: Add embedded data support"
   # Commit types: feat, fix, docs, test, refactor, style, chore
   ```

5. **Push & PR**
   ```bash
   git push origin feature/feature-name
   # Create Pull Request on GitHub
   ```

### Making Releases

**Complete process in docs/DEVELOPMENT.md**

Quick steps:
1. Update version in `qualtrics_sdk/__init__.py` and `pyproject.toml`
2. Update `CHANGELOG.md` (move Unreleased to version section)
3. Commit: `git commit -m "Release v0.2.0"`
4. Tag: `git tag -a v0.2.0 -m "Release version 0.2.0"`
5. Push: `git push origin main --tags`
6. Create GitHub Release
7. (Optional) Publish to PyPI

---

## 📝 Code Standards

### Python Style
- Follow PEP 8
- Use Black for formatting (line length: 100)
- Use Flake8 for linting
- Use type hints everywhere

### Code Organization
```python
# Good structure
def method_name(
    self,
    param1: str,
    param2: int = 5,
    optional: Optional[str] = None
) -> Dict[str, Any]:
    """
    Brief description.
    
    Longer explanation of what this does.
    
    Args:
        param1: Description
        param2: Description (default: 5)
        optional: Description
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When X happens
        Exception: When Y happens
        
    Example:
        >>> api = QualtricsAPI(token="x", data_center="y")
        >>> result = api.method_name("test")
        >>> print(result['key'])
        'value'
    """
    # Implementation
```

### Testing
- Every feature needs tests
- Aim for >80% coverage
- Test happy paths AND error cases
- Use fixtures for common setup
- Mock external API calls

---

## 🔐 Security

### API Credentials
- **NEVER** hardcode API keys in code
- Always use `.env` file
- `.env` is in `.gitignore`
- Use `.env.example` as template

### Current Setup
```bash
# .env (NOT in git)
QUALTRICS_API_TOKEN=your_actual_token
QUALTRICS_DATA_CENTER=upenn.qualtrics.com

# In code
import os
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv('QUALTRICS_API_TOKEN')
```

---

## 🚀 Quick Commands

### Setup
```bash
cd qualtricsapi
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### Run Examples
```bash
python examples/quick_start.py
python examples/comprehensive_example.py
```

### Test
```bash
pytest                          # Run all tests
pytest tests/test_client.py     # Run specific test
pytest --cov=qualtrics_sdk      # With coverage
```

### Format & Lint
```bash
black qualtrics_sdk/            # Format
flake8 qualtrics_sdk/           # Lint
mypy qualtrics_sdk/             # Type check
```

### Build
```bash
python -m build                 # Build distribution
pip install .                   # Install locally
```

---

## 📊 Current Status

**Code Base:**
- Main module: `qualtrics_sdk/core/client.py` (~600 lines)
- Methods: ~30 public methods
- Question types: 9 types supported
- Dependencies: 2 (requests, python-dotenv)

**Documentation:**
- README.md: ✅ Complete
- QUICK_REFERENCE.md: ✅ Complete
- DEVELOPMENT.md: ✅ Complete (versioning, releases)
- ROADMAP.md: ✅ Complete (v0.1 - v1.0 planned)
- CONTRIBUTING.md: ✅ Complete
- PROJECT_ORGANIZATION.md: ✅ Complete
- CHANGELOG.md: ✅ v0.1.0 documented

**Tests:**
- Test structure: ✅ Set up
- Test coverage: ⚠️ Needs expansion (currently minimal)

**CI/CD:**
- GitHub Actions: ❌ Not set up yet
- Pre-commit hooks: ❌ Not set up yet

---

## 🎯 Immediate Next Steps

### For Development
1. **Expand test coverage** (priority: high)
   - Add comprehensive unit tests
   - Mock API responses
   - Test error handling

2. **Set up CI/CD** (priority: medium)
   - GitHub Actions for tests
   - Automatic formatting checks
   - Coverage reports

3. **Start v0.2.0** (priority: high)
   - Implement embedded data support
   - Implement survey flow management
   - Add tests
   - Update docs

### For Project Management
1. **Initialize GitHub repository**
   - Create repo
   - Push code
   - Set up issues and labels

2. **Create issues for roadmap items**
   - One issue per feature
   - Label with version milestone
   - Link to roadmap

3. **Set up project board**
   - Kanban board: Todo, In Progress, Done
   - Track v0.2.0 progress

---

## 🤝 Contribution Notes

### When Someone Contributes
1. They should read `docs/CONTRIBUTING.md`
2. Create feature branch
3. Write code + tests
4. Update docs
5. Submit PR
6. Pass CI checks
7. Get review
8. Merge!

### Good First Issues
Label issues with `good first issue`:
- Documentation improvements
- Adding examples
- Writing tests for existing features
- Minor bug fixes

---

## 🐛 Known Issues / Technical Debt

### Current Limitations
1. **No async support** - All API calls are synchronous
2. **Limited error handling** - Basic exception handling only
3. **No retry logic** - Failed requests don't auto-retry
4. **No caching** - Every call hits the API
5. **No rate limiting** - Doesn't respect API rate limits
6. **Checkbox questions** - MAVR/MAHR selectors don't work yet

### Future Improvements
1. Add async/await support (v2.0?)
2. Better error messages with suggestions
3. Automatic retry with exponential backoff
4. Response caching layer
5. Rate limit handling
6. More question type selectors

---

## 📚 Key Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `README.md` | Package overview | First visit |
| `QUICK_REFERENCE.md` | Quick lookup | Daily use |
| `docs/DEVELOPMENT.md` | Versioning, releases | Before developing |
| `docs/ROADMAP.md` | Feature plans | Planning work |
| `docs/CONTRIBUTING.md` | How to contribute | Before contributing |
| `docs/PROJECT_ORGANIZATION.md` | Structure guide | Understanding layout |
| `CHANGELOG.md` | Version history | Before releases |
| `claude.md` | **This file** | AI context |

---

## 🔍 Important Context for AI Assistants

### When Helping with This Project

1. **Respect the structure** - Don't suggest breaking the package layout
2. **Follow semantic versioning** - Understand when to bump versions
3. **Check the roadmap** - Feature requests might already be planned
4. **Maintain consistency** - Follow existing code style
5. **Update all docs** - Code changes require doc updates
6. **Write tests** - New features need tests
7. **Secure credentials** - Never expose API keys

### Common Tasks

**Adding a feature:**
1. Check if it's in ROADMAP.md
2. Create in appropriate subpackage (`core/`, `models/`, `utils/`)
3. Add tests
4. Update CHANGELOG.md
5. Update README.md if public API changes
6. Add example if complex

**Fixing a bug:**
1. Write test that reproduces bug
2. Fix bug
3. Verify test passes
4. Update CHANGELOG.md
5. Document in commit message

**Making a release:**
1. Follow docs/DEVELOPMENT.md release checklist
2. Update 2 version numbers
3. Update CHANGELOG.md
4. Commit, tag, push
5. Create GitHub release

### Code Quality Requirements
- Black formatted (line length: 100)
- Flake8 compliant
- Type hints on all functions
- Docstrings on all public methods
- Tests for new features
- No hardcoded credentials

---

## 🎓 Learning Resources

**For understanding this project:**
- docs/DEVELOPMENT.md - Complete development guide
- docs/PROJECT_ORGANIZATION.md - Structure explained
- docs/ROADMAP.md - Feature timeline

**For Python packaging:**
- [Python Packaging Guide](https://packaging.python.org/)
- [Semantic Versioning](https://semver.org/)

**For testing:**
- [Pytest Documentation](https://docs.pytest.org/)

---

## ✅ Project Health Checklist

**Structure:** ✅ Professional package layout  
**Documentation:** ✅ Comprehensive (5 guides + README)  
**Versioning:** ✅ Semantic versioning defined  
**Roadmap:** ✅ Features planned through v1.0  
**Security:** ✅ Credentials protected  
**Code Quality:** ⚠️ Style defined, needs CI enforcement  
**Testing:** ⚠️ Structure ready, needs expansion  
**CI/CD:** ❌ Not set up yet  
**Community:** ❌ Not public yet  

---

**Last Updated:** 2026-02-01  
**Version:** 0.1.0  
**Status:** Initial Development (Pre-1.0)

---

This file helps AI assistants understand the project context, structure, goals, and workflows. Keep it updated as the project evolves!

---

## 🔄 Code Organization & Refactoring

### Current Structure (v0.1.0)

**Status:** Monolithic (needs refactoring)

```
qualtrics_sdk/core/client.py    (600+ lines)
└── QualtricsAPI class with all methods
```

**Issue:** One large file is hard to navigate and maintain.

### Recommended Structure (Modular with Mixins)

**See:** `docs/CODE_ORGANIZATION.md` and `docs/REFACTORING_PLAN.md`

```
qualtrics_sdk/core/
├── base.py                    (~100 lines) - Core API, HTTP requests
├── surveys.py                 (~150 lines) - Survey CRUD operations
├── questions.py               (~400 lines) - All question type creation
├── question_management.py     (~100 lines) - Update/delete questions
├── blocks.py                  (~80 lines)  - Block operations
└── client.py                  (~50 lines)  - Combines all mixins
```

**Benefits:**
- ✅ Small, focused files (easier to navigate)
- ✅ Clear separation of concerns
- ✅ Independent testing possible
- ✅ Less merge conflicts
- ✅ Easy to extend (just add new mixin)
- ✅ Zero breaking changes (same imports!)

### How Mixins Work

```python
# base.py
class APIBase:
    def __init__(self, token, data_center):
        self.base_url = ...
        self.headers = ...
    
    def _make_request(self, method, endpoint, data):
        # HTTP request logic
        pass

# surveys.py
class SurveyMixin:
    def create_survey(self, name):
        return self._make_request('POST', '/surveys', {...})
    
    def delete_survey(self, survey_id):
        return self._make_request('DELETE', f'/surveys/{survey_id}')

# questions.py
class QuestionMixin:
    def create_multiple_choice_question(self, ...):
        return self._make_request('POST', f'/surveys/{id}/questions', {...})

# client.py (combines everything!)
class QualtricsAPI(APIBase, SurveyMixin, QuestionMixin, ...):
    pass  # All methods inherited!

# Users still use same simple import:
from qualtrics_sdk import QualtricsAPI
api = QualtricsAPI(token, data_center)
api.create_survey("Test")  # Works!
```

### When to Refactor

**Recommendation:** Do it NOW (v0.1.0)

**Why now?**
- Package is still young
- Only 600 lines (manageable)
- No users depending on internals
- Sets foundation for growth

**Why not later?**
- Will be harder with more code
- More risk of breaking things
- Existing patterns harder to change

### Refactoring Checklist

See `docs/REFACTORING_PLAN.md` for step-by-step guide.

- [ ] Create backup of client.py
- [ ] Create base.py (core API)
- [ ] Create surveys.py (extract survey methods)
- [ ] Create questions.py (extract question methods)
- [ ] Create question_management.py (extract management methods)
- [ ] Create blocks.py (extract block methods)
- [ ] Update client.py (use mixins)
- [ ] Test all examples work
- [ ] Update documentation
- [ ] Commit: "Refactor: Split client into modular structure"

### File Organization Best Practices

**Guidelines:**
- Keep files under 500 lines (300 is better)
- One responsibility per module
- Related methods together
- Clear, descriptive names
- Document each module's purpose

**When to split a file:**
- ✅ 50-300 lines: Good size
- ⚠️ 300-500 lines: Consider splitting
- ❌ 500+ lines: Definitely split

---

## 📚 Additional Documentation

**Code Organization:**
- `docs/CODE_ORGANIZATION.md` - Detailed modular design
- `docs/REFACTORING_PLAN.md` - Step-by-step refactoring guide

**Development:**
- `docs/DEVELOPMENT.md` - Versioning, releases, workflow
- `docs/ROADMAP.md` - Feature roadmap (v0.1 - v1.0)
- `docs/CONTRIBUTING.md` - Contribution guidelines
- `docs/PROJECT_ORGANIZATION.md` - Project structure

---

**Last Updated:** 2026-02-01 (Added refactoring information)

---

## ✅ CODE REFACTORING COMPLETED (2026-02-01)

### Current Structure (Post-Refactoring)

**Status:** ✅ Modular with mixins (professionally organized)

```
qualtrics_sdk/core/
├── base.py                   (32 lines)   - Core API & authentication
├── surveys.py               (150 lines)   - Survey CRUD operations
├── questions.py             (395 lines)   - All question type creation
├── question_management.py   (124 lines)   - Question management
├── blocks.py                (60 lines)    - Block operations
├── client.py                (44 lines)    - Combines all mixins
└── client_backup.py         (629 lines)   - Original backup
```

### Module Responsibilities

**base.py:**
- `__init__(api_token, data_center)` - Initialize client
- Provides `self.base_url`, `self.headers` to all mixins

**surveys.py (SurveyMixin):**
- `create_survey()`, `get_survey()`, `delete_survey()`
- `list_surveys()`, `update_survey_name()`
- `get_survey_url()`

**questions.py (QuestionMixin):**
- `create_multiple_choice_question()`
- `create_text_entry_question()`
- `create_matrix_question()`
- `create_slider_question()`
- `create_rank_order_question()`
- `create_nps_question()`
- `create_descriptive_text()`
- `_generate_data_export_tag()` (helper)

**question_management.py (QuestionManagementMixin):**
- `get_question()`, `update_question()`, `update_question_text()`
- `delete_question()`, `get_survey_questions()`

**blocks.py (BlockMixin):**
- `get_blocks()`, `create_block()`

**client.py (QualtricsAPI):**
```python
class QualtricsAPI(APIBase, SurveyMixin, QuestionMixin, 
                   QuestionManagementMixin, BlockMixin):
    pass  # All methods inherited from mixins!
```

### Benefits Achieved

✅ **Organization:** 6 focused files (50-400 lines each) vs 1 huge file (629 lines)  
✅ **Navigation:** Need surveys? Open surveys.py. Need questions? Open questions.py.  
✅ **Testing:** Can test each module independently  
✅ **Collaboration:** Multiple developers can work on different modules  
✅ **Extension:** Add new features by creating new mixins  
✅ **Zero breaking changes:** All user code works identically

### Future Feature Addition (Example)

When adding embedded data (v0.2.0):

```python
# 1. Create qualtrics_sdk/core/embedded_data.py
class EmbeddedDataMixin:
    def add_embedded_data(self, survey_id, fields): ...
    def get_embedded_data(self, survey_id): ...

# 2. Update client.py (one line!)
class QualtricsAPI(
    APIBase, SurveyMixin, QuestionMixin,
    QuestionManagementMixin, BlockMixin,
    EmbeddedDataMixin  # <-- Add this!
):
    pass
```

Clean and organized!

---

**Last Updated:** 2026-02-01 (Refactoring completed)  
**Version:** 0.1.0 (modular structure)
