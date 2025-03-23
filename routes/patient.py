from fastapi import APIRouter, Depends
from typing import Annotated

from pydantic import BaseModel, field_serializer

from datetime import datetime

from database import get_session

from services.patient import *

router = APIRouter(prefix='/patient', tags=['Patient'])

class PatientOut(BaseModel):
    id: int
    name: str
    surname: str
    birth: datetime
    p_doc_id: int = None
    i_doc_id: int = None

    @field_serializer('birth')
    def serialize_birth(self, value: datetime):
        return datetime.strftime(value, '%d-%m-%Y')

class PatientIn(BaseModel):
    pass

@router.get('/{id}', response_model=PatientOut)
async def get_patient_route(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    patient: Patient = await get_patient(session=session, patient_id=id)
    return PatientOut(
        id=patient.id,
        name=patient.name,
        surname=patient.surname,
        birth=patient.birth,
        p_doc_id=patient.p_doc_id,
        i_doc_id=patient.i_doc_id
    )

