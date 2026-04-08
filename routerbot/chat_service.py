import logging
from routing import classify_intent, handlers
from config import RAG_TOP_K
from chat_log_repository import ChatLogRepository

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self, memory, retriever, debug=False):
        self.memory = memory
        self.debug = debug
        self.retriever = retriever
        self.chat_log_repository = ChatLogRepository()
        


    def process_message(self, message, session_id, request_id, use_rag=True, debug=False):
        cleaned_message = message.strip()

        if not cleaned_message:
            raise ValueError("Input message cannot be empty or whitespace.")
        
        logger.info(
            "[request_id=%s] flow=start session_id=%s message_length=%s use_rag=%s debug=%s",
            request_id,
            session_id,
            len(cleaned_message),
            use_rag,
            debug or self.debug
        )

        logger.info(
            "[request_id=%s] flow=memory_load_start session_id=%s",
            request_id,
            session_id
        )

        chat_history = self.memory.load()
        logger.info(
            "[request_id=%s] flow=memory_load_done session_id=%s history_messages=%s",
            request_id,
            session_id,
            len(chat_history)
        )

        logger.info(
            "[request_id=%s] flow=classify_start session_id=%s",
            request_id,
            session_id
        )


        intent = classify_intent(cleaned_message)
        logger.info(
            "[request_id=%s] flow=classify_done session_id=%s intent=%s",
            request_id,
            session_id,
            intent
        )


        retrieved_chunks = []
        rag_used = False

        if use_rag:
            logger.info(
                "[request_id=%s] flow=retrieve_start session_id=%s top_k=%s",
                request_id,
                session_id,
                RAG_TOP_K
            )

            retrieved_chunks = self.retriever.retrieve(cleaned_message, top_k=RAG_TOP_K)
            rag_used = len(retrieved_chunks) > 0

            if rag_used:
                top_chunk_summary = ", ".join(
                    f"{chunk['id']}:{chunk['score']}"
                    for chunk in retrieved_chunks[:3]
                )
                logger.info(
                    "[request_id=%s] flow=retrieve_done session_id=%s rag_used=%s retrieved_count=%s top_chunks=%s",
                    request_id,
                    session_id,
                    rag_used,
                    len(retrieved_chunks),
                    top_chunk_summary
                )

            else:
                logger.info(
                    "[request_id=%s] flow=retrieve_done session_id=%s rag_used=%s retrieved_count=0",
                    request_id,
                    session_id,
                    rag_used
                )

        else:
            logger.info(
                "[request_id=%s] flow=retrieve_skipped session_id=%s rag_used=%s reason=rag_disabled",
                request_id,
                session_id,
                rag_used
            )
    

        handler = handlers.get(intent, handlers["chat"]) # get the correct handler to what intent is otherwise return handler["chat"].
        logger.info(
            "[request_id=%s] flow=response_start session_id=%s intent=%s rag_used=%s",
            request_id,
            session_id,
            intent,
            rag_used
        )

        response = handler(cleaned_message, chat_history, retrieved_chunks=retrieved_chunks)
        logger.info(
            "[request_id=%s] flow=response_done session_id=%s intent=%s rag_used=%s response_length=%s",
            request_id,
            session_id,
            intent,
            rag_used,
            len(response)
        )

        logger.info(
            "[request_id=%s] flow=memory_save_start session_id=%s",
            request_id,
            session_id
        )

        self.memory.save(chat_history)
        logger.info(
            "[request_id=%s] flow=memory_save_done session_id=%s history_messages=%s",
            request_id,
            session_id,
            len(chat_history)
        )

        logger.info(
            "[request_id=%s] flow=db_save_start session_id=%s intent=%s rag_used=%s",
            request_id,
            session_id,
            intent,
            rag_used
        )

        self.chat_log_repository.save_chat_log(
            session_id=session_id,
            request_id=request_id,
            user_message=cleaned_message,
            bot_reply=response,
            intent=intent,
            rag_used=rag_used
        )

        logger.info(
            "[request_id=%s] flow=db_save_done session_id=%s intent=%s rag_used=%s",
            request_id,
            session_id,
            intent,
            rag_used
        )

        logger.info(
            "[request_id=%s] flow=complete session_id=%s intent=%s rag_used=%s response_length=%s",
            request_id,
            session_id,
            intent,
            rag_used,
            len(response)
        )


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