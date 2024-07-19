import os

import ParseInstances as Parser


def save_results_to_file(routes, cw_cost, directory, instance_name):
    """
    Salva i risultati dell'euristica in un file di testo .sol
    :param routes: routes calcolate
    :param cw_cost: costo totale
    :param directory:
    :param instance_name: nome del file
    :return:
    """

    # Estrai il nome dell'istanza dal percorso
    output_path = os.path.join(directory, f"{instance_name}.sol")

    # Assicurati che la directory di output esista
    os.makedirs(directory, exist_ok=True)

    # Formatta l'output
    output_lines = []
    for index, route in enumerate(routes):
        route_str = " ".join(str(node) for node in route[1:-1])  # Escludi l'ID del deposito
        output_lines.append(f"Route #{index + 1}: {route_str}")
    output_lines.append(f"Cost {cw_cost}")

    # Scrivi l'output nel file
    with open(output_path, 'w') as file:
        file.write("\n".join(output_lines))

    print(f"Results saved to {output_path}")


def calculate_cost(roots, nodes):
    total_cost = []
    dist = get_distance(nodes)

    for r in roots:
        cost = 0
        for i in range(len(r)-1):
            cost += dist[r[i]][r[i + 1]]

        total_cost.append(cost)

    return sum(total_cost)


def calculate_cost_whit_matrix(roots, matrix):
    total_cost = []

    for r in roots:
        cost = 0
        for i in range(len(r)-1):
            cost += matrix[r[i]][r[i + 1]]

        total_cost.append(cost)

    return sum(total_cost)


def calculate_routes_cost(routes, weights, demands):
    total_cost, route_cost = 0, 0
    for index, route in enumerate(routes):
        route_cost = 0
        route_str = " ".join(str(node) for node in route[1:-1])  # Escludi l'ID del deposito
        total_demand = sum(demands[node] for node in route[1:-1])  # Escludi il deposito
        route_cost += sum(weights[route[i]][route[i + 1]] for i in range(len(route) - 1))
        #print(f"Route #{index + 1}: {route_str} |total demand: {total_demand} |route cost: " f"{route_cost}")
        total_cost += route_cost
    #print(f"CALCULATED COST:  {total_cost}")
    return total_cost


# Calcola la matrice delle distanze tra tutti i nodi, sarà sempre simmetrica poiché abbiamo istanze CVRP
def get_distance(nodes):
    # Determine the maximum ID value among all nodes
    max_id = max(node.get_id() for node in nodes)

    # Initialize the costo matrix with 0s, with dimensions [max_id + 1][max_id + 1]
    costo = [[0 for _ in range(max_id + 1)] for _ in range(max_id + 1)]

    for i, u in enumerate(nodes):
        for j in range(i + 1, len(nodes)):  # Start from i + 1 to avoid repetitions and self-comparisons
            v = nodes[j]
            # Calculate the cost and assign it to the symmetric values in the matrix
            costo[u.get_id()][v.get_id()] = u.get_distance(v.get_id())
            costo[v.get_id()][u.get_id()] = costo[u.get_id()][v.get_id()]

    return costo


def get_license():
    path = "../config.properties"
    with open(path, "r") as file:
        for line in file:
            if "license" in line:
                licence = line.split("=")[1].strip()
                return licence


def total_demands(nodes):
    return sum([node.get_demand() for node in nodes])


def verify_if_feasible(routes, truck_capacity, nodes):
    for route in routes:
        total_demand = sum(find_by_id(node, nodes).get_demand() for node in route[1:-1])  # Escludi il deposito
        if total_demand > truck_capacity:
            return False
    return True


def find_by_id(id, nodes):
    for node in nodes:
        if node.get_id() == id:
            return node


