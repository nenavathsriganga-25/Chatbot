import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from tools import add_todo, list_todos, remove_todo, shared_memory
from memory import load_memory, save_memory

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY
)

# Load from file into shared memory
stored = load_memory()
shared_memory["name"] = stored.get("name")
shared_memory["chat_history"] = stored.get("chat_history", [])
shared_memory["todo_list"] = stored.get("todo_list", [])

chat_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

for msg in shared_memory["chat_history"]:
    chat_memory.chat_memory.add_user_message(msg["user"])
    chat_memory.chat_memory.add_ai_message(msg["ai"])

# Initialize agent
agent_executor = initialize_agent(
    [add_todo, list_todos, remove_todo],
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=chat_memory,
    verbose=True
)
