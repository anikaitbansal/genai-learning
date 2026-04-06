import logging
from routing import classify_intent, handlers
from config import RAG_TOP_K

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, memory, retriever, debug=False):
        self.memory = memory
        self.debug = debug
        self.retriever = retriever
        

    def process_message(self, message, session_id, request_id, use_rag=True, debug=False):
        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Input message cannot be empty or whitespace.")

        chat_history = self.memory.load()
        intent = classify_intent(cleaned_message)

        logger.info(
            "[request_id=%s] Session %s classified intent: %s", 
            request_id, 
            session_id, 
            intent)

        retrieved_chunks = []
        rag_used = False

        if use_rag:
            retrieved_chunks = self.retriever.retrieve(cleaned_message, top_k=RAG_TOP_K)
            rag_used = len(retrieved_chunks) > 0

            logger.info(
                "[request_id=%s] Session %s vector retrieval returned %s chunks",
                request_id,
                session_id,
                len(retrieved_chunks)
                )
        else:
            logger.info(
                "[request_id=%s] Session %s RAG disabled for this request.",
                    request_id,
                    session_id
                )
    

        handler = handlers.get(intent, handlers["chat"]) # get the correct handler to what intent is otherwise return handler["chat"].
        response = handler(cleaned_message, chat_history, retrieved_chunks=retrieved_chunks)

        self.memory.save(chat_history)

        logger.info(
            "[request_id=%s] Session %s response generated successfully.", 
            request_id, 
            session_id)


        result = {
            "user_message": cleaned_message,
            "bot_reply": response,
            "intent": intent,
            "session_id": session_id,
            "rag_used": rag_used,
        }

        if debug or self.debug:
            result["retrieved_chunks"] = retrieved_chunks

        return result