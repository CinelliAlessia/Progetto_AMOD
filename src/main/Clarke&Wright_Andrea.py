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

# Semplice somma delle domande sulla route e verifica se il nuovo nodo può essere aggiunto
def verify_if_route_feasible(truck_capacity, route, demand):
    route_demand = 0
    for node in route:
        route_demand += demand  # Calcolo domanda attuale sul cammino
    if route_demand + demand > truck_capacity:  # Verifico se posso aggiungere il nuovo nodo
        return False
    return True


# Implementazione Euristica di Clarke e Wright
def clarke_and_wright(path):
    # --------------- Dati del problema ---------------
    instance = parser.make_instance_from_path_name(path)  # todo controllo se funziona
    demands = parser.get_node_demands(instance)
    truck_capacity = parser.get_truck(instance).capacity
    edges = parser.get_edge_weight(instance)
    # -------------- Variabili da calcolare --------------
    routes = [] # Inizializzo le route come vuote
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
        i, j, value = s
        for route in routes:
            if route[-1] == i and j != depot_index:
                #  Se il nodo i è l'ultimo nodo di un percorso e j non è il deposito
                #  Prima di aggiungere devo verificare se la route è ammissibile
                #  Se la somma delle domande dei clienti è minore della capacità del veicolo
                #  allora la route è ammissibile
                if verify_if_route_feasible(truck_capacity, route, demands[j]):  # todo utilizzare un array con la domanda attuale sulla route, riduce i calcoli
                    route.append(j)  # Aggiungo j al percorso
                    print(f"Aggiunto {j} a {route}")
            elif route[0] == j and i != depot_index:
                #  Se il nodo j è il primo nodo di un percorso e i non è il deposito
                if verify_if_route_feasible(truck_capacity, route, demands[i]):
                    route.insert(0, i)  # Aggiungo i al percorso
                    print(f"Aggiunto {i} a {route}")



# -------------------------- Test -----------------------------
clarke_and_wright("resources/vrplib/Instances/P-n16-k8.vrp")
