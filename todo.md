# Todo

## 2026-03-08

- [x] Fix `create_nps_question` to use native NPS selector (MC/NPS) instead of SAHR
- [x] Add `left_label` and `right_label` params to NPS via `ColumnLabels` API field
- [x] Add `data_export_tag` param to NPS
- [x] Add `add_randomizer()` method for BlockRandomizer in survey flow
- [x] Test randomizer with embedded data dicts (2x2 experiment pattern)
- [x] Test randomizer with block ID strings
- [x] Update skill file (`~/.claude/skills/qualtrics-survey/skill.md`) with new methods

## 2026-02-28

- [x] Create `dev` branch
- [x] Investigate why branching logic was broken (SDK had no branch support; blocks appeared at top-level flow AND inside branches)
- [x] Implement `BranchLogicMixin` with `add_branch()`, `add_branch_simple()`, `add_branch_embedded()`
- [x] Auto-remove blocks from top-level flow when nesting inside branches
- [x] Wire `BranchLogicMixin` into `QualtricsAPI` client
- [x] End-to-end test: MC choice branching, embedded data branching, multi-condition AND branch
- [x] Clean up test surveys
- [x] Change default survey design from "flat" to "classic" (`Skin.templateId: "*classic"`)
- [x] Add default embedded data: PROLIFIC_PID (from URL), date_created, created_by_script
- [x] Add `get_survey_options()`, `update_survey_options()`, `set_survey_template()` methods
