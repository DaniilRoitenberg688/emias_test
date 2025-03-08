from fastapi import APIRouter, Depends, HTTPException
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from services import *
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class UserOut(BaseModel):
    id: int
    name: str
    surname: str


class UserIn(BaseModel):
    name: str
    surname: str


@router.get("")
async def users_get(session: AsyncSession = Depends(get_session)) -> list[UserOut]:
    users = await get_users(session)
    return [UserOut(id=user.id, name=user.name, surname=user.surname) for user in users]


@router.post("", status_code=201)
async def users_post(user_data: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    user = User()
    user.name = user_data.name
    user.surname = user_data.surname
    session.add(user)
    await session.commit()
    return UserOut(id=user.id, name=user.name, surname=user.surname)


@router.delete("/{user_id}", status_code=204)
async def users_delete(user_id: int, session: AsyncSession = Depends(get_session)):
    await delete_user(session, user_id)


@router.get("/{user_id}")
async def user_get(user_id: int, session: AsyncSession = Depends(get_session)) -> UserOut:
    user = await get_user(session, user_id)
    return UserOut(id=user.id, name=user.name, surname=user.surname)


@router.put("/{user_id}")
async def user_put(user_id: int, user_data: UserIn, session: AsyncSession = Depends(get_session)) -> UserOut:
    user = await update_user(session, user_id, user_data.name, user_data.surname)
    return UserOut(id=user.id, name=user.name, surname=user.surname)

