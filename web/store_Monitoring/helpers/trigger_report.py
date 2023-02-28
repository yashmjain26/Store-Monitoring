from sqlalchemy.orm import Session
from typing import List
from store_Monitoring.models.store import Store
from store_Monitoring.models.status_update import StoreStatus
from store_Monitoring.models.business_hour import StoreHours

# method to get store status by store id and timestamp
def get_store_status_by_id_and_timestamp(
    db: Session, store_id: int, timestamp_utc: str
) -> StoreStatus:
    return (
        db.query(StoreStatus)
        .filter(
            StoreStatus.store_id == store_id, StoreStatus.timestamp_utc == timestamp_utc
        )
        .first()
    )


# method to create store status
def create_store_status(
    db: Session, store_id: int, timestamp_utc: str, status: str
) -> StoreStatus:
    store_status = StoreStatus(
        store_id=store_id, timestamp_utc=timestamp_utc, status=status
    )
    db.add(store_status)
    db.commit()
    db.refresh(store_status)
    return store_status


# method to update store status
def update_store_status(
    db: Session, store_id: int, timestamp_utc: str, status: str
) -> StoreStatus:
    store_status = get_store_status_by_id_and_timestamp(db, store_id, timestamp_utc)
    if store_status:
        store_status.status = status
        db.commit()
        db.refresh(store_status)
    else:
        store_status = create_store_status(db, store_id, timestamp_utc, status)
    return store_status


# method to get store hours by store id and day of week
def get_store_hours_by_id_and_day_of_week(
    db: Session, store_id: int, day_of_week: int
) -> StoreHours:
    return (
        db.query(StoreHours)
        .filter(StoreHours.store_id == store_id, StoreHours.day_of_week == day_of_week)
        .first()
    )


# method to get all store hours by store id
def get_store_hours_by_id(db: Session, store_id: int) -> List[StoreHours]:
    return db.query(StoreHours).filter(StoreHours.store_id == store_id).all()


# method to create store hours
def create_store_hours(
    db: Session,
    store_id: int,
    day_of_week: int,
    start_time_local: str,
    end_time_local: str,
) -> StoreHours:
    store_hours = StoreHours(
        store_id=store_id,
        day_of_week=day_of_week,
        start_time_local=start_time_local,
        end_time_local=end_time_local,
    )
    db.add(store_hours)
    db.commit()
    db.refresh(store_hours)
    return store_hours


# method to update store hours
def update_store_hours(
    db: Session,
    store_id: int,
    day_of_week: int,
    start_time_local: str,
    end_time_local: str,
) -> StoreHours:
    store_hours = get_store_hours_by_id_and_day_of_week(db, store_id, day_of_week)
    if store_hours:
        store_hours.start_time_local = start_time_local
        store_hours.end_time_local = end_time_local
        db.commit()
        db.refresh(store_hours)
    else:
        store_hours = create_store_hours(
            db, store_id, day_of_week, start_time_local, end_time_local
        )
    return store_hours


# method to get store timezone by store id
def get_store_timezone_by_id(db: Session, store_id: int) -> Store:
    return db.query(Store).filter(Store.store_id == store_id).first()


# method to create store timezone
def create_store_timezone(db: Session, store_id: int, timezone_str: str) -> Store:
    store_timezone = Store(store_id=store_id, timezone_str=timezone_str)
    db.add(store_timezone)
    db.commit()
    db.refresh(store_timezone)
    return store_timezone
