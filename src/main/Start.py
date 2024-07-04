from src.main.Opt_solution import solve_vrp
from src.main import ParseInstances as Parse
from src.main import Clarke_Wright_Alessia as cwAle
from src.main.Plotter import plot_roots_graph

path_instance = "resources/vrplib/Instances/A-n32-k5.vrp"
instance = Parse.make_instance_from_path_name(path_instance)

nodes, truck = Parse.work_on_instance(path_instance)
roots_cw, cost_cw = cwAle.start(nodes, truck)

# Plot the figure
plot_roots_graph(nodes, roots_cw)

# Calcolo della matrice dei costi
costo = cwAle.get_distance(nodes)

#solveVrp = solve_vrp(nodes, truck, costo)
#print(f"Solve VRP: {solveVrp} - Cost_CW: {cost_cw}")
