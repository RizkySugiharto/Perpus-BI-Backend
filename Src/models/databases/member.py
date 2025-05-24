from sqlmodel import SQLModel, Field, String
from datetime import datetime, date
from typing import Optional, Literal

class MemberBase(SQLModel):
    NIM: str = Field(primary_key=True, max_length=10)
    name: str = Field(max_length=250)
    class_name: str = Field(max_length=30, alias='class')
    address: str = Field()
    birthdate: date = Field()
    gender: Literal['Laki-Laki', 'Perempuan'] = Field(sa_type=String(10))

class Member(MemberBase, table=True):
    __tablename__ = 'members'
    
    account_id: int = Field(foreign_key='accounts.account_id', unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MemberPublic(MemberBase):
    account_id: int
    created_at: datetime

class MemberCreate(MemberBase):
    NIM: str
    account_id: int
    name: str
    class_name: str
    address: str
    birthdate: date
    gender: Literal['Laki-Laki', 'Perempuan']

class MemberUpdate(MemberBase):
    name: Optional[str] = None
    class_name: Optional[str] = Field(default=None, alias='class')
    address: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[Literal['Laki-Laki', 'Perempuan']] = None
