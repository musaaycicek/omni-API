

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Float

class Base(DeclarativeBase):
    pass

class GDPRecord(Base):
    __tablename__ = "gdp_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String(100))
    country_code: Mapped[str] = mapped_column(String(10))
    year: Mapped[int] = mapped_column(Integer)
    value: Mapped[float] = mapped_column(Float, nullable=True)

