# Comms

## 2026-03-08 — NPS Labels + Randomizer

BenBen, both features are done and tested against the live API.

**NPS fix:** The old code used `MC/SAHR` (plain horizontal radio). Now uses `MC/NPS` (native Qualtrics NPS selector) with `ColumnLabels` for endpoint labels. The `ColumnLabels` format is `[{"Display": "left text", "IsLabelDefault": false}, {"Display": "right text", "IsLabelDefault": false}]` — discovered from your QSF file.

**Randomizer:** `add_randomizer()` added to `EmbeddedDataMixin`. Supports both block ID strings and embedded data dicts. Blocks are auto-removed from top-level flow (same pattern as branch logic).

**Skill file** updated with both new methods and experiment workflow notes.

**No questions for you.**

## 2026-02-28 — Branch Logic Implementation

BenBen, here's the summary of what was done:

**Problem:** The SDK had no way to add survey flow branching. Display logic (show/hide individual questions) existed, but survey flow branches (routing respondents to different blocks based on answers) did not.

**Root cause of "broken" branching:** When you create a block via `create_block()`, Qualtrics automatically adds it to the top-level flow. If you then manually tried to put that block inside a branch, it would appear both at the top level (always shown) AND inside the branch — so everyone would see everything regardless of the branch condition.

**Solution:** New `BranchLogicMixin` in `qualtrics_sdk/core/branch_logic.py` with three methods:

1. `add_branch_simple()` — one MC choice -> one block (most common case)
2. `add_branch()` — full power: multiple conditions with AND/OR, multiple blocks
3. `add_branch_embedded()` — branch on embedded data field values

The methods automatically remove referenced blocks from the top-level flow so they only appear inside branches.

**No questions for you at this time.**
