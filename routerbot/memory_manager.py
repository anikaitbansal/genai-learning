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

        logger.info("memory_stage=load_start file_path=%s", self.file_path)

        
        if os.path.exists(self.file_path):
            logger.info("memory_stage=file_found file_path=%s", self.file_path)
            try:
                with open(self.file_path, "r") as file:
                    chat_history = json.load(file)

                logger.info(
                "memory_stage=load_done file_path=%s message_count=%s",
                self.file_path,
                len(chat_history)
            )
                return chat_history
                
            except Exception as error: # we are trying to take a backup of our corrupted file by renaming it and if that fails too we return the default memory.
                backup_file = f"{self.file_path}.backup"
                logger.warning(
                    "memory_stage=load_failed file_path=%s error=%s",
                    self.file_path,
                    str(error)
                )

                try:
                    os.rename(self.file_path, backup_file)
                    logger.warning(
                        "memory_stage=backup_created original_file=%s backup_file=%s",
                        self.file_path,
                        backup_file
                    )

                except Exception as backup_error: 
                    logger.warning(
                        "memory_stage=backup_failed original_file=%s backup_file=%s error=%s",
                        self.file_path,
                        backup_file,
                        str(backup_error)
                    )

                logger.warning(
                    "memory_stage=load_fallback_default file_path=%s default_message_count=%s",
                    self.file_path,
                    len(default_history)
                )
                return default_history
            
        logger.info(
        "memory_stage=file_missing_using_default file_path=%s default_message_count=%s",
        self.file_path,
        len(default_history)
        )
        
        return default_history
    


    def save(self, chat_history):
        logger.info(
            "memory_stage=save_start file_path=%s message_count=%s",
            self.file_path,
            len(chat_history)
        )


        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(chat_history, file, indent=4)

        logger.info(
            "memory_stage=save_done file_path=%s message_count=%s",
            self.file_path,
            len(chat_history)
        )



    def clear(self):
        default_history = self.default_history()
        logger.info("memory_stage=clear_start file_path=%s", self.file_path)

        with open(self.file_path, "w") as file:
            json.dump(default_history, file, indent=4)
            
        logger.info(
        "memory_stage=clear_done file_path=%s message_count=%s",
        self.file_path,
        len(default_history)
    )

        return default_history