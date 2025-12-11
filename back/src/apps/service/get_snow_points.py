import json
from typing import List, Dict
from baumana import calculate_snow_at_address
from baumana import SNOW_DEPTH


'''берем из baumana словарь по одной улице, принимаем несколько таких, преобразуем в json'''

def collect_snow_points(
        addresses: List[str],
        city: str = "Казань",
        snow_depth_cm: float = SNOW_DEPTH,
        output_file: str = "snow_points.json"
) -> List[Dict]:
    points = []

    for addr in addresses:
        print(f"Обработка: {addr}")
        result = calculate_snow_at_address(addr, city, snow_depth_cm)
        if result:
            point = {
                "point_id": len(points) + 1,
                "address": result["address"],
                "lat": result["lat"],
                "lon": result["lon"],
                "length_m": result["length_m"],
                "area_m2": result["area_m2"],
                "snow_mass_kg": result["snow_mass_kg"],
                "trucks_needed": result["trucks_needed"],
                "volume_m3": result["volume_m3"]
            }
            points.append(point)
        else:
            print(f"Пропущен: {addr}")

    data = {
        "metadata": {
            "city": city,
            "snow_depth_cm": snow_depth_cm,
            "snow_density_kg_m3": 70.0,
            "generated_at": __import__("datetime").datetime.now().isoformat()
        },
        "points": points,
        "total_trucks_needed": sum(p["trucks_needed"] for p in points)
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nСохранено {len(points)} точек в '{output_file}'")
    print(f"Общее число рейсов: {data['total_trucks_needed']}")

    return points

