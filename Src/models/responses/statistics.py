from pydantic import BaseModel
from Src.models.databases.book import Book
from Src.models.databases.account import Account
    
class Statistics(BaseModel):
    count_active_loans: int
    most_borrowed_book: Book
    most_borrowed_member: Account