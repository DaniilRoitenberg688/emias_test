from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient, PDoc, IDoc
from services.p_doc import get_p_doc
from services.i_doc import get_i_doc
from sqlalchemy import select

async def get_patient(session: AsyncSession, patient_id: int):
    patient: Patient | None = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, 'Not found such patient')
    return patient

async def get_patients(session: AsyncSession):
    query = select(Patient)
    res = await session.scalars(query)
    return res.all()

async def create_patient(session: AsyncSession, name, surname, birth):
    patient = Patient()
    patient.name = name
    patient.surname = surname
    patient.birth = birth

    session.add(patient)
    await session.commit()

    return patient

async def delete_patient(session: AsyncSession, patient_id: int):
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, 'no such patient')
    await session.delete(patient)
    await session.commit()

async def edit_patient(session: AsyncSession, patient_id, name, surname, birth):
    patient = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, 'no such patient')
    patient.name = name
    patient.surname = surname
    patient.birth = birth

    await session.commit()
    await session.refresh(patient)

    return patient


# async def get_patient_p_doc(session: AsyncSession, p_doc: PDoc, patient: Patient):


async def set_p_doc_for_patient(session: AsyncSession, p_doc_id: int, patient_id: int):
    p_doc: PDoc = await get_p_doc(session, p_doc_id=p_doc_id)
    patient: Patient = await get_patient(session, patient_id=patient_id)
    patient.p_doc_id = p_doc.id
    await session.commit()

async def get_p_doc_for_patient(session: AsyncSession, patient_id: int):
    patient: Patient = await get_patient(session, patient_id=patient_id)
    p_doc: PDoc = await get_p_doc(session, p_doc_id=patient.p_doc_id)
    return p_doc

async def delete_p_doc_for_patient(session: AsyncSession, patient_id: int):
    patient: Patient = await get_patient(session, patient_id=patient_id)
    patient.p_doc_id = None
    await session.commit()



async def set_i_doc_for_patient(session: AsyncSession, i_doc_id: int, patient_id: int):
    i_doc: IDoc = await get_i_doc(session, i_doc_id=i_doc_id)
    patient: Patient = await get_patient(session, patient_id=patient_id)
    patient.i_doc_id = i_doc.id
    await session.commit()

async def get_i_doc_for_patient(session: AsyncSession, patient_id: int):
    patient: Patient = await get_patient(session, patient_id=patient_id)
    i_doc: IDoc = await get_i_doc(session=session, i_doc_id=patient.i_doc_id)
    return i_doc


async def delete_i_doc_for_patient(session: AsyncSession, patient_id: int):
    patient: Patient = await get_patient(session, patient_id=patient_id)
    patient.i_doc_id = None
    await session.commit()

