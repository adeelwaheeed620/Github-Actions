# Syntax Tree Generator
import json

# Placeholder logic
syntax_tree = {
    "type": "Module",
    "body": [
        {"type": "FunctionDef", "name": "main", "body": []}
    ]
}

with open("syntax-tree.json", "w") as f:
    json.dump(syntax_tree, f, indent=2)

print("Syntax tree generated.")