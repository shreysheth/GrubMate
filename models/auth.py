from pydantic import BaseModel, EmailStr

class LoginModel(BaseModel):
    email: EmailStr
    password: str

    def to_dict(self):
        return self.model_dump(exclude_none=True)
    
class SignUpModel(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str

    def to_dict(self):
        return self.model_dump(exclude_none=True)