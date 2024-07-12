import os
import time
import Clarke_Wright_Alessia as cwAle
import Clarke_Wright_Andrea as Cw
import ParseInstances as Parse
import Plotter as plotter
import Sweep_Ale as sweepAle
from src.main import Utils
from src.main.Random_Ale import vrp_random_1, vrp_random_2
from src.main.Sweep_Andrea import solve_sweep_on_instance


def print_roots(roots):
    for r in roots:
        print(r)


CW_ALE = False
CW_ANDRE = False
SWEEP_ALE = False
SWEEP_ANDRE = False
RANDOM = False

path_instance = "../resources/vrplib/Instances/E-n13-k4.vrp"
instance = Parse.make_instance_from_path_name(path_instance)
nodes, truck = Parse.work_on_instance(instance, False)

if nodes is None:
    # Non continuare l'esecuzione
    exit(1)

print("FINE PARSING")

# ALESSIA CW
if CW_ALE:
    # Registra il tempo di inizio
    start_time = time.time()
    # Chiamata alla funzione che vuoi misurare
    roots = cwAle.start(nodes, truck)
    # Registra il tempo di fine
    end_time = time.time()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione cwAle: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, roots)
    cost = Utils.calculate_cost(roots, nodes)
    print_roots(roots)
    print(f"Costi CW ALESSIA {cost}")

# ANDREA CW
if CW_ANDRE:
    # Registra il tempo di inizio
    start_time = time.time()
    # Chiamata alla funzione che vuoi misurare
    _, roots = Cw.solve_clarke_and_wright_on_instance(instance)
    # Registra il tempo di fine
    end_time = time.time()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione cwAndre: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, roots)
    cost = Utils.calculate_cost(roots, nodes)
    print_roots(roots)
    print(f"Costi CW ANDREA {cost}")

# SWEEP ALESSIA
if SWEEP_ALE:
    # Registra il tempo di inizio
    start_time = time.perf_counter()
    # Chiamata alla funzione che vuoi misurare
    roots_1, roots_2, roots_3 = sweepAle.sweep_algorithm(nodes, truck.get_capacity())

    # Registra il tempo di fine
    end_time = time.perf_counter()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione sweep Ale: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, roots_2)
    cost_2 = Utils.calculate_cost(roots_2, nodes)
    print_roots(roots_2)
    print(f"Costi SWEEP ALESSIA opt2: {cost_2}")

    plotter.plot_roots_graph(nodes, roots_3)
    cost_3 = Utils.calculate_cost(roots_3, nodes)
    print_roots(roots_3)
    print(f"Costi SWEEP ALESSIA opt3: {cost_3}")

# SWEEP ANDREA
if SWEEP_ANDRE:
    # Registra il tempo di inizio
    start_time = time.perf_counter()
    # Chiamata alla funzione che vuoi misurare
    roots, _ = solve_sweep_on_instance(instance, True, False)
    # Registra il tempo di fine
    end_time = time.perf_counter()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione sweep Andrea: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, roots)
    cost = Utils.calculate_cost(roots, nodes)
    print_roots(roots)
    print(f"Costi SWEEP ANDREA {cost}")

if RANDOM:

    best_cost = float("inf")
    best_root = []

    # Registra il tempo di inizio
    start_time = time.perf_counter()
    for i in range(1000):
        roots = vrp_random_1(nodes, truck.get_capacity())
        cost = Utils.calculate_cost(roots, nodes)
        if cost < best_cost:
            best_cost = cost
            best_root = roots  # Registra il tempo di fine
    end_time = time.perf_counter()

    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione random 1: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, best_root)
    print_roots(best_root)
    print(f"Costi random_1 {best_cost}")

    best_cost = float("inf")
    best_root = []

    # Registra il tempo di inizio
    start_time = time.perf_counter()
    for i in range(1000):
        roots = vrp_random_2(nodes, truck.get_capacity())
        cost = Utils.calculate_cost(roots, nodes)
        if cost < best_cost:
            best_cost = cost
            best_root = roots  # Registra il tempo di fine
    end_time = time.perf_counter()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione random 2: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, best_root)
    print_roots(best_root)
    print(f"Costi random_2 {best_cost}")