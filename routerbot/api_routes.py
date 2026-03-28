from fastapi import APIRouter, HTTPException
from memory_manager import MemoryManager
from chat_service import ChatService
from schemas import ChatRequest, ChatResponse

router = APIRouter()

memory = MemoryManager("chat_history.json")
service = ChatService(memory, debug=True)

@router.get("/")
def home():
    return {"message": "chatbot is running."}

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = service.process_message(request.message)
        return result
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.post("/reset")
def reset():
    try:
        memory.clear()
        return {"message": "Memory cleared."}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))