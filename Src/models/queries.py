from typing import Annotated, Literal

from fastapi import Query
from pydantic import BaseModel, Field

class _GetAllLoans(BaseModel):
    all: bool = Field(False)
    
class _GetAllBooks(BaseModel):
    search: str = Field('')
    
GetAllLoans = Annotated[_GetAllLoans, Query()]
GetAllBooks = Annotated[_GetAllBooks, Query()]