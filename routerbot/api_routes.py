from fastapi import APIRouter, HTTPException, Depends
from schemas import ChatRequest, ChatResponse, ResetResponse, ResetRequest
from dependencies import get_memory, build_chat_service
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def home():
    return {"message": "chatbot is running."}

@router.get("/health")
def health():
    return {"status": "healthy"}

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    request_id = str(uuid.uuid4())

    try:
        logger.info("[request_id=%s] Received message for session: %s", request_id, request.session_id)
        
        memory = get_memory(request.session_id)
        service = build_chat_service(memory)
        
        result = service.process_message(request.message, request.session_id, request_id)

        result["request_id"] = request_id

        logger.info("[request_id=%s] Sending response for session: %s", request_id, request.session_id)
        return result
    
    except ValueError as error:
        logger.exception("[request_id=%s] Validation error in /chat", request_id)
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        logger.exception("[request_id=%s] Unexpected error in /chat", request_id)
        raise HTTPException(status_code=500, detail=str(error))

@router.post("/reset", response_model=ResetResponse)
def reset( request: ResetRequest):
    try:
        logger.info("/reset called for session: %s", request.session_id )
    
        memory = get_memory(request.session_id)
        memory.clear()

        return {"message": "Memory cleared.",
                "session_id": request.session_id
                }
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

