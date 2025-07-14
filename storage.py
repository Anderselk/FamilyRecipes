# core/storage.py

import json
from core.recipe import Recipe

def load_recipes(file_path):
    """Load recipes from a JSON file. Return a list of Recipe objects."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Recipe.from_dict(item) for item in data]
    except FileNotFoundError:
        return []  # No data file yet
    except json.JSONDecodeError:
        print("Warning: Couldn't parse the recipe file. Starting with an empty list.")
        return []

def save_recipes(recipes, file_path):
    """Save a list of Recipe objects to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([r.to_dict() for r in recipes], f, indent=2, ensure_ascii=False)


import os
TAG_FILE = "recipes/tags.json"

def load_tags():
    if not os.path.exists(TAG_FILE):
        return []
    try:
        with open(TAG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Could not load tags. Starting empty.")
        return []

def save_tags(tags):
    with open(TAG_FILE, 'w', encoding='utf-8') as f:
        json.dump(tags, f, indent=2, ensure_ascii=False)

