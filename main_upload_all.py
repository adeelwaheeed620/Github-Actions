import os
import subprocess
from pathlib import Path
import json
import yaml

# Set repo info
GITHUB_USERNAME = "adeelwaheeed620"
GITHUB_REPO = "Github-Actions"
GITHUB_TOKEN = "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"
REMOTE_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"

# Root directory
ROOT = Path("github_actions_project")
ROOT.mkdir(exist_ok=True)
os.chdir(ROOT)

# 1. Create folders
os.makedirs(".github/workflows", exist_ok=True)
os.makedirs("scripts", exist_ok=True)

# 2. Create workflow files
workflow_files = {
    ".github/workflows/update_syntax_tree.yml": """
name: Syntax Tree Updater
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Syntax Tree Updater
        run: python scripts/generate_syntax_tree.py
      - name: Commit changes
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add syntax-tree.json
          git commit -m "Update syntax tree" || echo "No changes to commit"
          git push
""",
    ".github/workflows/pr_linter.yml": """
name: PR Linter
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run PR Linter
        run: python scripts/mock_pr_linter.py
""",
    ".github/workflows/pr_suggester.yml": """
name: PR Auto-Suggester
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  suggest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run PR Suggester
        run: python scripts/mock_pr_suggester.py
"""
}

# 3. Create script files
script_files = {
    "scripts/generate_syntax_tree.py": """
import json

def generate_syntax_tree():
    tree = {
        "modules": ["module1", "module2"],
        "functions": ["main", "process_data", "handle_request"],
        "classes": ["DataProcessor", "RequestHandler"]
    }
    with open("syntax-tree.json", "w") as f:
        json.dump(tree, f, indent=2)

if __name__ == "__main__":
    generate_syntax_tree()
""",
    "scripts/mock_pr_linter.py": """
print("Running mock PR linter...")
# Here you'd analyze PR contents and print issues (mocked)
""",
    "scripts/mock_pr_suggester.py": """
print("Running mock PR suggester...")
# Here you'd generate suggestions for PR (mocked)
"""
}

# 4. Create config and README
config = {
    "api_url": "https://example-ai-api.com/lint",
    "confidence_threshold": 0.8
}
with open("config.yml", "w") as f:
    yaml.dump(config, f)

with open("README.md", "w") as f:
    f.write("# GitHub Actions: Syntax Tree and PR Automation\n")

with open("syntax-tree.json", "w") as f:
    json.dump({}, f)

# Write all files
for path, content in {**workflow_files, **script_files}.items():
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# 5. Initialize git & push
subprocess.run(["git", "init"])
subprocess.run(["git", "remote", "add", "origin", REMOTE_URL])
subprocess.run(["git", "checkout", "-b", "main"])
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Initial commit with all automation files"])
subprocess.run(["git", "push", "-u", "origin", "main"])
