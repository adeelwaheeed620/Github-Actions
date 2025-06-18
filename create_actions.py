import os
import requests
import base64

# Set your repo details
username = "adeelwaheeed620"
repo = "Github-Actions"
branch = "main"
token = os.getenv("GH_TOKEN")

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

def create_or_update_file(path, content, message):
    print(f"Uploading: {path}")
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    
    # Check if file exists to get SHA
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sha = r.json()["sha"]
    else:
        sha = None

    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
        "branch": branch
    }
    if sha:
        data["sha"] = sha

    response = requests.put(url, headers=headers, json=data)
    print(f"{path} => {response.status_code}")
    if response.status_code not in [200, 201]:
        print(response.json())

# Files to create (mocked content)
files = {
    ".github/workflows/update_syntax_tree.yml": '''
name: Syntax Tree Updater
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update-tree:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Generate Syntax Tree
        run: python scripts/generate_syntax_tree.py
      - name: Check for Changes
        id: check_changes
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "actions@github.com"
          git add syntax-tree.json
          if git diff --cached --quiet; then
            echo "changed=false" >> $GITHUB_OUTPUT
          else
            echo "changed=true" >> $GITHUB_OUTPUT
      - name: Commit and Push
        if: steps.check_changes.outputs.changed == 'true'
        run: |
          git commit -m "Auto-update syntax tree"
          git push
''',

    ".github/workflows/pr_linter.yml": '''
name: PR Linter
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Run Linter
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/mock_pr_linter.py
''',

    ".github/workflows/pr_suggester.yml": '''
name: PR Auto Suggester
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  suggest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Run Suggestion Engine
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python scripts/mock_pr_suggester.py
'''
}

for path, content in files.items():
    create_or_update_file(path.strip(), content.strip(), f"Add workflow: {os.path.basename(path)}")
