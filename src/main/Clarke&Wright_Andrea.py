"""
Algoritmo Euristico di Clarke e Wright (1964) per il problema del Vehicle Routing Problem (VRP).
Utilizzato quando il numero di veicoli non è fissato a priori.

Passaggio 1. Calcola i risparmi ${s_{ij}=c_{i0}+c_{0j}-c_{ij}}$ per ${i, j=1,…, n}$ e ${i \neq j}$.
Crea ${n}$ percorsi di veicoli ${(0,i,0)}$ per ${i=1,…, n}$. Ordina i risparmi in modo non crescente.

Passaggio 2. Partendo dall'alto della lista dei risparmi, esegui quanto segue:
Dato un risparmio ${s_{ij}}$, determina se esistono due percorsi che possono essere fusi in modo ammissibile:
Quando due percorsi ${(0,…, i,0)}$ e ${(0,j, …,0)}$
possono essere fusi in modo ammissibile in un unico percorso: ${(0,…, i, j, …,0)}$,
si genera un risparmio (saves), definito nel passo 1.
Uno che inizia con ${(0,j)}$ Uno che termina con ${(i,0)}$ Combina questi due percorsi eliminando ${(0,j)}$ e ${(i,0)}$
e introducendo ${(i, j)}$.
"""
import os

import vrplib
import ParseInstances as parser


# Utilizzando i metodi definiti in ParseInstances.py,
# calcola i risparmi per ogni coppia di nodi e li ordina in modo decrescente
def calculate_saves_and_sort_descent(instance):
    dist = parser.get_edge_weight(instance)
    depots = parser.get_depots_index(instance)
    depotIndex = depots[0]  # !!!!! Assunto inizialmente un solo deposito, per semplicità di ragionamento
    n = parser.get_nodes_dimension(instance)
    saves = []
    for i in range(1, n):
        for j in range(i + 1, n):
            # formato save: (nodo, nodo, valore)
            saves.append((i, j, dist[depotIndex][i] + dist[j][depotIndex] - dist[i][j]))
    saves.sort(key=lambda x: x[2], reverse=True)
    return saves


def merge_routes_if_possible(routes, i, j, demands, truck_capacity, edges):
    route_i = None
    route_j = None
    for route in routes:
        if route[-2] == i:  # Il penultimo nodo, perché l'ultimo è il deposito
            route_i = route
        elif route[1] == j:  # Il secondo nodo, perché il primo è il deposito
            route_j = route
    if route_i and route_j and route_i != route_j:
        # Calcola la domanda totale per il percorso unito
        total_demand = sum(demands[node] for node in route_i[1:-1] + route_j[1:-1])
        if total_demand <= truck_capacity:
            # Unisci i percorsi
            new_route = route_i[:-1] + route_j[1:]
            routes.remove(route_i)
            routes.remove(route_j)
            routes.append(new_route)
            return True
    return False


def save_results_to_file(routes, cw_cost, path):
    # Estrai il nome dell'istanza dal percorso
    instance_name = os.path.basename(path).split('/')[0]
    output_directory = "resources/Heuristic_Solutions/CW_Solutions"
    output_path = os.path.join(output_directory, f"{instance_name}.sol")

    # Assicurati che la directory di output esista
    os.makedirs(output_directory, exist_ok=True)

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


# Implementazione Euristica di Clarke e Wright
def clarke_and_wright(path):
    # --------------- Dati del problema ---------------
    instance = parser.make_instance_from_path_name(path)  # todo controllo se funziona
    demands = parser.get_node_demands(instance)
    truck_capacity = parser.get_truck(instance).capacity
    edges = parser.get_edge_weight(instance)
    # -------------- Variabili da calcolare --------------
    routes = []  # Inizializzo le route come vuote
    cw_cost = 0
    # -----------------------------------------------------------------------------------
    # Passo 0: Devo definire un cammino per ogni cliente: (depotIndex, i, depotIndex)
    n = parser.get_nodes_dimension(instance)

    depots = parser.get_depots_index(instance)
    depot_index = depots[0]  # !!!!! Assunto inizialmente un solo deposito, per semplicità di ragionamento

    for i in range(1, n):
        routes.append([depot_index, i, depot_index])
        cw_cost += edges[depot_index][i] + edges[i][depot_index]
    print(f"Routes: {routes}")
    print(f"Initial Cost: {cw_cost}")
    # -----------------------------------------------------------------------------------
    # Passo 1: Calcolo saves per ogni coppia di nodi e li ordino in modo decrescente
    saves = calculate_saves_and_sort_descent(instance)
    print("Saves:")
    for s in saves:
        print(s)
    # -----------------------------------------------------------------------------------
    # Passo 2: Unisco le route in modo ammissibile
    for s in saves:
        i, j, _ = s
        if merge_routes_if_possible(routes, i, j, demands, truck_capacity, edges):
            print(f"Routes merged: {i} and {j}")
            cw_cost -= s[2]
            print(f"Updated Cost: {cw_cost}")
    # -----------------------------------------------------------------------------------
    # Passo 3: salva il risultato in un file .sol e stampa i risultati
    save_results_to_file(routes, cw_cost, path)
    # Stampa i risultati
    for index, route in enumerate(routes):
        route_str = " ".join(str(node) for node in route[1:-1])  # Escludi l'ID del deposito
        print(f"Route #{index + 1}: {route_str}")
    print(f"Cost {cw_cost}")


# -------------------------- Test -----------------------------
clarke_and_wright("resources/vrplib/Instances/P-n16-k8.vrp")
