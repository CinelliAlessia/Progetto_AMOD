import time
import Clarke_Wright_Alessia as cwAle
import Clarke_Wright_Andrea as Cw
import ParseInstances as Parse
import Plotter
import Sweep_Ale as sweepAle
import Utils
from Preliminar_Study_of_Instances import read_sol_file
from Random_Ale import vrp_random
from Sweep_Andrea import solve_sweep_on_instance


def print_routes(routes):
    if len(all_nodes) < 50:
        for c in routes:
            print(c)


CW_ALE = False
CW_ANDRE = False
SWEEP_ALE = True
SWEEP_ANDRE = False
RANDOM = False
RANDOM_ITERATION_NUMBER = 750

if CW_ALE or CW_ANDRE or RANDOM:
    work_on_explicit = True
else:
    work_on_explicit = False


path_instance = "../resources/vrplib/Instances/CMT8.vrp"
instance = Parse.make_instance_from_path_name(path_instance)
all_nodes, truck = Parse.work_on_instance(instance, work_on_explicit)
print("Fine Parsing")


def start():
    if all_nodes is None:
        return None

    # ALESSIA CW
    if CW_ALE:
        # Registra il tempo di inizio
        start_time = time.time()
        # Chiamata alla funzione che vuoi misurare
        routes = cwAle.start(all_nodes, truck)
        # Registra il tempo di fine
        end_time = time.time()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione cwAle: {execution_time} secondi")

        Plotter.plot_if_not_explicit(routes, all_nodes)
        cost = Utils.calculate_cost(routes, all_nodes)
        print_routes(routes)
        print(f"Costi CW ALESSIA {cost}")

    # ANDREA CW
    if CW_ANDRE:
        # Registra il tempo di inizio
        start_time = time.time()
        # Chiamata alla funzione che vuoi misurare
        routes, _, _ = Cw.solve_clarke_and_wright_on_instance(instance)
        # Registra il tempo di fine
        end_time = time.time()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione cwAndre: {execution_time} secondi")
        print("Plotting...")
        Plotter.plot_if_not_explicit(routes, all_nodes)
        print("Calcolo costo...")
        cost = Utils.calculate_cost(routes, all_nodes)
        print_routes(routes)
        print(f"Costi CW ANDREA {cost}")

    # SWEEP ALESSIA
    if SWEEP_ALE:
        truck_capacity = truck.get_capacity()

        # Registra il tempo di inizio
        start_time = time.perf_counter()
        # Chiamata alla funzione che vuoi misurare

        routes, costs = sweepAle.sweep_algorithm(all_nodes, truck_capacity, False, True)

        # Registra il tempo di fine
        end_time = time.perf_counter()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione sweep Ale: {execution_time} secondi")

        Plotter.plot_if_not_explicit(routes, all_nodes)
        print("Routes opt3:")
        print_routes(routes)
        print(f"Costi SWEEP ALESSIA: {costs}")

    # SWEEP ANDREA
    if SWEEP_ANDRE:
        # Registra il tempo di inizio
        start_time = time.perf_counter()
        # Chiamata alla funzione che vuoi misurare
        routes, _ = solve_sweep_on_instance(instance, True, False)
        # Registra il tempo di fine
        end_time = time.perf_counter()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione sweep Andrea: {execution_time} secondi")

        Plotter.plot_if_not_explicit(routes, all_nodes)

        cost = Utils.calculate_cost(routes, all_nodes)
        print("Routes:")
        print_routes(routes)
        print(f"Costi SWEEP ANDREA {cost}")

    if RANDOM:
        total_demand = Utils.total_demands(all_nodes)
        id_depots = Parse.get_depots_index(instance)[0]

        best_cost = float("inf")
        best_routes = []

        # Registra il tempo di inizio
        start_time = time.perf_counter()
        for i in range(RANDOM_ITERATION_NUMBER):
            routes, costs = vrp_random(all_nodes, truck.get_capacity(), total_demand, id_depots)
            if costs < best_cost:
                best_cost = costs
                best_routes = routes  # Registra il tempo di fine
        end_time = time.perf_counter()

        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time

        print_routes(best_routes)
        Plotter.plot_if_not_explicit(best_routes, all_nodes)

        print(f"Costi random: {best_cost}")
        print(f"Tempo di esecuzione random: {execution_time} secondi")


start()

sol_path = "../resources/vrplib/Solutions/CMT8.sol"
route, cost = read_sol_file(sol_path)
Plotter.plot_if_not_explicit(route, all_nodes)
print("Route from sol file;")
print_routes(route)
print(f"Cost from sol file: {cost}")
