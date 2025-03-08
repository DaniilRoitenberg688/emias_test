from models import IDoc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException


async def create_i_doc(session: AsyncSession, i_doc: IDoc):
    session.add(i_doc)
    await session.commit()

async def get_i_doc(session: AsyncSession, i_doc_id: int):
    i_doc = await session.get(IDoc, i_doc_id)
    if not i_doc:
        raise HTTPException(status_code=404, detail="I_doc not found")
    return i_doc

async def update_i_doc(session: AsyncSession, i_doc_id: int, i_doc_data: IDoc):
    i_doc = await session.get(IDoc, i_doc_id)
    if not i_doc:
        raise HTTPException(status_code=404, detail="I_doc not found")
    i_doc.ser = i_doc_data.ser
    i_doc.num = i_doc_data.num
    i_doc.give_date = i_doc_data.give_date
    await session.commit()
    return i_doc

async def delete_i_doc(session: AsyncSession, i_doc_id: int):
    i_doc = await session.get(IDoc, i_doc_id)
    if not i_doc:
        raise HTTPException(status_code=404, detail="I_doc not found")
    await session.delete(i_doc)
    await session.commit()