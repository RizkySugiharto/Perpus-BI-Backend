from fastapi import APIRouter, Body, Response, HTTPException, status, Cookie, Depends, Request
from sqlmodel import select
from Src.models.requests import auth as req_auth
from Src.models.responses import auth as res_auth
from Src.models.databases.account import Account
from Src.models.databases.member import Member
from typing import Annotated
from Src.database import SessionDep
from pydantic import BaseModel
from Src import utils
from Src.dependecies import authenticate

router = APIRouter(prefix='/auth')

@router.post('/register', response_model=BaseModel, status_code=status.HTTP_201_CREATED)
async def register_account(data: Annotated[req_auth.RegisterAccount, Body(embed=True)], session: SessionDep):
    password_hash = utils.one_way_encrypt(data.password)
    db_account = Account.model_validate({
        'email': data.email,
        'password_hash': password_hash,
        'role': 'anggota',
    })
    session.add(db_account)
    session.commit()
    session.refresh(db_account)
    
    db_member = Member.model_validate({
        'account_id': db_account.account_id,
        'NIM': data.NIM,
        'name': data.name,
        'class_name': data.class_name,
        'address': data.address,
        'birthdate': data.birthdate,
        'gender': data.gender,
    })
    session.add(db_member)
    session.commit()
    
    return {}

@router.post('/login', response_model=res_auth.Login)
async def login(request: Request, data: Annotated[req_auth.Login, Body(embed=True)], session: SessionDep, response: Response):
    account = session.exec(select(Account).filter_by(email=data.email)).one_or_none()
    password_hash = utils.one_way_encrypt(data.password)
    
    if not account or account.deleted_at or account.password_hash != password_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email or password is not valid")
    if account and not account.activated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account isn't activated yet")

    jwt_token = utils.encode_to_jwt({
        'account_id': account.account_id
    })
    response.set_cookie(
        key='token',
        value=jwt_token,
        secure=True,
        httponly=True,
        samesite='none'
    )
    
    return {
        'token': jwt_token
    }

@router.post('/logout', response_model=BaseModel)
async def logout(response: Response):
    response.delete_cookie(key='token')
    return {}

@router.get('/me', response_model=res_auth.GetMe, dependencies=[Depends(authenticate)])
async def get_me(request: Request, session: SessionDep):
    account = session.get(Account, request.scope['account_id'])
    if not account or account.deleted_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account isn't found or maybe have been deleted")
    if account and not account.activated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account isn't activated yet")
    
    return account

@router.patch('/me', response_model=res_auth.UpdateMe, dependencies=[Depends(authenticate)])
async def update_me(request: Request, data: Annotated[req_auth.UpdateMe, Body(embed=True)], session: SessionDep):
    account_db = session.get(Account, request.scope['account_id'])
    if not account_db or account_db.deleted_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account isn't found or maybe have been deleted")
    if account_db and not account_db.activated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account isn't activated yet")
    
    account_db.sqlmodel_update({
        'email': data.email
    })
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    
    return account_db