from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: str = Field(..., min_length=1)
    
class ChatResponse(BaseModel):
    user_message: str
    bot_reply: str
    intent: str
    session_id: str
    request_id: str

class ResetResponse(BaseModel):
    message: str
    session_id: str

class ResetRequest(BaseModel):
    session_id: str = Field(..., min_length=1)