# Gemini Chatbot
**Gemini Chatbot** is a simple and customizable web-based chatbot built using **Python Flask** and **HTML/CSS**.It provides a clean user interface for chatting with a agent, storing message history, and resetting the conversation.
---

## ✨ Features

The chatbot can:

-**Remember user's name** and previous messages
- **Store and manage a personal to-do list**
- Use **tool calls**:
    - `add_todo`
    - `list_todos`
    - `remove_todo`
- Run on a **Flask web UI**

---

## 🧠Memory Storage

Memory is stored and retrieved using a JSON file called **`storage.json`**.

### **Memory includes:**

- `name` → User's name (stored after first message)
- `chat_history` → Full conversation history
- `todo_list` → Contains the to-do list

Memory is **loaded on startup** and **updated after every tool or chat interaction**.

---

## 🔧Tool Calls
Tools are defined in `tools.py` using LangChain's **@tool** decorator:

| Tool                     | Purpose                        |
| ------------------------ | ------------------------------ |
| `add_todo(item: str)`    | Adds an item to the to-do list |
| `list_todos(dummy: str)` | Lists all current to-dos       |
| `remove_todo(item: str)` | Removes a to-do item by name   |

###Registration with Agent:

In `agent.py`, the tools are registered with LangChain’s Agent system:

agent_executor = initialize_agent(
    [add_todo, list_todos, remove_todo],
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=chat_memory,
    verbose=True
)

# ⚙️ Setup Instructions

### 1️⃣ Clone the Repository


git clone https://github.com/your-username/Chatbot.git
cd Chatbot

### 2️⃣ Set Up Virtual Environment

python -m venv virtual
.\virtual\Scripts\activate    # For Windows
# or
source virtual/bin/activate   # For Mac/Linux

### 3️⃣ Install Requirements

pip install -r requirements.txt

### 4️⃣ Add Your .env File

Create a .env file in the project root:
GOOGLE_API_KEY=your-real-api-key-here

### 5️⃣ Run the App

python app.py

### 🌐 Access the Web Interface

Open your browser and go to:

http://127.0.0.1:5000


💬 Example Prompts
| Prompt                  | What happens?           |
| ----------------------- | ----------------------- |
| "Hello"                    | Bot asks your name      |
| "My name is Ganga"        | Bot remembers your name |
| "Add buy chocolates"    | Adds to-do              |
| "Show my to-do list"    | Lists current to-dos    |
| "Remove buy chocolates" | Removes that to-do      |

⚠️ Limitations:
Only works with Gemini API key access
Currently works only with a single user (no login system)
Simple text interface (Flask form)
🚀 Future Improvements:
Add checkbox UI for to-do list
Add user authentication for multi-user support
Deploy live on Render / Replit
Switch to LangGraph for more flexible workflows

📁 Project Structure
chatbot/
├── app.py             # Flask app
├── agent.py           # LLM agent setup
├── tools.py           # Tool functions (add_todo, list_todo, remove_todo)
├── memory.py          # Load/save memory to storage.json
├── templates/
│   └── index.html     # Web UI
├── .env               # API keys (not uploaded)
├── .gitignore         # Ignore virtual env and .env
├── storage.json       # Chat + to-do list memory
└── requirements.txt   # Python dependencies
