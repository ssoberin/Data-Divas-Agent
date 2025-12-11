import json
import os
from typing import List, Dict
from geopy.distance import geodesic
from rasstoyaniye import calculate_route_metrics

'''получение необходимых для cvrp величин из данных json файлов'''

WORKERS_PATH = os.path.join(os.path.dirname(__file__), "workers.json")
POINTS_PATH = os.path.join(os.path.dirname(__file__), "snow_points.json")

_depots_list = None
_points_list = None
_metadata = {}


def _load_workers() -> List[Dict]:
    global _depots_list
    if _depots_list is None:
        with open(WORKERS_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            if isinstance(raw, list):
                _depots_list = raw
            elif isinstance(raw, dict) and "depots" in raw:
                _depots_list = raw["depots"]
            else:
                raise ValueError(f"Неподдерживаемый формат workers.json: {type(raw)}")
    return _depots_list


def _load_points() -> List[Dict]:
    global _points_list, _metadata
    if _points_list is None:
        with open(POINTS_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
            if isinstance(raw, list):
                _points_list = raw
                _metadata = {}
            elif isinstance(raw, dict):
                _points_list = raw.get("points", [])
                _metadata = raw.get("metadata", {})
            else:
                raise ValueError(f"Неподдерживаемый формат snow_points.json: {type(raw)}")
    return _points_list


def get_all_points() -> List[Dict]:
    depots = _load_workers()
    points = _load_points()
    all_points = []

    for depot in depots:
        all_points.append({
            "type": "depot",
            "id": depot.get("depot_id", len(all_points)),
            "name": depot.get("depot_name", f"Депо-{len(all_points)}"),
            "lat": depot["depot_lat"],
            "lon": depot["depot_lon"],
            "address": depot.get("address", "")
        })

    for point in points:
        all_points.append({
            "type": "client",
            "id": point.get("point_id", len(all_points) - len(depots)),
            "address": point["address"],
            "lat": point["lat"],
            "lon": point["lon"],
            "snow_mass_kg": point.get("snow_mass_kg", 0),
            "volume_m3": point.get("volume_m3", 0)
        })
    return all_points


def matriza_ras() -> List[List[int]]:
    all_points = get_all_points()
    n_total = len(all_points)

    matrix = [[0] * n_total for _ in range(n_total)]

    for i in range(n_total):
        for j in range(i + 1, n_total):
            p_i = all_points[i]
            p_j = all_points[j]

            try:
                result = calculate_route_metrics(
                    p_i["lat"], p_i["lon"],
                    p_j["lat"], p_j["lon"]
                )
                dist_km = result["distance_km"]

                if dist_km is None or dist_km < 0:
                    dist_km = 1_000_000
                dist_units = int(round(dist_km * 10))
                matrix[i][j] = dist_units
                matrix[j][i] = dist_units

            except Exception as e:
                print(f"Fallback для {i}→{j}: {e}")

    return matrix


def demand_snega_mdvrp() -> List[int]:
    return [
        0 if p["type"] == "depot" else int(round(p["snow_mass_kg"]))
        for p in get_all_points()
    ]


def obyom_mashiny() -> List[int]:
    capacities = []
    for depot in _load_workers():
        for worker in depot["workers"]:
            capacities.append(int(round(worker["max_payload_kg"])))
    return capacities


def build_vehicle_to_depot() -> List[int]:
    mapping = []
    depot_index = 0
    for depot in _load_workers():
        mapping.extend([depot_index] * len(depot["workers"]))
        depot_index += 1
    return mapping


def get_worker_info() -> List[Dict]:
    workers = []
    depot_idx = 0
    for depot in _load_workers():
        for worker in depot["workers"]:
            workers.append({
                "vehicle_id": len(workers),
                "depot_id": depot["depot_id"],
                "depot_name": depot["depot_name"],
                "depot_address": depot.get("address", ""),
                "worker_name": worker["name"],
                "worker_phone": worker["phone"],
                "tech_type": worker["tech_type"],
                "max_payload_kg": worker["max_payload_kg"],
                "max_trips_per_day": worker.get("max_trips_per_day", 1),
                "status": worker.get("status", "unknown")
            })
        depot_idx += 1
    return workers


def get_client_addresses() -> Dict[int, str]:
    all_points = get_all_points()
    return {
        i: p["address"]
        for i, p in enumerate(all_points)
        if p["type"] == "client"
    }

#for i in matriza_ras():
 #   print(i)






