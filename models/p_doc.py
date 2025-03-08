from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class PDoc(Base):
    __tablename__ = "p_doc"

    ser: Mapped[str] = mapped_column(String, nullable=False)
    num: Mapped[str] = mapped_column(String, nullable=False)
    give_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    give_place: Mapped[str] = mapped_column(String, nullable=False)