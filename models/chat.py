from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatModel(BaseModel):
    question: str
    user_id: str 
    thread_id:Optional[str] = None

    def to_dict(self):
        return self.model_dump(exclude_none=True)
    
class MessageModel(BaseModel):
    thread_id:str
    message: str
    created_at: datetime

    def to_dict(self):
        return self.model_dump(exclude_none=True)
    
class ThreadModel(BaseModel):
    user_id: str
    created_at: datetime

    def to_dict(self):
        return self.model_dump(exclude_none=True)
    
class ChatResponseModel(BaseModel):
    message: str
    user_id: str
    thread_id: str
    message_id: str

    def to_dict(self):
        return self.model_dump(exclude_none=True)