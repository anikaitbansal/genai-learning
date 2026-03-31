import json
import os
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, file_path="chat_history.json"):
        self.file_path = file_path



    def default_history(self):
        return [
            {"role": "system", "content": "You are a helpful assistant."}
            ]



    def load(self): # This function loads the chat history from the specified JSON file.        
        default_history = self.default_history()
        
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as file:
                    return json.load(file)
            except Exception as error: # we are trying to take a backup of our corrupted file by renaming it and if that fails too we return the default memory.
                backup_file = f"{self.file_path}.backup"
                try:
                    os.rename(self.file_path, backup_file)
                    logger.warning("Corrupted memory backed up as %s", backup_file)
                except Exception as backup_error: 
                    logger.warning("Failed to create backup file %s", backup_file)
            
                logger.warning("Failed to load memory. Using default history.")
        
        return default_history
    


    def save(self, chat_history): # This function saves the current chat history to the specified JSON file. It opens the file in write mode and writes the chat_history list as JSON data. This allows us to persist the conversation history so that it can be loaded again in future sessions, maintaining continuity in the interactions with the chatbot.
        with open(self.file_path, "w") as file:
            json.dump(chat_history, file, indent=4)



    def clear(self):
        default_history = self.default_history()

        with open(self.file_path, "w") as file:
            json.dump(default_history, file, indent=4)

        return default_history