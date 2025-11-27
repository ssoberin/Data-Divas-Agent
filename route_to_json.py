import requests
import json
from geopy.geocoders import Nominatim
from WeatherAPI import get_weather_data

USER_AGENT = "snow-removal-planner/1.0 (your-email@example.com)"
OSRM_URL = "http://localhost:5000"

WINTER_SPEED_FACTOR = 0.65
SNOW_DEPTH_THRESHOLD_CM = 5.0

geolocator = Nominatim(user_agent=USER_AGENT)

def format_duration(seconds: float) -> str:
    mins = int(seconds // 60)
    h, m = divmod(mins, 60)
    return f"{h} ч {m} мин" if h else f"{m} мин"


def geocode_address(address: str, city: str = "Казань") -> tuple[float, float] | None:
    try:
        loc = geolocator.geocode(f"{address}, {city}", timeout=10)
        return (loc.latitude, loc.longitude) if loc else None
    except Exception as e:
        print(f"Геокодирование '{address}': {e}")
        return None


def get_route_osrm(start: tuple[float, float], end: tuple[float, float]) -> dict | None:
    lon1, lat1 = start[1], start[0]
    lon2, lat2 = end[1], end[0]

    url = f"{OSRM_URL}/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data["code"] != "Ok":
            print(f"OSRM: {data.get('message')}")
            return None

        route = data["routes"][0]
        coords = route["geometry"]["coordinates"]
        nodes = [{"lat": lat, "lon": lon} for lon, lat in coords]

        duration_raw = route["duration"]
        duration_winter = duration_raw / WINTER_SPEED_FACTOR

        return {
            "nodes": nodes,
            "distance_m": route["distance"],
            "duration_raw_s": duration_raw,
            "duration_winter_s": duration_winter
        }
    except Exception as e:
        print(f"Ошибка OSRM: {e}")
        return None


def save_route_to_json(route_info: dict, filename: str = "route_plan.json"):
    d_km = route_info["distance_m"] / 1000
    dur_raw = format_duration(route_info["duration_raw_s"])
    dur_winter = format_duration(route_info["duration_winter_s"])

    result = {
        "route": {
            "distance_km": round(d_km, 2),
            "duration_normal": dur_raw,
            "duration_winter": dur_winter,
            "duration_winter_seconds": route_info["duration_winter_s"],
            "total_points": len(route_info["nodes"]),
            "nodes": route_info["nodes"]
        }
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Сохранено в {filename}")


if __name__ == "__main__":
    start_addr = "Улица Восход, 16"
    end_addr = "Улица Шамиля Усманова"
    city = "Казань"

    print(f"Анализ маршрута от: {start_addr} → До: {end_addr}, {city}")

    start = geocode_address(start_addr, city)
    end = geocode_address(end_addr, city)
    if not (start and end):
        exit(1)

    route = get_route_osrm(start, end)
    if not route:
        exit(1)

    save_route_to_json(route, filename="snow_route_plan.json")

    print("\n Итог:")
    print(f"    Расстояние: {route['distance_m']/1000:.2f} км")
    print(f"    Время (без снега): {format_duration(route['duration_raw_s'])}")
    print(f"    Время (с учётом снега): {format_duration(route['duration_winter_s'])}  [×{1/WINTER_SPEED_FACTOR:.1f}]")
    get_weather_data()


