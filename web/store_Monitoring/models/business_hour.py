from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()

@dataclass
class StoreHours(Base):
    __tablename__ = "business_hour"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time_local = Column(DateTime, nullable=False)
    end_time_local = Column(DateTime, nullable=False)
    is_open_24_7 = Column(Boolean, default=False)
    store = relationship("Store", back_populates="business_hours")