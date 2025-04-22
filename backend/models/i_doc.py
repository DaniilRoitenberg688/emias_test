from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class IDoc(Base):
    __tablename__ = "i_doc"

    ser: Mapped[str] = mapped_column(String, nullable=False)
    num: Mapped[str] = mapped_column(String, nullable=False)
    give_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)