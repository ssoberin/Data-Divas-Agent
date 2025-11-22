# services.py
from sqlmodel import select, Session
from models import Master, Vehicle, Street, Station
from typing import Dict, List, Any
import json  
from datetime import datetime, timedelta
from WeatherAPI import WeatherForecast

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
                "shift": brigade[0].shift  
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


def get_weather_for_prompt() -> Dict[str, Any]:
    """
    Получает данные о погоде для включения в промпт
    """
    try:
        wf = WeatherForecast(api_key="14eb71c084274841aa893453252211")
        result = wf.get_snow_forecast_analysis('Kazan', use_today=True)
        
        if not result:
            return {
                "snow_expected": True,  # По умолчанию предполагаем снег для демо
                "snow_height_cm": 8.0,
                "temperature_impact": "Умеренная температура",
                "work_recommendations": ["Планировать уборку снега"],
                "risk_level": "medium"
            }
        
        return result['snow_analysis']
    
    except Exception as e:
        print(f"❌ Ошибка получения погоды: {e}")
        return {
            "snow_expected": True,
            "snow_height_cm": 7.5,
            "temperature_impact": "Умеренная температура", 
            "work_recommendations": ["Планировать уборку снега"],
            "risk_level": "medium"
        }

def calculate_shift_schedule() -> Dict[str, Any]:
    """
    Рассчитывает расписание смен с временными интервалами
    """
    tomorrow = datetime.now() + timedelta(days=1)
    date_str = tomorrow.strftime('%Y-%m-%d')
    
    return {
        "plan_date": date_str,
        "shifts": {
            "дневная": {
                "start": "08:00",
                "end": "20:00",
                "description": "Основная рабочая смена"
            },
            "ночная": {
                "start": "20:00", 
                "end": "08:00",
                "description": "Ночная смена для непрерывной работы"
            }
        }
    }

def build_ai_prompt(session: Session) -> Dict[str, Any]:
    """
    Собирает все данные в структурированный промпт для нейросети
    """
    # Получаем все данные
    operational_data = get_all_data_for_prompt(session)
    weather_data = get_weather_for_prompt()
    schedule_data = calculate_shift_schedule()
    
    # Формируем промпт
    prompt = {
        "system_context": {
            "role": "Ты - система оптимизации вывоза снега для Казани. Твоя задача - создать оптимальный суточный план уборки снега с учетом всех доступных ресурсов и условий.",
            "constraints": [
                "Уборка начинается при накопленных осадках >=5 см",
                "Техника должна использоваться рационально с учетом ее вместимости",
                "Бригады распределяются по сменам (дневная/ночная)",
                "Нагрузка на снегоплавильные станции должна быть сбалансирована",
                "Сухие свалки используются только при перегрузке станций"
            ]
        },
        "planning_date": schedule_data["plan_date"],
        "weather_conditions": {
            "snow_expected": weather_data["snow_expected"],
            "snow_height_cm": weather_data["snow_height_cm"],
            "temperature_impact": weather_data["temperature_impact"],
            "risk_level": weather_data["risk_level"],
            "work_recommendations": weather_data["work_recommendations"]
        },
        "shift_schedule": schedule_data["shifts"],
        "available_resources": {
            "brigades": operational_data["brigades"],
            "vehicles": operational_data["vehicles"],
            "streets_to_clean": operational_data["streets_to_clean"],
            "stations": operational_data["stations"]
        },
        "optimization_goals": [
            "Минимизация общего пробега техники",
            "Балансировка нагрузки на станции",
            "Максимальное использование снегоплавильных пунктов",
            "Учет приоритета улиц по объему осадков", 
            "Эффективное распределение по сменам"
        ],
        "output_format": {
            "required_structure": {
                "plan_date": "string",
                "total_streets": "int", 
                "assigned_vehicles": "int",
                "assigned_brigades": "int",
                "routes": "list[dict]",
                "station_loading": "list[dict]",
                "shift_distribution": "list[dict]",
                "summary": "dict"
            },
            "route_fields": [
                "street_id", "street_name", "vehicle_id", "vehicle_name",
                "brigade_id", "brigade_shift", "station_id", "station_name",
                "estimated_snow_volume", "estimated_trips", "priority",
                "shift_time", "route_sequence", "notes"
            ],
            "shift_distribution_fields": [
                "shift_type", "brigade_count", "vehicle_count", 
                "streets_assigned", "start_time", "end_time"
            ]
        }
    }
    
    return prompt