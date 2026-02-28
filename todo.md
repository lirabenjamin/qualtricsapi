# Todo

## 2026-02-28

- [x] Create `dev` branch
- [x] Investigate why branching logic was broken (SDK had no branch support; blocks appeared at top-level flow AND inside branches)
- [x] Implement `BranchLogicMixin` with `add_branch()`, `add_branch_simple()`, `add_branch_embedded()`
- [x] Auto-remove blocks from top-level flow when nesting inside branches
- [x] Wire `BranchLogicMixin` into `QualtricsAPI` client
- [x] End-to-end test: MC choice branching, embedded data branching, multi-condition AND branch
- [x] Clean up test surveys
