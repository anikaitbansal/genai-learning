from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    user_message: str
    bot_reply: str
    intent: str