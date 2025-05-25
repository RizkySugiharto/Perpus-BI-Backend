from fastapi import APIRouter, Depends, HTTPException, status, Request
from Src.models.databases.account import Account
from Src.models.databases.book import Book
from Src.models.databases.loan import Loan, LoanPublic, LoanUpdate
from Src.models.requests import loan as req_loan
from Src.models.queries import GetAllLoans as Q_GetAllLoans
from sqlmodel import select
from pydantic import BaseModel
from Src.database import SessionDep
from Src.dependecies import authenticate, isAdmin, get_current_account
from typing import Optional

router = APIRouter(prefix='/loans', dependencies=[Depends(authenticate)])

@router.get('', response_model=list[LoanPublic])
async def get_all_loans(session: SessionDep, query: Q_GetAllLoans, current_account: Account = Depends(get_current_account)):
    if current_account.role == 'admin' and query.all:
        loans = session.exec(select(Loan).where(Loan.deleted_at == None)).all()
    else:
        loans = session.exec(select(Loan).where(Loan.deleted_at == None).filter_by(account_id=current_account.account_id)).all()
        
    return loans

@router.get('/{loan_id}', response_model=LoanPublic)
async def get_loan(loan_id: int, session: SessionDep):
    loan = session.get(Loan, loan_id)
    if not loan or loan.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    
    return loan

@router.post('', response_model=LoanPublic, status_code=status.HTTP_201_CREATED)
async def create_loan(request: Request, loan: req_loan.CreateLoan, session: SessionDep, current_account: Account = Depends(get_current_account)):
    book_db = session.get(Book, loan.book_id)
    account_db = session.get(Account, loan.account_id)
    use_account_id = loan.account_id != None and current_account.role == 'admin'
    
    if use_account_id and not account_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Given account is not found")
    
    if not book_db or book_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    if book_db.stock < 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Book's stock isn't enough to be borrowed")
    
    loan_db = Loan.model_validate({
        'account_id': loan.account_id if use_account_id else request.scope['account_id'],
        'book_id': loan.book_id,
        'loan_date': loan.loan_date,
        'return_date': loan.return_date,
        'taken': loan.taken,
    })
    book_db.sqlmodel_update({
        'stock': book_db.stock - 1
    })
    
    session.add(loan_db)
    session.add(book_db)
    session.commit()
    session.refresh(loan_db)
    
    return loan_db

@router.patch('/{loan_id}', response_model=LoanPublic, dependencies=[Depends(isAdmin)])
async def update_loan(loan_id: int, loan: LoanUpdate, session: SessionDep):
    loan_db = session.get(Loan, loan_id)
    if not loan_db or loan_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    
    book_db = session.get(Book, loan_db.book_id)
    if not book_db or book_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    loan_data = loan.model_dump(exclude_unset=True)
    loan_db.sqlmodel_update(loan_data)
    session.add(loan_db)
    session.commit()
    session.refresh(loan_db)
    
    return loan_db

@router.delete('/{loan_id}', response_model=BaseModel, dependencies=[Depends(isAdmin)])
async def delete_loan(loan_id: int, session: SessionDep):
    loan_db = session.get(Loan, loan_id)
    if not loan_db or loan_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    
    book_db = session.get(Book, loan_db.book_id)
    if not book_db or book_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book_db.sqlmodel_update({
        'stock': book_db.stock + 1
    })
    session.add(book_db)
    session.delete(loan_db)
    session.commit()
    
    return {}