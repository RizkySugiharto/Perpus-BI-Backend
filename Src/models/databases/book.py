from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class BookBase(SQLModel):
    title: str = Field(nullable=False, max_length=255, index=True)
    author: str = Field(nullable=False, max_length=250, index=True)
    publisher: str = Field(nullable=False, max_length=250, index=True)
    published_year: Optional[int] = Field(default=None, index=True)
    stock: int = Field(default=1, nullable=False)

class Book(BookBase, table=True):
    __tablename__ = 'books'
    
    book_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class BookPublic(BookBase):
    book_id: int
    created_at: datetime

class BookCreate(BookBase):
    title: str
    author: str
    publisher: str
    published_year: Optional[int] = None
    stock: int = 1

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_year: Optional[int] = None
    stock: Optional[int] = None
