import json
from pathlib import Path

STORE_PATH = Path("storage.json")

def load_memory():
    if STORE_PATH.exists():
        with open(STORE_PATH, "r") as f:
            data = json.load(f)
            return data
    else:
        return {"name": None, "chat_history": [], "todo_list": []}

def save_memory(memory):
    with open(STORE_PATH, "w") as f:
        json.dump(memory, f, indent=4)
