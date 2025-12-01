import requests
import math
from typing import Optional, Tuple
from get_coords import geocode_address, OVERPASS_URL, get_geolocator
from WeatherAPI import get_height
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


'''здесь рассчитываем по координатам улицы количество снега на этой улице
возвращаем словарь со значениями координат, объема снега и тп'''



GEOLOCATOR = get_geolocator()
SNOW_DEPTH = 5 # ЗАМЕНИТЬ НА ФУНКЦИЮ ВЕДЕРАПИ, ПРОСТО СНЕГА ЩАС НЕТ

ROAD_WIDTHS_M = {
    "pedestrian": 6.0,
    "footway": 5.0,
    "residential": 5.0,
    "tertiary": 6.0,
    "secondary": 6.5,
    "primary": 7.5,
    "default": 6.5
}

SNOW_DENSITY_KG_M3 = 70.0
MAX_LOAD_PER_TRUCK_KG = 10000 # БУДЕМ БРАТЬ ИЗ БД (ПО УМОЛЧАНИЮ БУДЕТ 10К ПОКА ЧТО


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)
    a = math.sin(Δφ / 2) ** 2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def overpass_query_with_retry(query: str, max_retries: int = 3, backoff_factor: float = 1.0):
    url = "https://overpass-api.de/api/interpreter"

    # Настройка политики повторных попыток
    retry_strategy = Retry(
        total=max_retries,
        status_forcelist=[429, 500, 502, 503, 504],  # включаем 504
        allowed_methods=["POST", "GET"],
        backoff_factor=backoff_factor,  # 1 => задержки: 1, 2, 4 сек
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    try:
        response = session.post(
            url,
            data={"data": query},
            timeout=(10, 30)  # connect timeout = 10s, read timeout = 30s
        )
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Overpass query failed after {max_retries + 1} attempts: {e}")
        raise
def get_road_at(lat: float, lon: float, radius_m: float = 20.0) -> Optional[Tuple[float, float, str]]:
    query = f"""
    [out:json][timeout:15];
    way(around:{radius_m},{lat},{lon})["highway"];
    out geom;
    """
    try:
        response = overpass_query_with_retry(query)
        response.raise_for_status()
        data = response.json()

        ways = [e for e in data.get("elements", []) if e.get("type") == "way"]
        if not ways:
            print(f"❌ Нет дорог в радиусе {radius_m} м от ({lat:.5f}, {lon:.5f})")
            return None

        way = ways[0]
        geom = way.get("geometry", [])
        if len(geom) < 2:
            return None

        length_m = sum(
            haversine_m(
                geom[i - 1]["lat"], geom[i - 1]["lon"],
                geom[i]["lat"], geom[i]["lon"]
            )
            for i in range(1, len(geom))
        )

        tags = way.get("tags", {})
        highway_type = tags.get("highway", "default")
        width_m = ROAD_WIDTHS_M.get(highway_type, ROAD_WIDTHS_M["default"])

        w_tag = tags.get("width")
        if w_tag:
            try:
                clean = ''.join(c for c in str(w_tag) if c in '0123456789.,')
                if clean:
                    width_m = float(clean.replace(',', '.'))
            except:
                pass

        return length_m, width_m, highway_type

    except Exception as e:
        print(f"❌ Overpass error: {e}")
        return None


def calculate_snow_at_address(address: str, city: str = "Казань", snow_depth_cm: float = SNOW_DEPTH):
    print(f"Расчёт снега для адреса: {address}, {city}")

    coords = geocode_address(address, city)
    if not coords:
        return None

    lat, lon = coords

    road_data = get_road_at(lat, lon)
    if not road_data:
        return None

    length_m, width_m, highway = road_data

    segment_length_m = min(length_m, 100.0)
    area_m2 = segment_length_m * width_m
    volume_m3 = area_m2 * (snow_depth_cm / 100.0)
    mass_kg = volume_m3 * SNOW_DENSITY_KG_M3
    trucks = math.ceil(mass_kg / MAX_LOAD_PER_TRUCK_KG)
    '''
    print("\n" + "=" * 55)
    print(f"Снег у адреса: {address}")
    print("=" * 55)
    print(f"Координаты:          {lat:.5f}, {lon:.5f}")
    print(f"Тип дороги:          {highway}")
    print(f"Длина участка:       {segment_length_m:.0f} м")
    print(f"Ширина:              {width_m:.1f} м")
    print(f"Площадь:             {area_m2:,.0f} м²")
    print(f"Глубина снега:       {snow_depth_cm} см")
    print(f"Объём снега:         {volume_m3:.1f} м³")
    print(f"Масса снега:         {mass_kg:,.0f} кг ({mass_kg / 1000:.1f} т)")
    print("-" * 55)
    print(f"Требуется рейсов: {trucks}")
    print("=" * 55)
    '''
    return {
        "address": address,
        "lat": lat,
        "lon": lon,
        "length_m": segment_length_m,
        "area_m2": round(area_m2),
        "snow_mass_kg": round(mass_kg, 1),
        "trucks_needed": trucks,
        "volume_m3": round(volume_m3, 1)
    }
#print(calculate_snow_at_address("Восход 16"))