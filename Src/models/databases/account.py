from pydantic import BaseModel
from sqlmodel import SQLModel, Field, String
from datetime import datetime
from typing import Literal, Optional

class AccountBase(SQLModel):
    email: str = Field(nullable=False, max_length=255, index=True, unique=True)
    role: Optional[Literal['anggota', 'admin', 'staff']] = Field(default='anggota', nullable=False, sa_type=String(10))
    activated: bool = Field(default=False)

class Account(AccountBase, table=True):
    __tablename__ = 'accounts'
    
    account_id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="accounts.account_id")

class AccountPublic(AccountBase):
    account_id: int
    created_at: datetime

class AccountCreate(BaseModel):
    email: str
    password: str
    role: Literal['anggota', 'admin', 'staff'] = 'anggota'
    activated: Optional[bool] = False

class AccountUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[Literal['anggota', 'admin', 'staff']] = None
    activated: Optional[bool] = None
