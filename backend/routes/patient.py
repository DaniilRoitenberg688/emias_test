from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import Annotated, ClassVar

from routes.i_doc import IDocOut
from routes.p_doc import PDocOut
from pydantic import BaseModel, field_serializer, Field, validator, ConfigDict

from datetime import datetime

from database import get_session

from services.patient import *

router = APIRouter(prefix='/patient', tags=['Patient'])

class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    surname: str
    birth: datetime
    p_doc_id: int | None = None
    i_doc_id: int | None = None


    @field_serializer('birth')
    def serialize_birth(self, value: datetime):
        return datetime.strftime(value, '%d-%m-%Y')

class PatientIn(BaseModel):
    name: str
    surname: str
    birth: Annotated[datetime, Field(format="DD-MM-YYYY", example='12-12-1212')]

    @validator('birth', pre=True)
    def parse_birth(cls, value):
        return datetime.strptime(
            value,
            '%d-%m-%Y'
        ).date()

@router.get('/{id}', response_model=PatientOut)
async def get_patient_route(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    patient: Patient = await get_patient(session=session, patient_id=id)
    return PatientOut.from_orm(patient)


@router.post('', response_model=PatientOut, status_code=201)
async def create_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient: PatientIn):
    patient: Patient = await create_patient(session=session, name=patient.name, surname=patient.surname, birth=patient.birth)
    return PatientOut.from_orm(patient)


@router.get('', response_model=list[PatientOut])
async def get_all_patients(session: Annotated[AsyncSession, Depends(get_session)]):
    patients: list[Patient] = await get_patients(session)
    return [PatientOut.from_orm(i) for i in patients]

@router.delete('/{id}', status_code=204)
async def delete_patient_route(session: Annotated[AsyncSession, Depends(get_session)], id: int):
    await delete_patient(session, patient_id=id)

@router.put('/{id}', status_code=200)
async def edit_patient_route(session: Annotated[AsyncSession, Depends(get_session)], id: int, patient_data: PatientIn):
    patient: Patient = await edit_patient(session, patient_id=id, **patient_data.model_dump())
    return PatientOut.from_orm(patient)

@router.post('/{patient_id}/p_doc/{p_doc_id}')
async def set_p_doc_for_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient_id: int, p_doc_id: int):
    await set_p_doc_for_patient(session, patient_id=patient_id, p_doc_id=p_doc_id)
    return JSONResponse({'answer': 'p_doc added successfully'})

@router.delete('/{patient_id}/p_doc', status_code=204)
async def delete_p_doc_for_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient_id: int):
    await delete_p_doc_for_patient(session, patient_id=patient_id)

@router.get('/{patient_id}/p_doc', response_model=PDocOut)
async def get_p_doc_for_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient_id: int):
    p_doc: PDoc = await get_p_doc_for_patient(session, patient_id=patient_id)
    return PDocOut.from_orm(p_doc)


@router.post('/{patient_id}/i_doc/{i_doc_id}')
async def set_i_doc_for_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient_id: int, i_doc_id: int):
    await set_i_doc_for_patient(session, patient_id=patient_id, i_doc_id=i_doc_id)
    return JSONResponse({'answer': 'i_doc added successfully'})

@router.delete('/{patient_id}/i_doc', status_code=204)
async def delete_i_doc_for_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient_id: int):
    await delete_i_doc_for_patient(session, patient_id=patient_id)

@router.get('/{patient_id}/i_doc', response_model=IDocOut)
async def get_i_doc_for_patient_route(session: Annotated[AsyncSession, Depends(get_session)], patient_id: int):
    i_doc: IDoc = await get_i_doc_for_patient(session, patient_id=patient_id)
    return IDocOut.from_orm(i_doc)
