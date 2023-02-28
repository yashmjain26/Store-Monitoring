from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()


@dataclass
class StoreStatus(Base):
    __tablename__ = "status_update"

    id = Column(Integer, primary_key=True, autoincrement=True)
    store_id = Column(Integer, nullable=False)
    timestamp_utc = Column(DateTime, nullable=False)
    status = Column(String(10), nullable=False)
    store = relationship("Store", back_populates="status_updates")

    # method to get store status by store id and timestamp
    @classmethod
    def get_store_status_by_id_and_timestamp(
        cls, store_id: int, timestamp_utc: str
    ) -> StoreStatus:
        return (
            cls.query(StoreStatus)
            .filter(
                StoreStatus.store_id == store_id,
                StoreStatus.timestamp_utc == timestamp_utc,
            )
            .first()
        )

    # method to create store status
    @classmethod
    def create_store_status(
        cls, store_id: int, timestamp_utc: str, status: str
    ) -> StoreStatus:

        store_status = StoreStatus(
            store_id=store_id, timestamp_utc=timestamp_utc, status=status
        )
        cls.add(store_status)
        cls.commit()
        cls.refresh(store_status)
        return store_status

    # method to update store status
    @classmethod
    def update_store_status(
        cls, store_id: int, timestamp_utc: str, status: str
    ) -> StoreStatus:
        store_status = get_store_status_by_id_and_timestamp(
            cls, store_id, timestamp_utc
        )
        if store_status:
            store_status.status = status
            cls.commit()
            cls.refresh(store_status)
        else:
            store_status = create_store_status(cls, store_id, timestamp_utc, status)
        return store_status
