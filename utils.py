from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
import json


def memory_from_json(memory_json_str: str) -> ConversationBufferMemory:
    messages_data = json.loads(memory_json_str)

    messages = []
    for msg in messages_data:
        if msg["type"] == "human":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            messages.append(AIMessage(content=msg["content"]))

    memory = ConversationBufferMemory(return_messages=True)
    memory.chat_memory.messages = messages
    return memory
