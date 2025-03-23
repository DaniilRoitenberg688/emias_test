from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models import Patient
from sqlalchemy import select

async def get_patient(session: AsyncSession, patient_id: int):
    patient: Patient | None = await session.get(Patient, patient_id)
    if not patient:
        raise HTTPException(404, 'Not found such patient')
    return patient

async def get_patients(session: AsyncSession) -> list[Patient]:
    query = select(Patient)
    patients: list[Patient] = await session.scalars(query).all()
    return patients

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
    await session.delete(patient)

async def edit_patient(session: AsyncSession, patient_id, name, surname, birth):
    patient = await session.get(Patient, patient_id)
    patient.name = name
    patient.surname = surname
    patient.birth = birth

    await session.commit()
    await session.refresh(patient)

    return patient