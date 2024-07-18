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
        #print(f"Route #{index + 1}: {route_str} |total demand: {total_demand} |route cost: "
        #      f"{route_cost}")
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



# TEST


def read_sol_file(filepath):
    routes = []

    with open(filepath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('Route #'):
                route_str = line.strip().split(': ')[1]
                nodes = list(map(int, route_str.split()))
                formatted_route = [0] + nodes + [0]
                routes.append(formatted_route)
            elif line.startswith('Cost'):
                cost = int(line.split()[1].strip())

    return routes, cost


def fix_cost(directory):
    # Controlla che la directory esista
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' non trovata.")
        return

    # Ottieni la lista dei file .sol nella directory
    sol_files = [f for f in os.listdir(directory) if f.endswith('.sol')]

    for sol_file in sol_files:
        filepath = os.path.join(directory, sol_file)
        print(f"Modifica del file: {filepath}")

        # Leggi le routes e il costo dal file .sol
        routes, file_cost = read_sol_file(filepath)

        name_file = sol_file.split(".")[0]

        # Carica l'istanza dal file VRP
        instance_path = f'../resources/vrplib/Instances/{name_file}.vrp'
        instance = Parser.make_instance_from_path_name(instance_path)

        # Ottieni i pesi degli archi e le richieste dei nodi
        weights = Parser.get_edge_weight(instance)
        demands = Parser.get_node_demands(instance)

        # Calcola il costo totale delle routes
        calculated_cost = calculate_routes_cost(routes, weights, demands)
        print(f"Costo calcolato dalle routes: {calculated_cost}")
        print(f"Costo indicato nel file .sol: {file_cost}")

        # Confronto tra costo calcolato e costo dal file .sol
        if calculated_cost == file_cost:
            print("I costi coincidono.")
        else:
            modify_optimal_value_vrp(instance_path, calculated_cost)
            print("Attenzione: i costi non coincidono.")

        print()  # Linea vuota per separare le stampe dei vari file


def modify_optimal_value_vrp(filepath, new_optimal_value):
    # Leggi tutte le linee dal file VRP
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Trova e modifica l'optimal value
    for i, line in enumerate(lines):
        if line.startswith('COMMENT'):
            parts = line.split(':')
            parts[-1] = f' Optimal value: {new_optimal_value})\n'
            lines[i] = ':'.join(parts)
            break

    # Sovrascrivi il file VRP con l'optimal value modificato
    with open(filepath, 'w') as file:
        file.writelines(lines)


import os

def add_optimal_value_to_vrp(filepath, optimal_value):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    comment_found = False
    for i, line in enumerate(lines):
        if line.startswith('COMMENT'):
            lines[i] = line.strip() + f', Optimal value: {optimal_value})\n'
            comment_found = True
            break

    if not comment_found:
        for i, line in enumerate(lines):
            if line.startswith('TYPE'):
                lines.insert(i, f'COMMENT : Optimal value: {optimal_value}\n')
                break

    with open(filepath, 'w') as file:
        file.writelines(lines)

def add_optimal_value_to_all_vrps_in_directory(directory, optimal_value):
    if not os.path.isdir(directory):
        print(f"Directory '{directory}' non trovata.")
        return

    vrp_files = [f for f in os.listdir(directory) if f.endswith('.vrp')]

    for vrp_file in vrp_files:
        filepath = os.path.join(directory, vrp_file)
        print(f"Modifica del file: {filepath}")
        add_optimal_value_to_vrp(filepath, optimal_value)
        print(f"Valore ottimale aggiunto: {optimal_value}")


# Esempio di utilizzo per la directory specificata
directory_path = "../resources/vrplib/Solutions"
fix_cost(directory_path)





