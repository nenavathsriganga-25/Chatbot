from flask import Flask, render_template, request
from agent import agent_executor
from memory import load_memory, save_memory
from tools import shared_memory

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Load current memory from storage.json
    memory_state = load_memory()

    if request.method == "POST":
        user_input = request.form["message"]

        # First interaction: save name
        if memory_state["name"] is None:
            memory_state["name"] = user_input
            response = f"Nice to meet you, {user_input}!"
        else:
            # Send to Gemini agent
            response = agent_executor.run(user_input)

            # Append to conversation history
            memory_state["chat_history"].append({
                "user": user_input,
                "ai": response
            })

            # Sync to-do list from shared memory
            memory_state["todo_list"] = shared_memory["todo_list"]

        # Save updated memory to file
        save_memory(memory_state)

        return render_template(
            "index.html",
            name=memory_state["name"],
            chat_history=memory_state["chat_history"]
        )

    # GET request
    return render_template(
        "index.html",
        name=memory_state["name"],
        chat_history=memory_state["chat_history"]
    )

if __name__ == "__main__":
    app.run(debug=True)
