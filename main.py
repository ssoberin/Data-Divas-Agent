from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, List
from sqlmodel import Session  
from database import create_db_and_tables, get_session, engine
from services import build_ai_prompt
from datetime import datetime
from models import (
    MasterCreate, MasterPublic, MasterUpdate,
    VehicleCreate, VehiclePublic, VehicleUpdate,
    StreetCreate, StreetPublic, StreetUpdate,
    StationCreate, StationPublic, StationUpdate
)
from crud import (
    create_master, read_masters, read_master, update_master, delete_master,
    create_vehicle, read_vehicles, read_vehicle, update_vehicle, delete_vehicle,
    create_street, read_streets, read_street, update_street, delete_street,
    create_station, read_stations, read_station, update_station, delete_station
)
from services import (
    get_all_data_for_prompt,
)

app = FastAPI(title="SnowExport Optimizer")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

SessionDep = Annotated[Session, Depends(get_session)]

@app.get("/")
def root():
    return {"message": "SnowExport Optimizer API"}

# REST для Мастеров
@app.post("/masters/", response_model=MasterPublic)
def api_create_master(master: MasterCreate, session: SessionDep):
    return create_master(session, master)

@app.get("/masters/", response_model=List[MasterPublic])
def api_read_masters(session: SessionDep, skip: int = 0, limit: int = 100):
    return read_masters(session, skip, limit)

@app.get("/masters/{master_id}", response_model=MasterPublic)
def api_read_master(master_id: int, session: SessionDep):
    return read_master(session, master_id)

@app.put("/masters/{master_id}", response_model=MasterPublic)
def api_update_master(master_id: int, master_update: MasterUpdate, session: SessionDep):
    return update_master(session, master_id, master_update)

@app.delete("/masters/{master_id}")
def api_delete_master(master_id: int, session: SessionDep):
    return delete_master(session, master_id)

# REST для Техники
@app.post("/vehicles/", response_model=VehiclePublic)
def api_create_vehicle(vehicle: VehicleCreate, session: SessionDep):
    return create_vehicle(session, vehicle)

@app.get("/vehicles/", response_model=List[VehiclePublic])
def api_read_vehicles(session: SessionDep, skip: int = 0, limit: int = 100):
    return read_vehicles(session, skip, limit)

@app.get("/vehicles/{vehicle_id}", response_model=VehiclePublic)
def api_read_vehicle(vehicle_id: int, session: SessionDep):
    return read_vehicle(session, vehicle_id)

@app.put("/vehicles/{vehicle_id}", response_model=VehiclePublic)
def api_update_vehicle(vehicle_id: int, vehicle_update: VehicleUpdate, session: SessionDep):
    return update_vehicle(session, vehicle_id, vehicle_update)

@app.delete("/vehicles/{vehicle_id}")
def api_delete_vehicle(vehicle_id: int, session: SessionDep):
    return delete_vehicle(session, vehicle_id)

# REST для Улиц
@app.post("/streets/", response_model=StreetPublic)
def api_create_street(street: StreetCreate, session: SessionDep):
    return create_street(session, street)

@app.get("/streets/", response_model=List[StreetPublic])
def api_read_streets(session: SessionDep, skip: int = 0, limit: int = 100):
    return read_streets(session, skip, limit)

@app.get("/streets/{street_id}", response_model=StreetPublic)
def api_read_street(street_id: int, session: SessionDep):
    return read_street(session, street_id)

@app.put("/streets/{street_id}", response_model=StreetPublic)
def api_update_street(street_id: int, street_update: StreetUpdate, session: SessionDep):
    return update_street(session, street_id, street_update)

@app.delete("/streets/{street_id}")
def api_delete_street(street_id: int, session: SessionDep):
    return delete_street(session, street_id)

# REST для Станций
@app.post("/stations/", response_model=StationPublic)
def api_create_station(station: StationCreate, session: SessionDep):
    return create_station(session, station)

@app.get("/stations/", response_model=List[StationPublic])
def api_read_stations(session: SessionDep, skip: int = 0, limit: int = 100):
    return read_stations(session, skip, limit)

@app.get("/stations/{station_id}", response_model=StationPublic)
def api_read_station(station_id: int, session: SessionDep):
    return read_station(session, station_id)

@app.put("/stations/{station_id}", response_model=StationPublic)
def api_update_station(station_id: int, station_update: StationUpdate, session: SessionDep):
    return update_station(session, station_id, station_update)

@app.delete("/stations/{station_id}")
def api_delete_station(station_id: int, session: SessionDep):
    return delete_station(session, station_id)

@app.get("/test_method")
def api_test_method(session: SessionDep):
    return get_all_data_for_prompt(session)


@app.get("/ai-prompt/")
def api_get_ai_prompt(session: SessionDep):
    """
    Возвращает структурированный промпт для AI-планировщика
    """
    return build_ai_prompt(session)


@router.post("/plan")
def generate_snow_cleaning_plan(
    planning_date: str,
    session: Session = Depends(get_session)
):
    """
    Генерация плана уборки снега с помощью нейросети и выгрузка CSV.
    """

    # Получаем данные из базы
    all_data = get_all_data_for_prompt(session)

    # Формируем промпт — сюда можно вставить системные ограничения и цели
    prompt = {
        "system_context": {
            "role": "Ты - система оптимизации вывоза снега для Казани...",
            "constraints": [
                "Уборка начинается при накопленных осадках >=5 см",
                "Техника должна использоваться рационально",
                "Баланc нагрузки станций",
                "И т.д."
            ]
        },
        "planning_date": planning_date,
        "weather_conditions": {
            "snow_expected": False,
            "snow_height_cm": 0,
            "risk_level": "low"
        },
        "available_resources": all_data,
        "optimization_goals": [
            "Минимизация пробега",
            "Баланс станций",
            "Приоритет по снегу"
        ],
        "output_format": {
            "required_structure": {
                "plan_date": "string",
                "total_streets": "int",
                "assigned_vehicles": "int",
                "assigned_brigades": "int",
                "routes": "list",
                "station_loading": "list",
                "shift_distribution": "list",
                "summary": "dict"
            }
        }
    }

    # 📌 Вызов ИИ
    try:
        llm_response = call_model_api(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Проверяем структуру ответа (легкая валидация)
    if "routes" not in llm_response:
        raise HTTPException(status_code=500, detail="Некорректный формат ответа от ИИ")

    # ----------------------
    # Генерация CSV
    # ----------------------
    filename = f"snow_plan_{planning_date}.csv"
    file_path = os.path.join(OUTPUT_CSV_DIR, filename)

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "street_id", "street_name", "vehicle_id", "vehicle_name",
            "brigade_id", "brigade_shift", "station_id", "station_name",
            "estimated_snow_volume", "estimated_trips", "priority",
            "shift_time", "route_sequence", "notes"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for route in llm_response.get("routes", []):
            writer.writerow(route)

    # Возвращаем JSON + файл
    return {
        "status": "success",
        "plan": llm_response,
        "csv_file": f"/snow-cleaning/csv/{filename}"
    }


@router.get("/csv/{filename}")
def download_csv(filename: str):
    file_path = os.path.join(OUTPUT_CSV_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="text/csv", filename=filename)