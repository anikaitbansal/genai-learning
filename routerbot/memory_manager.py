import json
import os


class MemoryManager:
    def __init__(self, file_path="chat_history.json"):
        self.file_path = file_path

    def load(self): # This function loads the chat history from the specified JSON file. It checks if the file exists, and if it does, it reads the contents and parses it as JSON to populate the chat_history list. If the file does not exist, it initializes an empty chat history. This allows us to persist the conversation history across different sessions of the chatbot, enabling it to maintain context even after being restarted.
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    return json.load(file)
            except Exception:
                print("[DEBUG] Failed to load memory. Using default.")
        
        return [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    def save(self, chat_history): # This function saves the current chat history to the specified JSON file. It opens the file in write mode and writes the chat_history list as JSON data. This allows us to persist the conversation history so that it can be loaded again in future sessions, maintaining continuity in the interactions with the chatbot.
        with open(self.file_path, "w") as file:
            json.dump(chat_history, file, indent=4)

    def clear(self):
        default_history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

        with open(self.file_path, "w") as file:
            json.dump(default_history, file, indent=4)

        return default_history