# crud.py
from sqlmodel import select
from fastapi import HTTPException
from typing import List, Optional
from models import (
    Master, MasterCreate, MasterUpdate, MasterPublic,
    Vehicle, VehicleCreate, VehicleUpdate, VehiclePublic,
    Street, StreetCreate, StreetUpdate, StreetPublic,
    Station, StationCreate, StationUpdate, StationPublic
)
from sqlmodel import Session

# Мастера
def create_master(session: Session, master: MasterCreate) -> MasterPublic:
    db_master = Master.from_orm(master)
    session.add(db_master)
    session.commit()
    session.refresh(db_master)
    return MasterPublic.from_orm(db_master)

def read_masters(session: Session, skip: int = 0, limit: int = 100) -> List[MasterPublic]:
    statement = select(Master).offset(skip).limit(limit)
    results = session.exec(statement).all()
    return [MasterPublic.from_orm(m) for m in results]

def read_master(session: Session, master_id: int) -> MasterPublic:
    master = session.get(Master, master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    return MasterPublic.from_orm(master)

def update_master(session: Session, master_id: int, master_update: MasterUpdate) -> MasterPublic:
    master = session.get(Master, master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    update_data = master_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(master, key, value)
    session.add(master)
    session.commit()
    session.refresh(master)
    return MasterPublic.from_orm(master)

def delete_master(session: Session, master_id: int):
    master = session.get(Master, master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    session.delete(master)
    session.commit()
    return {"detail": "Master deleted"}

# Аналогично для Vehicle (повторяющаяся логика, замените классы)
def create_vehicle(session: Session, vehicle: VehicleCreate) -> VehiclePublic:
    db_vehicle = Vehicle.from_orm(vehicle)
    session.add(db_vehicle)
    session.commit()
    session.refresh(db_vehicle)
    return VehiclePublic.from_orm(db_vehicle)

def read_vehicles(session: Session, skip: int = 0, limit: int = 100) -> List[VehiclePublic]:
    statement = select(Vehicle).offset(skip).limit(limit)
    results = session.exec(statement).all()
    return [VehiclePublic.from_orm(v) for v in results]

def read_vehicle(session: Session, vehicle_id: int) -> VehiclePublic:
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return VehiclePublic.from_orm(vehicle)

def update_vehicle(session: Session, vehicle_id: int, vehicle_update: VehicleUpdate) -> VehiclePublic:
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    update_data = vehicle_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vehicle, key, value)
    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)
    return VehiclePublic.from_orm(vehicle)

def delete_vehicle(session: Session, vehicle_id: int):
    vehicle = session.get(Vehicle, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    session.delete(vehicle)
    session.commit()
    return {"detail": "Vehicle deleted"}

# Для Street
def create_street(session: Session, street: StreetCreate) -> StreetPublic:
    db_street = Street.from_orm(street)
    session.add(db_street)
    session.commit()
    session.refresh(db_street)
    return StreetPublic.from_orm(db_street)

def read_streets(session: Session, skip: int = 0, limit: int = 100) -> List[StreetPublic]:
    statement = select(Street).offset(skip).limit(limit)
    results = session.exec(statement).all()
    return [StreetPublic.from_orm(s) for s in results]

def read_street(session: Session, street_id: int) -> StreetPublic:
    street = session.get(Street, street_id)
    if not street:
        raise HTTPException(status_code=404, detail="Street not found")
    return StreetPublic.from_orm(street)

def update_street(session: Session, street_id: int, street_update: StreetUpdate) -> StreetPublic:
    street = session.get(Street, street_id)
    if not street:
        raise HTTPException(status_code=404, detail="Street not found")
    update_data = street_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(street, key, value)
    session.add(street)
    session.commit()
    session.refresh(street)
    return StreetPublic.from_orm(street)

def delete_street(session: Session, street_id: int):
    street = session.get(Street, street_id)
    if not street:
        raise HTTPException(status_code=404, detail="Street not found")
    session.delete(street)
    session.commit()
    return {"detail": "Street deleted"}

# Для Station
def create_station(session: Session, station: StationCreate) -> StationPublic:
    db_station = Station.from_orm(station)
    session.add(db_station)
    session.commit()
    session.refresh(db_station)
    return StationPublic.from_orm(db_station)

def read_stations(session: Session, skip: int = 0, limit: int = 100) -> List[StationPublic]:
    statement = select(Station).offset(skip).limit(limit)
    results = session.exec(statement).all()
    return [StationPublic.from_orm(s) for s in results]

def read_station(session: Session, station_id: int) -> StationPublic:
    station = session.get(Station, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return StationPublic.from_orm(station)

def update_station(session: Session, station_id: int, station_update: StationUpdate) -> StationPublic:
    station = session.get(Station, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    update_data = station_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(station, key, value)
    session.add(station)
    session.commit()
    session.refresh(station)
    return StationPublic.from_orm(station)

def delete_station(session: Session, station_id: int):
    station = session.get(Station, station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    session.delete(station)
    session.commit()
    return {"detail": "Station deleted"}