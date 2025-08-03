from pydantic import BaseModel, Field

class ChromaIngestionSchema(BaseModel):
    file_name:str = Field(default="")
    fileId: str = Field(default="")

    def to_dict(self):
        return self.model_dump(exclude_none=True)