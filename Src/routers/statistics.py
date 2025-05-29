from fastapi import APIRouter, Depends, HTTPException, Request, status
from Src.models.databases.book import Book
from Src.models.databases.account import Account
from Src.models.databases.loan import Loan
from Src.models.responses.statistics import Statistics
from sqlmodel import select, col, or_, func, alias, desc
from Src.database import SessionDep
from Src.dependecies import authenticate, isAdminOrStaff

router = APIRouter(prefix='/statistics', dependencies=[Depends(authenticate), Depends(isAdminOrStaff)])

@router.get('', response_model=Statistics)
async def index(session: SessionDep):
    loans = session.exec(select(Loan).where(Loan.taken == True, Loan.returned == False)).all()
    count_loan = func.count(Loan.loan_id)
    book = session.exec(select(Book).group_by(Loan.book_id).join(Loan, Loan.book_id == Book.book_id).order_by(desc(count_loan))).first()
    account = session.exec(select(Account).group_by(Loan.account_id).join(Loan, Loan.account_id == Account.account_id).order_by(desc(count_loan))).first()
    
    return {
        'count_active_loans': len(loans),
        'most_borrowed_book': book,
        'most_borrowed_member': account,
    }