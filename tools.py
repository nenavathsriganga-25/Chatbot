from langchain.tools import tool

# Shared memory dict
shared_memory = {
    "name": None,
    "chat_history": [],
    "todo_list": []
}

@tool
def add_todo(item: str) -> str:
    """Add a to-do item to the user's list."""
    shared_memory["todo_list"].append(item)
    return f"I have added '{item}' to your to-do list."

@tool
def list_todos(dummy: str = "list") -> str:
    """List all current to-do items."""
    todos = shared_memory["todo_list"]
    if not todos:
        return "Your to-do list is empty."
    return "\n".join(f"{i+1}. {todo}" for i, todo in enumerate(todos))

@tool
def remove_todo(item: str) -> str:
    """Remove a to-do item by exact name."""
    if item in shared_memory["todo_list"]:
        shared_memory["todo_list"].remove(item)
        return f"Removed '{item}' from your to-do list."
    else:
        return f"'{item}' not found in your to-do list."
