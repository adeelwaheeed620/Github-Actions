import os
import sys
import yaml
import requests
import subprocess
import json

CONFIG_PATH = "config.yml"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def get_changed_files():
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        stdout=subprocess.PIPE, text=True
    )
    return result.stdout.strip().splitlines()

def read_file_content(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_syntax_tree():
    with open("syntax-tree.json", "r") as f:
        return json.load(f)

def call_ai_linter(api_url, api_key, file_path, content, syntax_tree):
    payload = {
        "filename": file_path,
        "content": content,
        "syntax_tree": syntax_tree,
        "task": "lint"
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def post_comment_to_pr(summary):
    print("\n--- Linter Summary ---\n")
    print(summary)

def main():
    config = load_config()
    changed_files = get_changed_files()
    syntax_tree = load_syntax_tree()
    api_url = config["ai_api_url"]
    api_key = config["ai_api_key"]

    summary = ""

    for path in changed_files:
        if not path.endswith(".py"):  # Lint only Python files
            continue
        content = read_file_content(path)
        result = call_ai_linter(api_url, api_key, path, content, syntax_tree)
        if result.get("issues"):
            summary += f"\n**{path}**:\n"
            for issue in result["issues"]:
                summary += f"- {issue}\n"

    if summary:
        post_comment_to_pr(summary)
    else:
        print("No linting issues found.")

if __name__ == "__main__":
    main()
