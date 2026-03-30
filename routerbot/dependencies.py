from memory_manager import MemoryManager
from chat_service import ChatService
import os

DEBUG_MODE = True
MEMORY_DIR = "memory_store"

def get_memory(session_id: str):
    os.makedirs(MEMORY_DIR, exist_ok=True)
    file_path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    return MemoryManager(file_path)

def build_chat_service(memory):
    return ChatService(memory, debug=DEBUG_MODE)
    