from typing import Literal, Optional
from datetime import date
from pydantic import BaseModel, EmailStr
    
class Login(BaseModel):
    token: str
    
class GetMe(BaseModel):
    account_id: int
    email: EmailStr
    role: Literal["anggota", "admin"]
    
class UpdateMe(BaseModel):
    account_id: int
    email: EmailStr
    role: Literal["anggota", "admin"]
    