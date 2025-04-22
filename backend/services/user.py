from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException


async def create_user(session: AsyncSession, name: str, surname: str):
    user = User()
    user.name = name
    user.surname = surname
    session.add(user)
    await session.commit()
    return user


async def get_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



async def get_users(session: AsyncSession):
    users = await session.execute(select(User))
    return users.scalars().all()

async def delete_user(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()

async def update_user(session: AsyncSession, user_id: int, name: str, surname: str):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = name
    user.surname = surname
    await session.commit()
    return user

