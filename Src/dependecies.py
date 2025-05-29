from fastapi import Header, status, HTTPException, Cookie, Request
from sqlmodel import select
from Src.models.databases.account import Account
from Src.database import SessionDep
from typing import Annotated, Optional, Union
from Src import utils
from Src.models.cookie import AuthCookie

def authenticate(request: Request, session: SessionDep, cookies: Annotated[AuthCookie, Cookie()], token: Annotated[str, Header()] = ''):
    if cookies and cookies.token:
        decoded = utils.decode_from_jwt(cookies.token)
    elif token:
        decoded = utils.decode_from_jwt(token)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
        
    if not decoded.get('account_id', False):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")
    
    account = session.get(Account, decoded['account_id'])
    if account and not account.activated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You account account isn't activated yet")
    
    request.scope['account_id'] = decoded['account_id']
    
def isAdmin(request: Request, session: SessionDep):
    account = session.get(Account, request.scope['account_id'])
    if account.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this endpoint")
    
def isAdminOrStaff(request: Request, session: SessionDep):
    account = session.get(Account, request.scope['account_id'])
    if not (account.role == 'admin' or account.role == 'staff'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have access to this endpoint")
    
def get_current_account(request: Request, session: SessionDep):
    account = session.get(Account, request.scope['account_id'])
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your account data not found")
    
    return account
        