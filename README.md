# GitHub Actions – AI-Powered Code Quality Automation

This project provides a complete GitHub Actions automation suite that:

1. 🔁 Keeps your syntax tree in sync
2. 🔍 Analyzes every Pull Request for issues
3. 💡 Suggests AI-powered inline code fixes

---

## 🔧 Features

### 1. **Syntax Tree Updater**
- **Trigger:** Runs on a schedule (daily at midnight) or manually.
- **Purpose:** Regenerates `syntax-tree.json` using the current codebase.
- **Workflow:** `.github/workflows/update_syntax_tree.yml`

### 2. **AI-Powered PR Linter**
- **Trigger:** Pull request events (`opened` and `synchronize`)
- **Purpose:** Sends the changed files and syntax tree to an external AI API for issue detection.
- **Issues Detected:** Broken references, type mismatches, missing imports, etc.
- **Workflow:** `.github/workflows/pr_linter.yml`
- **Script:** `scripts/pr_linter.py`

### 3. **AI-Powered PR Auto-Suggester**
- **Trigger:** Pull request events (`opened` and `synchronize`)
- **Purpose:** Requests inline fix suggestions from the AI API and posts them as review comments.
- **Workflow:** `.github/workflows/pr_suggester.yml`
- **Script:** `scripts/pr_suggester.py`

- *## ⚙️ Configuration

All configurable values are stored in `config.yml`:

```yaml
api_url: "https://your-ai-api.example.com/lint"
api_key: "your-secret-api-key"
confidence_threshold: 0.85
You can modify this file without changing the code.

**Setup
Install dependencies locally:

bash
Copy
Edit
pip install -r requirements.txt
Make sure the config.yml file contains your AI API credentials and parameters.

Push the repository to GitHub – all actions will trigger automatically on schedule or PR events.

