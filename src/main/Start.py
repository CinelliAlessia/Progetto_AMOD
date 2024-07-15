import time
import Clarke_Wright_Alessia as cwAle
import Clarke_Wright_Andrea as Cw
import ParseInstances as Parse
import Plotter
import Sweep_Ale as sweepAle
from src.main import Utils
from src.main.Random_Ale import vrp_random
from src.main.Sweep_Andrea import solve_sweep_on_instance


def print_roots(roots):
    if len(nodes) < 50:
        for c in roots:
            print(c)


CW_ALE = False
CW_ANDRE = False
SWEEP_ALE = False
SWEEP_ANDRE = False
RANDOM = False
RANDOM_ITERATION_NUMBER = 750

if CW_ALE or CW_ANDRE or RANDOM:
    work_on_explicit = True
else:
    work_on_explicit = False


path_instance = "../resources/vrplib/Instances/Antwerp1.vrp"
instance = Parse.make_instance_from_path_name(path_instance)
nodes, truck = Parse.work_on_instance(instance, work_on_explicit)


def start():
    if nodes is None:
        return None

    # ALESSIA CW
    if CW_ALE:
        # Registra il tempo di inizio
        start_time = time.time()
        # Chiamata alla funzione che vuoi misurare
        routes = cwAle.start(nodes, truck)
        # Registra il tempo di fine
        end_time = time.time()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione cwAle: {execution_time} secondi")

        Plotter.plot_if_not_explicit(routes, nodes)
        cost = Utils.calculate_cost(routes, nodes)
        print_roots(routes)
        print(f"Costi CW ALESSIA {cost}")

    # ANDREA CW
    if CW_ANDRE:
        # Registra il tempo di inizio
        start_time = time.time()
        # Chiamata alla funzione che vuoi misurare
        _, routes = Cw.solve_clarke_and_wright_on_instance(instance)
        # Registra il tempo di fine
        end_time = time.time()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione cwAndre: {execution_time} secondi")

        Plotter.plot_if_not_explicit(routes, nodes)

        cost = Utils.calculate_cost(routes, nodes)
        print_roots(routes)
        print(f"Costi CW ANDREA {cost}")

    # SWEEP ALESSIA
    if SWEEP_ALE:
        truck_capacity = truck.get_capacity()

        # Registra il tempo di inizio
        start_time = time.perf_counter()
        # Chiamata alla funzione che vuoi misurare
        routes, costs = sweepAle.sweep_algorithm(nodes, truck_capacity)

        # Registra il tempo di fine
        end_time = time.perf_counter()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time
        print(f"Tempo di esecuzione sweep Ale: {execution_time} secondi")

        Plotter.plot_if_not_explicit(routes, nodes)
        print_roots(routes)
        print(f"Costo: {Utils.calculate_cost(routes, nodes)}")

        print(f"Costi SWEEP ALESSIA opt2: {costs}")

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

        Plotter.plot_if_not_explicit(routes, nodes)

        cost = Utils.calculate_cost(routes, nodes)
        print_roots(routes)
        print(f"Costi SWEEP ANDREA {cost}")

    if RANDOM:
        total_demand = Utils.total_demands(nodes)
        id_depots = Parse.get_depots_index(instance)[0]

        best_cost = float("inf")
        best_root = []

        # Registra il tempo di inizio
        start_time = time.perf_counter()
        for i in range(RANDOM_ITERATION_NUMBER):
            routes = vrp_random(nodes, truck.get_capacity(), total_demand, id_depots)
            cost = Utils.calculate_cost(routes, nodes)
            if cost < best_cost:
                best_cost = cost
                best_root = routes  # Registra il tempo di fine
        end_time = time.perf_counter()

        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time

        print_roots(best_root)
        Plotter.plot_if_not_explicit(best_root, nodes)

        print(f"Costi random: {best_cost}")
        print(f"Tempo di esecuzione random: {execution_time} secondi")


start()
