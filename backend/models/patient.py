from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, DateTime
from sqlalchemy import String, ForeignKey
from datetime import datetime


class Patient(Base):
    __tablename__ = "patient"

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    i_doc_id: Mapped[int] = mapped_column(ForeignKey("i_doc.id"), nullable=True)

    p_doc_id: Mapped[int] = mapped_column(ForeignKey("p_doc.id"), nullable=True)