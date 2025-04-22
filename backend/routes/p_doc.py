from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import PDoc
from services.p_doc import create_p_doc, get_p_doc, update_p_doc, delete_p_doc
from database import get_session
from pydantic import BaseModel, Field, validator, field_serializer, ConfigDict
from typing import Annotated
from datetime import datetime
router = APIRouter(prefix="/p_doc", tags=["p_doc"])

class PDocIn(BaseModel):
    ser: Annotated[str, Field(min_length=4, max_length=4)]
    num: Annotated[str, Field(min_length=6, max_length=6)]
    give_place: Annotated[str, Field(min_length=1, max_length=100)]
    give_date: Annotated[datetime, Field(format="DD-MM-YYYY", example='12-12-1212')]

    @validator('give_date', pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            '%d-%m-%Y'
        ).date()


class PDocOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    ser: str
    num: str
    give_place: str
    give_date: datetime

    @field_serializer('give_date')
    def serialize_give_date(self, value: datetime):
        return datetime.strftime(value, '%d-%m-%Y')

@router.post("", response_model=PDocOut, status_code=201)
async def post_p_doc(p_doc_data: PDocIn, session: AsyncSession = Depends(get_session)) -> PDocOut:
    p_doc = PDoc()
    p_doc.ser = p_doc_data.ser
    p_doc.num = p_doc_data.num
    p_doc.give_place = p_doc_data.give_place
    p_doc.give_date = p_doc_data.give_date
    added_p_doc = await create_p_doc(session=session, p_doc=p_doc)
    return PDocOut(id=added_p_doc.id, ser=added_p_doc.ser, num=added_p_doc.num, give_place=added_p_doc.give_place, give_date=added_p_doc.give_date)


@router.get("/{p_doc_id}", response_model=PDocOut)
async def p_doc_get(p_doc_id: int, session: AsyncSession = Depends(get_session)) -> PDocOut:
    p_doc = await get_p_doc(session=session, p_doc_id=p_doc_id)
    return PDocOut(id=p_doc.id, ser=p_doc.ser, num=p_doc.num, give_place=p_doc.give_place, give_date=p_doc.give_date)

@router.delete("/{p_doc_id}", status_code=204)
async def p_doc_delete(p_doc_id: int, session: AsyncSession = Depends(get_session)):
    p_doc = await delete_p_doc(session=session, p_doc_id=p_doc_id)


@router.put("/{p_doc_id}", response_model=PDocOut)
async def p_doc_put(p_doc_id: int, p_doc_data: PDocIn, session: AsyncSession = Depends(get_session)) -> PDocOut:
    p_doc = await update_p_doc(session=session, p_doc_id=p_doc_id, p_doc_data=p_doc_data)
    return PDocOut(id=p_doc.id, ser=p_doc.ser, num=p_doc.num, give_place=p_doc.give_place, give_date=p_doc.give_date)


