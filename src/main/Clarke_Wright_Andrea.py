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
import ParseInstances as Parser

VERBOSE = False  # Se True, stampa valori delle istanze e i passaggi dell'euristica di Clarke e Wright
SAVE_sOLUTION_ON_FILE = True  # Se True, salva i risultati in un file .sol


# Utilizzando i metodi definiti in ParseInstances.py,
# calcola i risparmi per ogni coppia di nodi e li ordina in modo decrescente
def calculate_saves_and_sort_descent(instance):
    dist = Parser.get_edge_weight(instance)
    depots = Parser.get_depots_index(instance)
    depot_index = depots[0]  # todo !!!!! Assunto inizialmente un solo deposito, per semplicità di ragionamento
    n = Parser.get_nodes_dimension(instance)
    saves = []
    for i in range(0, n):
        for j in range(i + 1, n):
            # formato di un save: (nodo, nodo, valore)
            # deve essere calcolato solo se i e j non sono depositi
            if i not in depots or j not in depots:
                saves.append((i, j, dist[depot_index][i] + dist[j][depot_index] - dist[i][j]))
    saves.sort(key=lambda x: x[2], reverse=True)
    return saves


def merge_routes_if_possible(routes, i, j, demands, truck_capacity):
    route_i = None
    route_j = None
    # Trova i due percorsi che hanno i come ultimo e j come primo, o viceversa
    for route in routes:
        if route[-2] == i or route[1] == i:  # Il penultimo nodo, perché l'ultimo è il deposito
            route_i = route
        elif route[-2] == j or route[1] == j:  # Il penultimo nodo, perché l'ultimo è il deposito
            route_j = route

    if route_i and route_j and route_i != route_j:
        # Calcola la domanda totale per il percorso unito
        total_demand = sum(demands[node] for node in route_i[1:-1] + route_j[1:-1])
        if total_demand <= truck_capacity:
            # Unisci i percorsi, Devo differenziare i due casi:
            # 1. Se i è l'ultimo nodo di una route e j è il primo nodo di una route
            if route_i[-2] == i and route_j[1] == j:
                # prima route_i(tranne dep finale) e poi route_j(tranne dep iniziale)
                new_route = route_i[:-1] + route_j[1:]
            # 2. Se j è l'ultimo nodo di una route e i è il primo nodo di una route
            else:
                # prima route_j(tranne dep finale) e poi route_i(tranne dep iniziale)
                new_route = route_j[:-1] + route_i[1:]
            # Aggiorno la lista delle route
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
# input: path del file .vrp
# output: costo totale dei percorsi e lista di percorsi
def solve_clarke_and_wright(path):
    # --------------- Dati del problema ---------------
    instance = Parser.make_instance_from_path_name(path)  # todo controllo se funziona
    demands = Parser.get_node_demands(instance)  # Ci sono anche le domande del deposito
    truck_capacity = Parser.get_truck(instance).capacity
    edges = Parser.get_edge_weight(instance)  # Pesi degli archi
    depots = Parser.get_depots_index(instance)  # Indici dei depositi
    depot_index = depots[0]  # todo !!!Assunto inizialmente un solo deposito, per semplicità di ragionamento!!
    # -------------- Variabili da calcolare --------------
    routes = []  # Inizializzo le route come vuote (inizialmente ogni cliente ha un proprio veicolo, n route)
    cw_cost = 0  # Variabile che esprime il costo totale dei percorsi
    # -----------------------------------------------------------------------------------
    # Passo 0: Devo definire un cammino per ogni cliente: (depotIndex, i, depotIndex)
    n = Parser.get_nodes_dimension(instance)
    for i in range(0, n):
        if i not in depots:  # Se il cliente i non è un deposito
            routes.append([depot_index, i, depot_index])
            cw_cost += edges[depot_index][i] + edges[i][depot_index]
    if VERBOSE: print(f"First n Route: {routes} \nCost {cw_cost}")
    # -----------------------------------------------------------------------------------
    # Passo 1: Calcolo saves per ogni coppia di nodi e li ordino in modo decrescente
    saves = calculate_saves_and_sort_descent(instance)
    if VERBOSE:
        print("Saves Ordered:")
        for s in saves:
            print(s)
    # -----------------------------------------------------------------------------------
    # Passo 2: Unisco le route in modo ammissibile (Provo solo save positivi)
    for s in saves:
        i, j, save_value = s
        if save_value >= 0:
            if merge_routes_if_possible(routes, i, j, demands, truck_capacity):
                cw_cost -= save_value
                if VERBOSE:
                    print(f"Merged {i} and {j} in the same route with save {save_value}")
                    print(f"Updated Cost: {cw_cost}")
        # Se il save è negativo, non ha senso unire i percorsi
    # -----------------------------------------------------------------------------------
    # Passo 3: salva il risultato in un file .sol e stampa i risultati
    if SAVE_sOLUTION_ON_FILE: save_results_to_file(routes, cw_cost, path)
    # Stampa i risultati a schermo
    if VERBOSE:
        for index, route in enumerate(routes):
            route_str = " ".join(str(node) for node in route[1:-1])  # Escludi l'ID del deposito
            total_demand = sum(demands[node] for node in route[1:-1])  # Escludi il deposito
            print(
                f"Route #{index + 1}: {route_str} |total demand: {total_demand} |route cost: {sum(edges[route[i]][route[i + 1]] for i in range(len(route) - 1))}")
        print(f"Cost {cw_cost}")
    return cw_cost, routes

# -------------------------- Test -----------------------------
# solve_clarke_and_wright("resources/vrplib/Instances/A-n32-k5.vrp")
# solve_clarke_and_wright("resources/vrplib/Instances/CopilotInstance.vrp")
