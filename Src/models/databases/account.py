from pydantic import BaseModel
from sqlmodel import SQLModel, Field, String
from datetime import datetime
from typing import Literal, Optional

class AccountBase(SQLModel):
    email: str = Field(nullable=False, max_length=255, index=True, unique=True)
    password_hash: str = Field(nullable=False)
    role: Optional[Literal['anggota', 'admin']] = Field(default='anggota', nullable=False, sa_type=String(10))
    activated: bool = Field(default=False)

class Account(AccountBase, table=True):
    __tablename__ = 'accounts'
    
    account_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class AccountPublic(AccountBase):
    account_id: int
    created_at: datetime

class AccountCreate(BaseModel):
    email: str
    password: str
    role: Literal['anggota', 'admin'] = 'anggota'
    activated: Optional[bool] = False

class AccountUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[Literal['anggota', 'admin']] = None
    activated: Optional[bool] = None
