from sqlalchemy.orm import Mapped, mapped_column
from database import Base, DateTime
from sqlalchemy import String
from datetime import datetime


class Patient(Base):
    __tablename__ = "patient"

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
