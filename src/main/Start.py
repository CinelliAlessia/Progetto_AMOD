import time
import Clarke_Wright_Andrea as Cw
import ParseInstances as Parse
import Clarke_Wright_Alessia as cwAle
from src.main.Plotter import plot_roots_graph

path_instance = "resources/vrplib/Instances/F-n135-k7.vrp"
instance = Parse.make_instance_from_path_name(path_instance)

nodes, truck = Parse.work_on_instance(path_instance)

# Registra il tempo di inizio
start_time = time.time()

# Chiamata alla funzione che vuoi misurare
roots_cw, cost_cw = cwAle.start(nodes, truck)
# Registra il tempo di fine
end_time = time.time()

# Calcola la durata dell'esecuzione
execution_time = end_time - start_time

print(f"Tempo di esecuzione: {execution_time} secondi")

#ANDREA

# Registra il tempo di inizio
start_time = time.time()
# Chiamata alla funzione che vuoi misurare
cw_cost, _ = Cw.solve_clarke_and_wright(path_instance)
# Registra il tempo di fine
end_time = time.time()

# Calcola la durata dell'esecuzione
execution_time = end_time - start_time
print(f"Tempo di esecuzione: {execution_time} secondi")

# Plot the figure
plot_roots_graph(nodes, roots_cw)

# Calcolo della matrice dei costi
costo = cwAle.get_distance(nodes)

#solveVrp = solve_vrp(nodes, truck, costo)
#print(f"Solve VRP: {solveVrp} - Cost_CW: {cost_cw}")
