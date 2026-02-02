# Creating GitHub Issues Programmatically

This directory contains scripts to automatically create GitHub issues from the templates in `.github/ISSUE_TEMPLATE/`.

## Prerequisites

### 1. Install GitHub CLI

**macOS:**
```bash
brew install gh
```

**Ubuntu/Debian:**
```bash
sudo apt install gh
```

**Windows:**
```bash
winget install --id GitHub.cli
```

Or download from: https://cli.github.com/

### 2. Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate with your GitHub account.

### 3. Initialize Git Repository (if not already done)

If this isn't already a GitHub repository:

```bash
# Initialize git
git init

# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/qualtrics-sdk.git

# Or if you've already created the repo on GitHub
gh repo create qualtrics-sdk --public --source=. --remote=origin
```

### 4. Create Milestones (Optional but Recommended)

The issues reference milestones `v0.2.0` and `v0.4.0`. You can create these:

**Via GitHub Web:**
1. Go to your repository on GitHub
2. Click "Issues" → "Milestones" → "New milestone"
3. Create milestones: `v0.2.0` and `v0.4.0`

**Via GitHub CLI:**
```bash
gh api repos/:owner/:repo/milestones -f title="v0.2.0" -f description="Survey Flow & Logic Features"
gh api repos/:owner/:repo/milestones -f title="v0.4.0" -f description="Response Management Features"
```

## Running the Scripts

You have two options:

### Option 1: Bash Script (macOS/Linux)

```bash
./create_github_issues.sh
```

### Option 2: Python Script (Cross-platform)

```bash
python3 create_github_issues.py
```

Or make it executable and run directly:
```bash
chmod +x create_github_issues.py
./create_github_issues.py
```

## What Gets Created

The script creates 4 GitHub issues:

1. **[FEATURE] Add Embedded Data Support**
   - Labels: `enhancement`, `v0.2.0`
   - Milestone: `v0.2.0`

2. **[FEATURE] Add Randomization Support**
   - Labels: `enhancement`, `v0.2.0`
   - Milestone: `v0.2.0`

3. **[FEATURE] Add Conditional Display / Display Logic Support**
   - Labels: `enhancement`, `v0.2.0`
   - Milestone: `v0.2.0`

4. **[FEATURE] Add Response Management and Export Support**
   - Labels: `enhancement`, `v0.4.0`
   - Milestone: `v0.4.0`

## Verifying Issues Were Created

```bash
# List all issues
gh issue list

# View a specific issue
gh issue view 1

# View issue in browser
gh issue view 1 --web
```

## Troubleshooting

### Error: "not authenticated"
```bash
gh auth login
```

### Error: "not in a git repository"
```bash
git init
git remote add origin https://github.com/yourusername/qualtrics-sdk.git
```

### Error: "milestone not found"
If milestones don't exist, the script will still create the issues without milestones. You can add them later:

```bash
# Add milestone to an issue
gh issue edit 1 --milestone "v0.2.0"
```

### Error: "permission denied"
Make the scripts executable:
```bash
chmod +x create_github_issues.sh
chmod +x create_github_issues.py
```

## Manual Creation

If you prefer to create issues manually, use the templates in `.github/ISSUE_TEMPLATE/`:

```bash
# Create issue interactively (prompts you to select template)
gh issue create

# Create issue from specific template
gh issue create --template embedded-data.md
```

## After Creating Issues

Once issues are created, you can:

1. **Organize with Projects:**
   ```bash
   gh project item-add <project-id> --owner <owner> --url <issue-url>
   ```

2. **Assign to Team Members:**
   ```bash
   gh issue edit 1 --add-assignee @username
   ```

3. **Add to Milestone:**
   ```bash
   gh issue edit 1 --milestone "v0.2.0"
   ```

4. **Add Labels:**
   ```bash
   gh issue edit 1 --add-label "good first issue"
   ```

## GitHub CLI Cheat Sheet

```bash
# List issues
gh issue list
gh issue list --state open
gh issue list --label "enhancement"
gh issue list --milestone "v0.2.0"

# View issue
gh issue view 1
gh issue view 1 --web

# Edit issue
gh issue edit 1 --title "New title"
gh issue edit 1 --body "New description"
gh issue edit 1 --add-label "bug"
gh issue edit 1 --add-assignee @me

# Close issue
gh issue close 1

# Comment on issue
gh issue comment 1 --body "Great idea!"

# Search issues
gh issue list --search "embedded data"
```

## Notes

- Issues are created in the current repository (based on git remote)
- The scripts check prerequisites before creating issues
- If milestones don't exist, issues are created without milestones (can be added later)
- All issue bodies include links to the full specification templates
- Issues are automatically labeled with `enhancement` and version tags

## See Also

- [.github/ISSUE_TEMPLATE/README.md](.github/ISSUE_TEMPLATE/README.md) - Issue templates guide
- [GITHUB_ISSUES_SUMMARY.md](GITHUB_ISSUES_SUMMARY.md) - Summary of all issue templates
- [GitHub CLI Documentation](https://cli.github.com/manual/)
