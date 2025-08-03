from typing import List, Optional, Any
from pydantic import BaseModel
    
class RAGResponseModel(BaseModel):
    context: Optional[str] = None
    vector_results: Optional[List[Any]] = None

    def to_dict(self):
        return self.model_dump(exclude_none=True)
    
class MongoQueryResponseModel(BaseModel):
    results: Optional[List[Any]] = None

    def to_dict(self):
        return self.model_dump(exclude_none=True)
    
class ToolResponseModel(BaseModel):
    data: Optional[List[RAGResponseModel|MongoQueryResponseModel]] = None
    status: int
    message: str
    is_error: bool = True

    def to_dict(self):
        return self.model_dump(exclude_none=True)