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


path_instance = "resources/vrplib/Instances/A-n32-k5.vrp"
instance = Parse.make_instance_from_path_name(path_instance)
nodes, truck = Parse.work_on_instance(path_instance)
print("FINE PARSING")

CW_ALE = False
CW_ANDRE = False
SWEEP_ALE = False
SWEEP_ANDRE = False
RANDOM = True

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
    _ , roots = Cw.solve_clarke_and_wright(path_instance)
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
    roots = sweepAle.sweep_algorithm(nodes, truck.get_capacity())

    # Registra il tempo di fine
    end_time = time.perf_counter()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione sweep Ale: {execution_time} secondi")

    plotter.plot_roots_graph(nodes, roots)
    cost = Utils.calculate_cost(roots, nodes)
    print_roots(roots)
    print(f"Costi SWEEP ALESSIA {cost}")

# SWEEP ANDREA
if SWEEP_ANDRE:
    # Registra il tempo di inizio
    start_time = time.perf_counter()
    # Chiamata alla funzione che vuoi misurare
    roots, _ = solve_sweep_on_instance(path_instance, True, False)
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
    print("RANDOM 1")
    for i in range(1000):
        roots = vrp_random_1(nodes, truck.get_capacity())
        cost = Utils.calculate_cost(roots, nodes)
        if cost < best_cost:
            best_cost = cost
            best_root = roots

    plotter.plot_roots_graph(nodes, best_root)
    print_roots(best_root)
    print(f"Costi random_1 {best_cost}")

    print("RANDOM 2")
    best_cost = float("inf")
    best_root = []
    for i in range(1000):
        roots = vrp_random_2(nodes, truck.get_capacity())
        cost = Utils.calculate_cost(roots, nodes)
        if cost < best_cost:
            best_cost = cost
            best_root = roots

    plotter.plot_roots_graph(nodes, best_root)
    print_roots(best_root)
    print(f"Costi random_2 {best_cost}")
