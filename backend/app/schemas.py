from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ======================
# Employee Schemas
# ======================


class EmployeeCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    


class EmployeeResponse(BaseModel):
    id: int
    emp_id: str
    name: str
    email: Optional[EmailStr] = None
    

    class Config:
        from_attributes = True

