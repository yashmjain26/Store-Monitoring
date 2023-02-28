from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class Store(Base):
    __tablename__ = "store"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    timezone_str = Column(String(255), default="UST")
    business_hours = relationship("BusinessHour", back_populates="store")
    status_updates = relationship("StatusUpdate", back_populates="store")