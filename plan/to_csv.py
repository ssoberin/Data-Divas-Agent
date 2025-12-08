
import csv
import os
from typing import List, Dict, Any

def export_plan_to_csv(
    workers: List[Dict],
    route_map: Dict[int, Dict],
    client_addr: Dict[int, str],
    output_path: str = "plan_tehniki.csv"
):
    rows = []

    for worker in workers:
        vid = worker["vehicle_id"]
        route = route_map.get(vid)
        if not route:
            continue

        depot_name = worker["depot_name"]
        depot_address = worker["depot_address"]
        client_nodes = route["route"][1:-1]
        addresses = [client_addr.get(node, f"Узел-{node}") for node in client_nodes]
        addresses_str = "; ".join(addresses)

        rows.append({
            "Депо": depot_name,
            "Адрес_депо": depot_address,
            "Водитель": worker["worker_name"],
            "Телефон": worker["worker_phone"],
            "Техника": worker["tech_type"],
            "Грузоподъёмность_кг": worker["max_payload_kg"],
            "Загрузка_кг": f"{route['load_kg']} / {route['capacity_kg']}",
            "Пробег_м": route["distance_m"] * 100,
            "Адреса": addresses_str
        })

    rows.sort(key=lambda r: (r["Депо"], r["Водитель"]))

    if not rows:
        print("Нет активных маршрутов для экспорта.")
        return

    dir_path = os.path.dirname(output_path) or "."
    os.makedirs(dir_path, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        fieldnames = [
            "Депо", "Адрес_депо", "Водитель", "Телефон", "Техника",
            "Грузоподъёмность_кг", "Загрузка_кг", "Пробег_м", "Адреса"
        ]
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            delimiter=";",
            quoting=csv.QUOTE_MINIMAL,
            extrasaction='ignore'
        )

        writer.writeheader()
        writer.writerows(rows)

    abs_path = os.path.abspath(output_path)
    print(f"Экспорт завершён: {len(rows)} маршрутов → {abs_path}")
    return abs_path


