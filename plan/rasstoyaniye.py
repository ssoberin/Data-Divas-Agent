import requests
from get_coords import geocode_address, OSRM_URL
from baumana import SNOW_DEPTH


'''здесь происходит запрос к osrm, то есть обяз дб развернута карта из data/
считаем маршрут от одной координаты до другой с учетом дорог и без/с учетом снега'''


WINTER_SPEED_FACTOR = 0.65
SNOW_DEPTH_THRESHOLD_CM = 4.0


def _get_route_osrm_raw(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> dict | None:
    url = f"{OSRM_URL}/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data["code"] != "Ok":
            return None
        route = data["routes"][0]
        return {
            "distance_m": route["distance"],
            "duration_s": route["duration"]
        }
    except Exception:
        return None


def calculate_route_metrics(
        snow_lat: float,
        snow_lon: float,
        depo_lat: float,
        depo_lon: float,
        snow_depth_cm: float = SNOW_DEPTH
) -> dict:

    route = _get_route_osrm_raw(snow_lat, snow_lon, depo_lat, depo_lon)
    if not route:
        return {
            "success": False,
            "distance_km": 0.0,
            "duration_normal_min": 0.0,
            "duration_winter_min": 0.0,
            "needs_removal": False
        }

    dist_km = route["distance_m"] / 1000
    dur_normal_min = route["duration_s"] / 60
    dur_winter_min = (route["duration_s"] / WINTER_SPEED_FACTOR) / 60
    needs_removal = snow_depth_cm > SNOW_DEPTH_THRESHOLD_CM

    return {
        "success": True,
        "distance_km": round(dist_km, 2),
        "duration_normal_min": round(dur_normal_min, 1),
        "duration_winter_min": round(dur_winter_min, 1),
        "needs_removal": needs_removal
    }

#print(calculate_route_metrics(55.7908696,49.0976020, 55.7756236, 49.2194394))