# services.py
from sqlmodel import select, Session
from .models import Master, Vehicle, Street, Station
from typing import Dict, List, Any
import json  # Для парсинга JSON полей (координаты)

def get_masters_for_prompt(session: Session) -> List[Dict[str, Any]]:
    """
    Получает мастеров, группируя по бригадам (по 2 на бригаду), только доступных.
    """
    masters = session.exec(select(Master).where(Master.available == True)).all()
    brigades = []
    for i in range(0, len(masters), 2):
        brigade = masters[i:i+2]
        if len(brigade) >= 2:  # Только полные бригады
            brigades.append({
                "brigade_id": i // 2 + 1,  # Простой ID
                "masters": [{"id": m.id, "name": m.name, "shift": m.shift} for m in brigade],
                "shift": brigade[0].shift  # Предполагаем одинаковая смена в бригаде
            })
    return brigades

def get_vehicles_for_prompt(session: Session) -> List[Dict[str, Any]]:
    """
    Получает доступную технику с характеристиками.
    """
    vehicles = session.exec(select(Vehicle).where(Vehicle.available == True)).all()
    return [{
        "id": v.id,
        "name": v.name,
        "capacity": v.capacity,
        "fuel_consumption": v.fuel_consumption
    } for v in vehicles]

def get_streets_for_prompt(session: Session) -> List[Dict[str, Any]]:
    """
    Получает улицы, нуждающиеся в уборке (осадки >=5 см, не убрана), с координатами.
    """
    streets = session.exec(select(Street).where(
        Street.accumulated_precip >= 5,
        Street.status == "не убрана"
    )).all()
    return [{
        "id": s.id,
        "name": s.name,
        "point_a": json.loads(s.point_a),  # [lat, lon]
        "point_b": json.loads(s.point_b),  # [lat, lon]
        "accumulated_precip": s.accumulated_precip,
        "status": s.status
    } for s in streets]

def get_stations_for_prompt(session: Session) -> List[Dict[str, Any]]:
    """
    Получает открытые станции с загрузкой и координатами (включая свалки).
    """
    stations = session.exec(select(Station).where(Station.status == "открыта")).all()
    return [{
        "id": st.id,
        "name": st.name,
        "coordinates": json.loads(st.coordinates),  # [lat, lon]
        "capacity": st.capacity,
        "current_load": st.current_load,
        "is_dump": st.is_dump
    } for st in stations]

def get_all_data_for_prompt(session: Session) -> Dict[str, Any]:
    return {
        "brigades": get_masters_for_prompt(session),
        "vehicles": get_vehicles_for_prompt(session),
        "streets_to_clean": get_streets_for_prompt(session),
        "stations": get_stations_for_prompt(session)
    }