from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional

class LoanBase(SQLModel):
    account_id: int = Field(foreign_key="accounts.account_id", nullable=False)
    book_id: int = Field(foreign_key="books.book_id", nullable=False)
    loan_date: date = Field(default_factory=datetime.utcnow, nullable=False)
    return_date: date = Field(default_factory=datetime.utcnow, nullable=False)
    taken: bool = Field(default=False, nullable=False)
    returned: bool = Field(default=False, nullable=False)

class Loan(LoanBase, table=True):
    __tablename__ = 'loans'
    
    loan_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    returned_at: Optional[date] = None
    current_paid_fine: Optional[int] = None
    deleted_at: Optional[datetime] = None
    deleted_by: Optional[int] = Field(default=None, foreign_key="accounts.account_id")

class LoanPublic(LoanBase):
    loan_id: int
    
class LoanFinePublic(BaseModel):
    loan_id: int
    taken: bool
    returned: bool
    return_date: Optional[date] = None
    current_paid_fine: Optional[int]
    returned_at: Optional[date]

class LoanCreate(BaseModel):
    book_id: int
    loan_date: date
    return_date: date
    taken: bool = False

class LoanUpdate(BaseModel):
    return_date: Optional[date] = None
    taken: Optional[bool] = None
    returned: Optional[bool] = None
    current_paid_fine: Optional[int] = None

