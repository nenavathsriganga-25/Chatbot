
from flask import Flask, render_template, request, redirect, url_for
from agent import create_agent  #agent_executor
from memory import load_memory, save_memory
from tools import shared_memory

app = Flask(__name__)

agent_executor = create_agent()

#@app.before_first_request
def sync_shared_memory():
    memory_state = load_memory()
    shared_memory["todo_list"] = memory_state.get("todo_list", [])
    shared_memory["chat_history"] = memory_state.get("chat_history", [])
    shared_memory["name"] = memory_state.get("name")

@app.route("/", methods=["GET", "POST"])
def index():
    
    sync_shared_memory()
    memory_state = load_memory()

    if request.method == "POST":
        user_input = request.form["message"].strip()

        if not user_input:
            return redirect(url_for("index"))

        # First interaction: save name
        if memory_state["name"] is None:
            memory_state["name"] = user_input
            shared_memory["name"] = user_input
            response = f"Nice to meet you, {user_input}! \n   What can I help you with today?"
            memory_state["chat_history"].append({
                "user": user_input,
                "ai": response
            })
        else:
            response = agent_executor.run(user_input)
            # Append to conversation history
            memory_state["chat_history"].append({
                "user": user_input,
                "ai": response
            })
            # Sync to-do list from shared memory
            memory_state["todo_list"] = shared_memory["todo_list"]

        save_memory(memory_state)

        return render_template(
            "index.html",
            name=memory_state["name"],
            chat_history=memory_state["chat_history"],
            todo_list=None if len(memory_state["todo_list"])==0  else memory_state["todo_list"]
        )

    # GET request
    return render_template(
        "index.html",
        name=memory_state["name"],
        chat_history=memory_state["chat_history"],
        todo_list=None if len(memory_state["todo_list"])==0  else memory_state["todo_list"]
    )

@app.route("/clear", methods=["POST"])
def clear():
    global agent_executor
    sync_shared_memory()
    memory_state = load_memory()
    memory_state["chat_history"] = []
    memory_state["todo_list"] = []
    memory_state["name"] = None 
    save_memory(memory_state)
    shared_memory["chat_history"] = []
    shared_memory["todo_list"] = []
    shared_memory["name"] = None 
    
    agent_executor = create_agent()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
