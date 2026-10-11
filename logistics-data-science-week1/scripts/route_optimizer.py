"""Synthetic capacitated vehicle routing with Euclidean map units, not road kilometers."""
import argparse
import math
from pathlib import Path
import pandas as pd
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def optimize(path, vehicle_capacity=11, vehicle_count=2):
    stops = pd.read_csv(path)
    expected = {'id', 'x', 'y', 'demand'}
    if not expected.issubset(stops.columns):
        raise ValueError(f'Expected columns: {sorted(expected)}')
    if stops.iloc[0]['id'] != 'DEPOT':
        raise ValueError('First stop must be DEPOT')
    if (stops['demand'] < 0).any() or sum(stops['demand']) > vehicle_capacity * vehicle_count:
        raise ValueError('Invalid demand or insufficient total fleet capacity')
    coords = list(zip(stops['x'].astype(float), stops['y'].astype(float)))
    distances = [[int(round(math.dist(a, b) * 1000)) for b in coords] for a in coords]
    manager = pywrapcp.RoutingIndexManager(len(stops), vehicle_count, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return distances[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_index)
    demand_values = stops['demand'].astype(int).tolist()

    def demand_callback(from_index):
        return demand_values[manager.IndexToNode(from_index)]

    demand_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(demand_index, 0, [vehicle_capacity] * vehicle_count, True, 'Capacity')
    search = pywrapcp.DefaultRoutingSearchParameters()
    search.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search.time_limit.seconds = 3
    solution = routing.SolveWithParameters(search)
    if not solution:
        print('No feasible route found with given capacities/settings')
        return
    total = 0
    for vehicle in range(vehicle_count):
        index = routing.Start(vehicle)
        route, load, length = [], 0, 0
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(str(stops.iloc[node]['id']))
            load += demand_values[node]
            nxt = solution.Value(routing.NextVar(index))
            length += routing.GetArcCostForVehicle(index, nxt, vehicle)
            index = nxt
        route.append('DEPOT')
        total += length
        print(f'Vehicle {vehicle+1}: {" -> ".join(route)} | load={load}/{vehicle_capacity} | distance={length/1000:.2f} planar units')
    print(f'Total distance: {total/1000:.2f} planar units (NOT kilometers)')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=str(Path(__file__).resolve().parents[1] / 'data' / 'synthetic_stops.csv'))
    args = parser.parse_args()
    optimize(args.input)


if __name__ == '__main__':
    main()
