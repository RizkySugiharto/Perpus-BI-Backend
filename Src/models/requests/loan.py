from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class CreateLoan(BaseModel):
    book_id: int = Field(title="Id of your book")
    loan_date: date = Field(title="Date of the loan")
    return_date: date = Field(title="Date of the return")
    taken: Optional[bool] = Field(title="Is it have been taken or not?", default=False)