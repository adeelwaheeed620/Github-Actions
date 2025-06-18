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

def call_ai_suggester(api_url, api_key, file_path, content, syntax_tree, threshold):
    payload = {
        "filename": file_path,
        "content": content,
        "syntax_tree": syntax_tree,
        "task": "suggest_fixes",
        "confidence_threshold": threshold
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def post_suggestions(suggestions):
    print("\n--- Suggested Fixes ---\n")
    for suggestion in suggestions:
        print(f"File: {suggestion['file']}")
        print(f"Line {suggestion['line']}:")
        print(f"Suggested change:\n{suggestion['suggestion']}\n")

def main():
    config = load_config()
    changed_files = get_changed_files()
    syntax_tree = load_syntax_tree()
    api_url = config["ai_api_url"]
    api_key = config["ai_api_key"]
    threshold = config.get("confidence_threshold", 0.8)

    all_suggestions = []

    for path in changed_files:
        if not path.endswith(".py"):
            continue
        content = read_file_content(path)
        result = call_ai_suggester(api_url, api_key, path, content, syntax_tree, threshold)
        if result.get("suggestions"):
            all_suggestions.extend(result["suggestions"])

    if all_suggestions:
        post_suggestions(all_suggestions)
    else:
        print("No suggestions found.")

if __name__ == "__main__":
    main()
