from typing import Any, Literal, Optional, Annotated
from dataclasses import dataclass
from datetime import date
from pydantic import BaseModel, Field, EmailStr, GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic import BaseModel, GetCoreSchemaHandler

class RegisterAccount(BaseModel):
    email: EmailStr = Field(max_length=255, title="Email of your account")
    password: str = Field(title="Your password")
    NIM: str = Field(max_length=10, title="Your NIM")
    name: str = Field(max_length=250, title="Your name")
    class_name: str = Field(max_length=30, title="Your class")
    address: str = Field(title="Your address")
    birthdate: date = Field(title="Your birthdate (only date)")
    gender: Literal["Laki-Laki", "Perempuan"] = Field(title="Your gender")
    
class Login(BaseModel):
    email: EmailStr = Field(max_length=255, title="Email of your account")
    password: str = Field(title="Your password")
    
class UpdateMe(BaseModel):
    email: Optional[EmailStr] = Field(max_length=255, title="Email of your account", default=None)