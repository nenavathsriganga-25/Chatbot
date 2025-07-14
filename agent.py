import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from tools import add_todo, list_todos, remove_todo, shared_memory
from memory import load_memory  #, save_memory
from langchain.tools import Tool
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

list_todos_tool = Tool(
    name="list_todos",
    func=list_todos,
    description="List all current to-do items.",
    return_direct=True
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    google_api_key=GOOGLE_API_KEY,
    system_message= '''
You are a friendly assistant that manages a to-do list for the user. 
Whenever the user asks to see their to-do list, always respond by listing each item on its own line, numbered, and never summarize the list in a single sentence. 
Do not use commas or 'and' to join items. 
Always use this format:

Here's your current to-do list:
1. First item
2. Second item
3. Third item

Never use any other format for listing to-dos.

'''
)

# # Load from file into shared memory
# stored = load_memory()
# shared_memory["name"] = stored.get("name")
# shared_memory["chat_history"] = stored.get("chat_history", [])
# shared_memory["todo_list"] = stored.get("todo_list", [])

# chat_memory = ConversationBufferMemory(
#     memory_key="chat_history",
#     return_messages=True
# )

# for msg in shared_memory["chat_history"]:
#     chat_memory.chat_memory.add_user_message(msg["user"])
#     chat_memory.chat_memory.add_ai_message(msg["ai"])

# # Initialize agent
# agent_executor = initialize_agent(
#     [add_todo, list_todos, remove_todo],
#     llm,
#     agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
#     memory=chat_memory,
#     verbose=False
# )

def create_agent():
    # Always load the latest chat history
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

    return initialize_agent(
        [add_todo, list_todos, remove_todo,list_todos_tool],
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=chat_memory,
        verbose=False
    )

# # Use this function to get a fresh agent
# agent_executor = create_agent()