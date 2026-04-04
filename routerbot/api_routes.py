import logging
from fastapi import APIRouter, HTTPException, Request
from schemas import ChatRequest, ChatResponse, ResetResponse, ResetRequest, FeedbackRequest, FeedbackSummaryResponse, BuildKnowledgeBaseResponse
from dependencies import get_memory, build_chat_service
from feedback_manager import FeedbackManager
from build_knowledge_base import build_knowledge_base

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", tags=["general"])
def home():
    return {"message": "chatbot is running."}



@router.get("/health", tags=["general"])
def health():
    return {"status": "healthy"}



@router.post("/chat", response_model=ChatResponse, tags=["chat"])
def chat(request: ChatRequest, http_request: Request):

    request_id = http_request.state.request_id

    try:
        logger.info("[request_id=%s] Received message for session: %s", request_id, request.session_id)
        
        memory = get_memory(request.session_id)
        service = build_chat_service(memory)
        
        result = service.process_message(
            request.message,
            request.session_id,
            request_id,
            use_rag=request.use_rag,
            debug=request.debug
        )
        
        logger.info("[request_id=%s] Sending response for session: %s", request_id, request.session_id)
        return result
    
    except ValueError as error:
        logger.exception("[request_id=%s] Validation error in /chat", request_id)
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        logger.exception("[request_id=%s] Unexpected error in /chat", request_id)
        raise HTTPException(status_code=500, detail=str(error))



@router.post("/reset", response_model=ResetResponse, tags=["chat"])
def reset( request: ResetRequest, http_request: Request):
    request_id = http_request.state.request_id

    try:
        logger.info("[request_id=%s] /reset called for session: %s", request_id, request.session_id)
    
        memory = get_memory(request.session_id)
        memory.clear()

        logger.info(
            "[request_id=%s] Memory cleared successfully for session: %s",
            request_id,
            request.session_id
        )

        return {"message": "Memory cleared.",
                "session_id": request.session_id,
                }
    
    except Exception as error:
        logger.exception(
            "[request_id=%s] Unexpected error in /reset",
            request_id
        )
        raise HTTPException(status_code=500, detail=str(error))
    


@router.post("/feedback", tags=["feedback"])
def submit_feedback(request: FeedbackRequest, http_request: Request):
    request_id = http_request.state.request_id

    try:
        logger.info(
            "[request_id=%s] Received feedback for session: %s (target_request_id=%s)",
            request_id,
            request.session_id,
            request.request_id
        )

        feedback_manager = FeedbackManager()

        entry = feedback_manager.create_feedback_entry(
            session_id=request.session_id,
            request_id=request.request_id,
            rating=request.rating,
            comments=request.comments
        )
        feedback_manager.save_feedback(entry)

        logger.info(
            "[request_id=%s] Feedback saved successfully for target_request_id=%s",
            request_id,
            request.request_id
        )

        return {"message": "Feedback submitted successfully.",
                }    
    except Exception as error:
        logger.exception(
            "[request_id=%s] Error while storing feedback",
            request_id
        )
        raise HTTPException(status_code=500, detail=str(error))
    


@router.get("/feedback/summary", response_model=FeedbackSummaryResponse, tags=["feedback"])
def feedback_summary(http_request: Request):
    request_id = http_request.state.request_id

    try:
        logger.info(
            "[request_id=%s] Fetching feedback summary",
            request_id
        )

        feedback_manager = FeedbackManager()
        summary = feedback_manager.get_summary()

        logger.info(
            "[request_id=%s] Feedback summary generated successfully",
            request_id
        )

        return summary

    except Exception as error:
        logger.exception(
            "[request_id=%s] Error while generating feedback summary",
            request_id
        )
        raise HTTPException(status_code=500, detail=str(error))
    


@router.post("/knowledge-base/rebuild", response_model=BuildKnowledgeBaseResponse, tags=["rag"])
def rebuild_knowledge_base(http_request: Request):
    request_id = http_request.state.request_id

    try:
        logger.info(
            "[request_id=%s] Rebuilding knowledge base",
            request_id
        )

        result = build_knowledge_base()

        logger.info(
            "[request_id=%s] Knowledge base rebuilt successfully | documents=%s | chunks=%s | file=%s",
            request_id,
            result["total_documents"],
            result["total_chunks"],
            result["knowledge_file"]
        )

        return result

    except Exception as error:
        logger.exception(
            "[request_id=%s] Error while rebuilding knowledge base: %s",
            request_id,
            str(error)
        )
        raise HTTPException(status_code=500, detail=str(error))