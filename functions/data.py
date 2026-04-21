import json
import os

FILE = "data.json"


def ensure_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def read_data():
    ensure_file()

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_data(new_data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2)