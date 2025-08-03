from pydantic import BaseModel
from typing import Optional, Dict

class ApiResponseModel(BaseModel):
    status: int
    message: str
    data: Optional[object] = None
    is_error: bool = True
    
    def to_dict(self):
        return self.model_dump(exclude_none=True)