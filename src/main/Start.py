import time
import Clarke_Wright_Andrea as Cw
import ParseInstances as Parse
import Clarke_Wright_Alessia as cwAle
import Sweep_Ale as sweepAle
from src.main.Plotter import plot_roots_graph

path_instance = "resources/vrplib/Instances/P-n16-k8.vrp"
instance = Parse.make_instance_from_path_name(path_instance)
nodes, truck = Parse.work_on_instance(path_instance)

# Calcolo della matrice dei costi
dist = cwAle.get_distance(nodes)


def calculateCost(roots):
    total_cost = []

    for r in roots:
        cost = 0
        for i in range(len(r)-1):
            cost += dist[r[i]][r[i + 1]]

        print(f"Route: {r} - Cost: {cost}")
        total_cost.append(cost)

    #print(f"Total cost: {sum(total_cost)}")
    return sum(total_cost)


# ALESSIA CW

# Registra il tempo di inizio
start_time = time.time()
# Chiamata alla funzione che vuoi misurare
roots_cw_ale, cost_cw = cwAle.start(nodes, truck)
# Registra il tempo di fine
end_time = time.time()
# Calcola la durata dell'esecuzione
execution_time = end_time - start_time
print(f"Tempo di esecuzione: {execution_time} secondi")

# ANDREA CW

# Registra il tempo di inizio
start_time = time.time()
# Chiamata alla funzione che vuoi misurare
cw_cost, roots_cw_andre = Cw.solve_clarke_and_wright(path_instance)
# Registra il tempo di fine
end_time = time.time()
# Calcola la durata dell'esecuzione
execution_time = end_time - start_time
print(f"Tempo di esecuzione: {execution_time} secondi")


# Plot the figure
plot_roots_graph(nodes, roots_cw_ale)

# Sweep ALESSIA
roots_sweep_ale = sweepAle.sweep_algorithm(nodes, truck.get_capacity())
for i, cluster in enumerate(roots_sweep_ale):
    print(cluster)

plot_roots_graph(nodes, roots_sweep_ale)


# Calcolo dei costi
cost_cw_ale = calculateCost(roots_cw_ale)
print(f"Costi CW ALESSIA {cost_cw_ale}")
cost_cw_andre = calculateCost(roots_cw_andre)
print(f"Costi CW ANDREA {cost_cw_andre}")
cost_sweep_ale = calculateCost(roots_sweep_ale)
print(f"Costi SWEEP ALESSIA {cost_sweep_ale}")
