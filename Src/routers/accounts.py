from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from Src.models.databases.account import Account, AccountPublic, AccountCreate, AccountUpdate
from sqlmodel import select
from pydantic import BaseModel
from Src.database import SessionDep
from Src.dependecies import authenticate, isAdmin
from Src import utils

router = APIRouter(prefix='/accounts', dependencies=[Depends(authenticate), Depends(isAdmin)])

@router.get('', response_model=list[AccountPublic])
async def get_all_accounts(session: SessionDep):
    accounts = session.exec(select(Account).where(Account.deleted_at == None)).all()
    return accounts

@router.get('/{account_id}', response_model=AccountPublic)
async def get_account(account_id: int, session: SessionDep):
    account = session.get(Account, account_id)
    if not account or account.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    return account

@router.post('', response_model=AccountPublic, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate, session: SessionDep):
    password_hash = utils.one_way_encrypt(account.password)
    account_db = Account.model_validate({
        'email': account.email,
        'password_hash': password_hash,
        'role': account.role,
        'activated': account.activated,
    })
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    
    return account_db

@router.patch('/{account_id}', response_model=AccountPublic)
async def update_account(account_id: int, account: AccountUpdate, session: SessionDep):
    account_db = session.get(Account, account_id)
    if not account_db or account_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    account_data = account.model_dump(exclude_unset=True)
    account_db.sqlmodel_update(account_data)
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
        
    return account_db

@router.delete('/{account_id}', response_model=BaseModel)
async def delete_account(request: Request, account_id: int, session: SessionDep):
    account_db = session.get(Account, account_id)
    if not account_db or account_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    account_db.sqlmodel_update({
        'deleted_at': datetime.now(),
        'deleted_by': request.scope['account_id'],
    })
    session.add(account_db)
    session.commit()
    
    return {}