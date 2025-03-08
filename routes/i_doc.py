from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import IDoc
from services import create_i_doc, get_i_doc, update_i_doc, delete_i_doc
from pydantic import BaseModel, Field, validator, field_serializer
from typing import Annotated
from datetime import datetime

router = APIRouter(prefix="/i_doc", tags=["i_doc"])

class IDocIn(BaseModel):
    ser: Annotated[str, Field(min_length=4, max_length=4)]
    num: Annotated[str, Field(min_length=6, max_length=6)]
    give_date: Annotated[datetime, Field(format="DD-MM-YYYY", example='12-12-2024')]

    @validator('give_date', pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            '%d-%m-%Y'
        ).date()

class IDocOut(BaseModel):
    id: int
    ser: str
    num: str
    give_date: datetime

    @field_serializer('give_date')
    def serialize_give_date(self, value: datetime):
        return datetime.strftime(value, '%d-%m-%Y')

@router.post("", response_model=IDocOut, status_code=201)
async def create_i_doc_route(i_doc_data: IDocIn, session: AsyncSession = Depends(get_session)):
    i_doc = IDoc()
    i_doc.ser = i_doc_data.ser
    i_doc.num = i_doc_data.num
    i_doc.give_date = i_doc_data.give_date
    await create_i_doc(session, i_doc)
    return IDocOut(id=i_doc.id, ser=i_doc.ser, num=i_doc.num, give_date=i_doc.give_date)

@router.get("/{i_doc_id}", response_model=IDocOut)
async def get_i_doc_route(i_doc_id: int, session: AsyncSession = Depends(get_session)):
    i_doc: IDoc = await get_i_doc(session, i_doc_id)
    return IDocOut(id=i_doc.id, num=i_doc.num, ser=i_doc.ser, give_date=i_doc.give_date)

@router.put("/{i_doc_id}", response_model=IDocOut)
async def update_i_doc_route(i_doc_id: int, i_doc_data: IDocIn, session: AsyncSession = Depends(get_session)):
    i_doc = await update_i_doc(session, i_doc_id, i_doc_data)
    return IDocOut(id=i_doc.id, num=i_doc.num, ser=i_doc.ser, give_date=i_doc.give_date)

@router.delete("/{i_doc_id}", status_code=204)
async def delete_i_doc_route(i_doc_id: int, session: AsyncSession = Depends(get_session)):
    await delete_i_doc(session, i_doc_id)