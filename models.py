from sqlmodel import SQLModel, Field
from typing import Optional, List
import json  # Для парсинга координат позже, но пока не используем

class MasterBase(SQLModel):
    name: str
    shift: str  # "дневная" | "ночная"

class Master(MasterBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    available: bool = Field(default=True)

class MasterCreate(MasterBase):
    pass

class MasterUpdate(SQLModel):
    name: Optional[str] = None
    shift: Optional[str] = None
    available: Optional[bool] = None

class MasterPublic(MasterBase):
    id: int
    available: bool

# Техника
class VehicleBase(SQLModel):
    name: str
    capacity: float  # тонны
    fuel_consumption: float  # л/км

class Vehicle(VehicleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    available: bool = Field(default=True)

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(SQLModel):
    name: Optional[str] = None
    capacity: Optional[float] = None
    fuel_consumption: Optional[float] = None
    available: Optional[bool] = None

class VehiclePublic(VehicleBase):
    id: int
    available: bool

# Улицы
class StreetBase(SQLModel):
    name: str
    points: str = Field(default="[]")  # JSON str для списка координат
    point_a: str  # JSON [lat, lon]
    point_b: str  # JSON [lat, lon]
    accumulated_precip: float = Field(default=0.0)
    status: str = Field(default="не убрана")
    prev_day_precip: float = Field(default=0.0)

class Street(StreetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class StreetCreate(StreetBase):
    pass

class StreetUpdate(SQLModel):
    name: Optional[str] = None
    points: Optional[str] = None
    point_a: Optional[str] = None
    point_b: Optional[str] = None
    accumulated_precip: Optional[float] = None
    status: Optional[str] = None
    prev_day_precip: Optional[float] = None

class StreetPublic(StreetBase):
    id: int

# Снегоплавильные станции
class StationBase(SQLModel):
    name: str
    coordinates: str  # JSON [lat, lon]
    capacity: int = Field(default=10)  # машин/час
    status: str = Field(default="открыта")
    current_load: int = Field(default=0)

class Station(StationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_dump: bool = Field(default=False)  # Для сухой свалки

class StationCreate(StationBase):
    is_dump: Optional[bool] = False

class StationUpdate(SQLModel):
    name: Optional[str] = None
    coordinates: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None
    current_load: Optional[int] = None
    is_dump: Optional[bool] = None

class StationPublic(StationBase):
    id: int
    is_dump: bool