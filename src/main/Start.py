import time
import Clarke_Wright_Andrea as Cw
import ParseInstances as Parse
import Clarke_Wright_Alessia as cwAle
import Sweep_Ale as sweepAle
import Plotter as pltt
from src.main import Utils
from src.main.Sweep_Andrea import solve_sweep_on_instance
import matplotlib.pyplot as plt

# Chiude tutte le figure aperte
plt.close('all')

path_instance = "resources/vrplib/Instances/P-n19-k2.vrp"
instance = Parse.make_instance_from_path_name(path_instance)
nodes, truck = Parse.work_on_instance(path_instance)

# Calcolo della matrice dei costi
dist = cwAle.get_distance(nodes)

CW_ALE = False
CW_ANDRE = False
SWEEP_ALE = True
SWEEP_ANDRE = False

# ALESSIA CW
if CW_ALE:
    # Registra il tempo di inizio
    start_time = time.time()
    # Chiamata alla funzione che vuoi misurare
    roots_cw_ale = cwAle.start(nodes, truck)
    # Registra il tempo di fine
    end_time = time.time()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione cwAle: {execution_time} secondi")

    pltt.plot_roots_graph(nodes, roots_cw_ale)
    cost_cw_ale = Utils.calculateCost(roots_cw_ale, dist)
    print(f"Costi CW ALESSIA {cost_cw_ale}")

# ANDREA CW
if CW_ANDRE:
    # Registra il tempo di inizio
    start_time = time.time()
    # Chiamata alla funzione che vuoi misurare
    cw_cost, roots_cw_andre = Cw.solve_clarke_and_wright(path_instance)
    # Registra il tempo di fine
    end_time = time.time()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione cwAndre: {execution_time} secondi")

    pltt.plot_roots_graph(nodes, roots_cw_andre)
    cost_cw_andre = Utils.calculateCost(roots_cw_andre, dist)
    print(f"Costi CW ANDREA {cost_cw_andre}")

# SWEEP ALESSIA
if SWEEP_ALE:
    # Registra il tempo di inizio
    start_time = time.time()
    # Chiamata alla funzione che vuoi misurare
    roots_sweep_ale = sweepAle.sweep_algorithm(nodes, truck.get_capacity())
    # Registra il tempo di fine
    end_time = time.time()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione sweep Ale: {execution_time} secondi")

    pltt.plot_roots_graph(nodes, roots_sweep_ale)
    cost_sweep_ale = Utils.calculateCost(roots_sweep_ale, dist)
    print(f"Costi SWEEP ALESSIA {cost_sweep_ale}")

# SWEEP ANDREA
if SWEEP_ANDRE:
    # Registra il tempo di inizio
    start_time = time.time()
    # Chiamata alla funzione che vuoi misurare
    roots_sweep_andre, _ = solve_sweep_on_instance(path_instance)
    # Registra il tempo di fine
    end_time = time.time()
    # Calcola la durata dell'esecuzione
    execution_time = end_time - start_time
    print(f"Tempo di esecuzione sweep Andrea: {execution_time} secondi")

    pltt.plot_roots_graph(nodes, roots_sweep_andre)
    cost_sweep_andre = Utils.calculateCost(roots_sweep_andre, dist)
    print(f"Costi SWEEP ANDREA {cost_sweep_andre}")

