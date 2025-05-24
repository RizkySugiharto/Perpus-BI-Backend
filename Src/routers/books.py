from fastapi import APIRouter, Depends, HTTPException, status
from Src.models.databases.book import Book, BookPublic, BookCreate, BookUpdate
from sqlmodel import select
from pydantic import BaseModel
from Src.database import SessionDep
from Src.dependecies import authenticate, isAdmin

router = APIRouter(prefix='/books', dependencies=[Depends(authenticate)])

@router.get('', response_model=list[BookPublic])
async def get_all_books(session: SessionDep):
    books = session.exec(select(Book)).all()
    return books

@router.get('/{book_id}', response_model=BookPublic)
async def get_book(book_id: int, session: SessionDep):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    return book

@router.post('', response_model=BookPublic, dependencies=[Depends(isAdmin)], status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, session: SessionDep):
    book_db = Book.model_validate(book)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    
    return book_db

@router.patch('/{book_id}', response_model=BookPublic, dependencies=[Depends(isAdmin)])
async def update_book(book_id: int, book: BookUpdate, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    book_data = book.model_dump(exclude_unset=True)
    book_db.sqlmodel_update(book_data)
    session.add(book_db)
    session.commit()
    session.refresh(book_db)
    
    return book_db

@router.delete('/{book_id}', response_model=BaseModel, dependencies=[Depends(isAdmin)])
async def delete_book(book_id: int, session: SessionDep):
    book_db = session.get(Book, book_id)
    if not book_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    session.delete(book_db)
    session.commit()
    
    return {}