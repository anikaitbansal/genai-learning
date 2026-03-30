import logging
from routing import classify_intent, handlers


logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, memory, debug=False):
        self.memory = memory
        self.debug = debug

    def process_message(self, message):
        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Input message cannot be empty or whitespace.")
        
        chat_history = self.memory.load()
        intent = classify_intent(cleaned_message)

        if self.debug:
            logger.info(f"Intent: {intent}")
        #else:
            #print("Intent:", intent)

        handler = handlers.get(intent, handlers["chat"])
        if not handler:
            handler = handlers["chat"]

        if self.debug:
            logger.info(f"Handler: {handler.__name__}")

        response = handler(cleaned_message, chat_history)

        self.memory.save(chat_history)

        return {
            "user_message": cleaned_message,
            "bot_reply": response,
            "intent": intent

        }