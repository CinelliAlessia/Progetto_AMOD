import ParseInstances as Parser
import Utils
from Clarke_Wright_Andrea import solve_clarke_and_wright_on_instance
from Preliminar_Study_of_Instances import read_sol_file
from Start import print_roots
from Sweep_Ale import sweep_algorithm

CW = False
SWEEP = True
RANDOM = False
RANDOM_ITERATION_NUMBER = 750

if CW or RANDOM:
    work_on_explicit = True
else:
    work_on_explicit = False


path_instance = "../resources/vrplib/Instances/E-n31-k7.vrp"
path_sol = "../resources/vrplib/Solutions/E-n31-k7.sol"

instance = Parser.make_instance_from_path_name(path_instance)
all_nodes, truck = Parser.work_on_instance(instance, work_on_explicit)
truck_capacity = truck.get_capacity()
weights = Parser.get_edge_weight(instance)
demands = Parser.get_node_demands(instance)

routes, _ = read_sol_file(path_sol)
print("Root sol:", routes)
Utils.calculate_routes_cost(routes, weights, demands)

print("Fine Parsing")


if CW:
    routes, _, _ = solve_clarke_and_wright_on_instance(instance)
    print_roots(routes)
    cost = Utils.calculate_cost(routes, all_nodes)
    print_roots(routes)
    print(f"Costi CW ANDREA {cost}")

if SWEEP:

    # Chiamata alla funzione che vuoi misurare
    routes, costs = sweep_algorithm(all_nodes, truck_capacity, False, True)
    print_roots(routes)
    print(f"Costo: {Utils.calculate_cost(routes, all_nodes)}")
    print(f"Costi SWEEP ALESSIA: {costs}")


Utils.calculate_routes_cost(routes, weights, demands)
