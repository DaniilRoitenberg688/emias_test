from models import PDoc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

async def create_p_doc(session: AsyncSession, p_doc: PDoc):
    session.add(p_doc)
    await session.commit()
    return p_doc

async def get_p_doc(session: AsyncSession, p_doc_id: int):
    p_doc = await session.get(PDoc, p_doc_id)
    if not p_doc:
        raise HTTPException(status_code=404, detail="P_doc not found")
    return p_doc

async def update_p_doc(session: AsyncSession, p_doc_id: int, p_doc_data):
    p_doc = await session.get(PDoc, p_doc_id)
    if not p_doc:
        raise HTTPException(status_code=404, detail="P_doc not found")
    
    p_doc.ser = p_doc_data.ser
    p_doc.num = p_doc_data.num
    p_doc.give_date = p_doc_data.give_date
    p_doc.give_place = p_doc_data.give_place

    await session.commit()
    return p_doc


async def delete_p_doc(session: AsyncSession, p_doc_id: int):
    p_doc = await session.get(PDoc, p_doc_id)
    if not p_doc:
        raise HTTPException(status_code=404, detail="P_doc not found")
    await session.delete(p_doc)
    await session.commit()
    return p_doc