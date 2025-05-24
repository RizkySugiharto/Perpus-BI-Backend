from fastapi import APIRouter, Depends, HTTPException, status
from Src.models.databases.member import Member, MemberPublic, MemberCreate, MemberUpdate
from sqlmodel import select
from pydantic import BaseModel
from Src.database import SessionDep
from Src.dependecies import authenticate, isAdmin

router = APIRouter(prefix='/members', dependencies=[Depends(authenticate), Depends(isAdmin)])

@router.get('', response_model=list[MemberPublic])
async def get_all_members(session: SessionDep):
    members = session.exec(select(Member)).all()
    return members

@router.get('/{NIM}', response_model=MemberPublic)
async def get_member(NIM: str, session: SessionDep):
    member = session.get(Member, NIM)
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    
    return member

@router.post('', response_model=MemberPublic, status_code=status.HTTP_201_CREATED)
async def create_member(member: MemberCreate, session: SessionDep):
    member_db = Member.model_validate(member)
    session.add(member_db)
    session.commit()
    session.refresh(member_db)
    
    return member_db

@router.patch('/{NIM}', response_model=MemberPublic)
async def update_member(NIM: str, member: MemberUpdate, session: SessionDep):
    member_db = session.get(Member, NIM)
    if not member_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    
    member_data = member.model_dump(exclude_unset=True)
    member_db.sqlmodel_update(member_data)
    session.add(member_db)
    session.commit()
    session.refresh(member_db)
    
    return member_db

@router.delete('/{NIM}', response_model=BaseModel)
async def delete_member(NIM: str, session: SessionDep):
    member_db = session.get(Member, NIM)
    if not member_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    
    session.delete(member_db)
    session.commit()
    
    return {}