from geopy.geocoders import Nominatim
import time
from typing import List, Tuple, Optional

'''здесь получаем координаты места'''


USER_AGENT = "snow-removal-planner/1.1 (khamidullovas@gmail.com)"
OSRM_URL = "http://localhost:5000"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


_geolocator = None
def get_geolocator():
    global _geolocator
    if _geolocator is None:
        _geolocator = Nominatim(user_agent=USER_AGENT, timeout=10)
    return _geolocator


def geocode_address(address: str, city: str = "Казань") -> Optional[Tuple[float, float]]:
    try:
        time.sleep(1.1)
        loc = get_geolocator().geocode(f"{address}, {city}")
        return (loc.latitude, loc.longitude) if loc else None
    except Exception as e:
        print(f"⚠️ Геокодирование '{address}': {e}")
        return None

#print(geocode_address("Улица Ленина, 1"))
