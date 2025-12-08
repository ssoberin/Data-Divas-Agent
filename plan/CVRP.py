from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from typing import List, Dict

'''здесь мат модель для решения задачи маршрутов транспортов с учетом грузоподъемности 
отталкиваемся от кг и объема, считаем в итоге через кг, но находим минимум из реального веса и веса полученного из
объема умноженного на плотность
подробнее см документацию'''

def solve_mdvrp(
        c_ij: List[List[int]],
        d_i: List[int],
        vehicle_to_depot: List[int],
        Q_k: List[int],
        time_limit_sec: int = 30
) -> Dict:
    N = len(d_i)
    K = len(Q_k)
    assert len(vehicle_to_depot) == K

    d_i = [int(round(x)) for x in d_i]
    Q_k = [int(round(x)) for x in Q_k]
    c_ij = [[int(round(cell)) for cell in row] for row in c_ij]

    starts = vehicle_to_depot
    ends = vehicle_to_depot

    manager = pywrapcp.RoutingIndexManager(
        N,
        K,
        starts,
        ends
    )
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        i = manager.IndexToNode(from_index)
        j = manager.IndexToNode(to_index)
        return c_ij[i][j]

    transit_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    def demand_callback(from_index):
        i = manager.IndexToNode(from_index)
        return d_i[i]

    demand_idx = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_idx,
        0,
        Q_k,
        True,
        "Capacity"
    )
    depot_nodes = set(vehicle_to_depot)
    for depot_node in depot_nodes:
        try:
            index = manager.NodeToIndex(depot_node)
            allowed_vehicles = [
                k for k, d in enumerate(vehicle_to_depot) if d == depot_node
            ]
            routing.SetAllowedVehiclesForIndex(allowed_vehicles, index)
        except Exception:
            pass

    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.seconds = time_limit_sec
    search_params.log_search = False

    solution = routing.SolveWithParameters(search_params)

    result = {"status": "NO_SOLUTION", "total_distance": 0, "routes": []}
    if not solution:
        return result

    status_map = {
        0: "ROUTING_NOT_SOLVED",
        1: "FEASIBLE",
        2: "INFEASIBLE",
        3: "TIME_LIMIT",
        4: "INVALID",
        5: "INFEASIBLE",
    }
    result["status"] = status_map.get(routing.status(), f"UNKNOWN({routing.status()})")

    total_distance = 0
    for k in range(K):
        route = []
        index = routing.Start(k)
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            index = solution.Value(routing.NextVar(index))
        end_node = manager.IndexToNode(index)
        route.append(end_node)

        if len(route) <= 2:
            continue

        distance_k = sum(
            c_ij[route[t]][route[t + 1]] for t in range(len(route) - 1)
        )
        load_k = sum(d_i[i] for i in route[1:-1])

        result["routes"].append({
            "vehicle_id": k,
            "depot": vehicle_to_depot[k],
            "capacity_kg": Q_k[k],
            "route": route,
            "load_kg": load_k,
            "distance_m": distance_k
        })
        total_distance += distance_k

    result["total_distance"] = total_distance
    return result



