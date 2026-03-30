from fastapi import APIRouter, HTTPException, Depends
from schemas import ChatRequest, ChatResponse, ResetResponse
from dependencies import get_memory, build_chat_service
from memory_manager import MemoryManager
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def home():
    return {"message": "chatbot is running."}

@router.get("/health")
def health():
    return {"status": "healthy"}

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest,
         memory: MemoryManager = Depends(get_memory)
         ):
    try:
        logger.info(f"Received message: {request.message}")

        service = build_chat_service(memory)
        result = service.process_message(request.message)

        logger.info(f"Sending response: {result['intent']}")
        logger.info(f"Bot reply generated successfully.")

        return result
    
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.post("/reset", response_model=ResetResponse)
def reset(
    memory: MemoryManager = Depends(get_memory)
):
    try:
        logger.info("/reset called")

        memory.clear()
        
        return {"message": "Memory cleared."}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

