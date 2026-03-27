from routing import classify_intent, handlers


class ChatService:
    def __init__(self, memory, debug=False):
        self.memory = memory
        self.debug = debug

    def process_message(self, message):
        chat_history = self.memory.load()
        intent = classify_intent(message)

        if self.debug:
            print("[DEBUG] Intent:", intent)
        else:
            print("Intent:", intent)

        handler = handlers.get(intent)
        if not handler:
            handler = handlers["chat"]

        if self.debug:
            print("[DEBUG] handler:", handler.__name__)

        response = handler(message, chat_history)

        self.memory.save(chat_history)

        return response