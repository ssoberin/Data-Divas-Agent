import time

from vivaldi import (
    matriza_ras, demand_snega_mdvrp, obyom_mashiny,
    build_vehicle_to_depot, get_worker_info, get_client_addresses
)
from CVRP import solve_mdvrp
from WeatherAPI import start_or_no, get_height
from get_snow_points import collect_snow_points
from to_csv import export_plan_to_csv


ADDRESSES = [
        "Улица Восход, 16",
        "Улица Шамиля Усманова, 10",
        "Проспект Победы, 100",
        "Улица Баумана, 55",
        "Улица Ленина, 1"
    ]


def main():
    if start_or_no() == False:
        print("Cегодня уборка снега не требуется. Высота снега меньше 5")
    else:
        print(f"Высота снега: {get_height()}. Начинаем планирование уборки.")
        collect_snow_points(ADDRESSES)
        print("Загрузка данных...")
        c_ij = matriza_ras()
        d_i = demand_snega_mdvrp()
        Q_k = obyom_mashiny()
        vehicle_to_depot = build_vehicle_to_depot()
        workers = get_worker_info()
        client_addr = get_client_addresses()

        print(f"Загружено: {len(workers)} водителей, {len(client_addr)} точек снега")

        print("Решение MDVRP...")
        result = solve_mdvrp(
            c_ij=c_ij,
            d_i=d_i,
            vehicle_to_depot=vehicle_to_depot,
            Q_k=Q_k,
            time_limit_sec=30
        )

        print("ПЛАН ТЕХНИКИ — НАЗНАЧЕНИЕ ВОДИТЕЛЕЙ")

        if result["status"] != "FEASIBLE":
            print(f"Статус: {result['status']}. Решение не найдено.")
            return

        route_map = {r["vehicle_id"]: r for r in result["routes"]}

        for worker in workers:
            vid = worker["vehicle_id"]
            route = route_map.get(vid)
            if not route:
                print(f"{worker['worker_name']} ({worker['tech_type']}) — отдыхает")
                continue

            client_nodes = route["route"][1:-1]
            addresses = [client_addr.get(node, f"Узел-{node}") for node in client_nodes]

            print(f"\n{worker['worker_name']}")
            print(f"   {worker['worker_phone']}")
            print(f"   {worker['tech_type']} (грузоподъёмность: {worker['max_payload_kg']} кг)")
            print(f"   Депо: {worker['depot_name']}, {worker['depot_address']}")
            print(f"   Загрузка: {route['load_kg']} / {route['capacity_kg']} кг")
            print(f"   Маршрут:")
            for i, addr in enumerate(addresses, 1):
                print(f"      {i}. {addr}")
            print(f"   Общая дистанция: {route['distance_m'] * 100} м")

        export_plan_to_csv(
            workers=workers,
            route_map=route_map,
            client_addr=client_addr,
            output_path="output/plan_tehniki.csv"
        )

if __name__ == "__main__":
    main()