from tornado import concurrent
import time
import ParseInstances as Parser
import Utils

EXECUTION_TIMEOUT = 300  # Tempo massimo di esecuzione in secondi
VERBOSE = False  # Se True, stampa valori delle istanze e i passaggi dell'euristica di Clarke e Wright
SAVE_SOLUTION_ON_FILE = False  # Se True, salva i risultati in un file .sol
RESULT_DIRECTORY = "Results/Heuristic_Solutions/CW_Solutions"  # Directory di output per i risultati

# ------------ Definisco le variabili globali che descrivono l'istanza specifica ------------------------
global weights, demands, depots, depot_index, truck_capacity, name  # Imposto variabili globali


# Utilizzando i metodi definiti in ParseInstances.py,
# calcola i risparmi per ogni coppia di nodi e li ordina in modo decrescente
def calculate_saves_and_sort_descent(instance):
    n = Parser.get_nodes_dimension(instance)
    saves = []
    for i in range(1, n):  # todo ho cambiato da 0 a 1
        for j in range(i + 1, n):
            # formato di un save: (nodo, nodo, valore)
            # deve essere calcolato solo se i e j non sono depositi
            if i not in depots or j not in depots:
                saves.append((i, j, weights[depot_index][i] + weights[j][depot_index] - weights[i][j]))
    saves.sort(key=lambda x: x[2], reverse=True)
    return saves


def merge_routes_if_possible(routes, i, j):
    route_i = None
    route_j = None
    # Trova i due percorsi che hanno i come ultimo e j come primo, o viceversa
    for route in routes:
        if route[-2] == i or route[1] == i:
            route_i = route
        elif route[-2] == j or route[1] == j:
            route_j = route

    if route_i and route_j and route_i != route_j:
        # Calcola la domanda totale per il percorso unito (route_i + route_j)
        total_demand = sum(demands[node] for node in route_i[:-1] + route_j[1:])
        if total_demand <= truck_capacity:
            # Unisci i percorsi, Devo differenziare i due casi:
            # 1. Se i è l'ultimo nodo di una route e j è il primo nodo di una route
            if route_i[-2] == i and route_j[1] == j:
                # prima route_i(tranne dep finale) e poi route_j(tranne dep iniziale)
                new_route = route_i[:-1] + route_j[1:]
            # 2. Se j è l'ultimo nodo di una route e i è il primo nodo di una route
            elif route_j[-2] == j and route_i[1] == i:
                # prima route_j(tranne dep finale) e poi route_i(tranne dep iniziale)
                new_route = route_j[:-1] + route_i[1:]
            else:
                return False
            # Aggiorno la lista delle route
            routes.remove(route_i)
            routes.remove(route_j)
            routes.append(new_route)
            return True
    return False


# Implementazione Euristica di Clarke e Wright
# input: path del file .vrp
# output: costo totale dei percorsi e lista di percorsi
def solve_clarke_and_wright_on_instance(instance):
    print("Solving: ", Parser.get_name(instance))
    # --------------- Inizializzo le variabili globali ---------------
    global demands, weights, depots, depot_index, truck_capacity, name
    demands = Parser.get_node_demands(instance)
    truck_capacity = Parser.get_truck(instance).capacity
    weights = Parser.get_edge_weight(instance)
    depots = Parser.get_depots_index(instance)
    depot_index = depots[0]  # todo !!!Assunto inizialmente un solo deposito, per semplicità di ragionamento!!!
    # -------------- Variabili da calcolare --------------
    routes = []  # Inizializzo le route come vuote (inizialmente ogni cliente ha un proprio veicolo, n route)
    cw_cost = 0  # Variabile che esprime il costo totale dei percorsi
    status = "Finished"
    # -----------------------------------------------------------------------------------
    # Passo 0: Devo definire un cammino per ogni cliente: (depotIndex, i, depotIndex)
    n = Parser.get_nodes_dimension(instance)
    for i in range(0, n):
        if i not in depots:  # Se il cliente i non è un deposito
            routes.append([depot_index, i, depot_index])
            cw_cost += weights[depot_index][i] + weights[i][depot_index]
    # ------------------------- Inizializzazione timer di esecuzione ----------------------------
    start_time = time.perf_counter()  # Almeno una soluzione anche se banale e pessima è definita
    # -----------------------------------------------------------------------------------
    # Passo 1: Calcolo saves per ogni coppia di nodi e li ordino in modo decrescente
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(calculate_saves_and_sort_descent, instance)
        try:
            saves = future.result(timeout=EXECUTION_TIMEOUT)
        except concurrent.futures.TimeoutError:
            print('Timeout scaduto durante il calcolo dei saves')
            status = "Timeout " + str(EXECUTION_TIMEOUT)
            saves = None
    if saves is None:
        Utils.save_results_to_file(routes, cw_cost, RESULT_DIRECTORY, "CW_" + name)
        return routes, cw_cost, status
    # -----------------------------------------------------------------------------------
    # Passo 2: Unisco le route in modo ammissibile (Provo solo save positivi)
    for s in saves:
        i, j, save_value = s
        if save_value > 0:
            if merge_routes_if_possible(routes, i, j):
                cw_cost -= save_value
            # --------- Controllo timeout --------------
            execution_time = (time.perf_counter() - start_time)
            if execution_time > EXECUTION_TIMEOUT:
                print('Timeout Scaduto')
                status = "Timeout " + str(EXECUTION_TIMEOUT)
                break
        # Se il save è negativo, non ha senso unire i percorsi
    # -----------------------------------------------------------------------------------
    # Passo 3: salva il risultato in un file .sol e stampa i risultati
    if SAVE_SOLUTION_ON_FILE:
        name = Parser.get_name(instance)
        Utils.save_results_to_file(routes, cw_cost, RESULT_DIRECTORY, "CW_" + name)
    # Stampa i risultati a schermo
    if VERBOSE:
        for index, route in enumerate(routes):
            route_str = " ".join(str(node) for node in route[1:-1])  # Escludi l'ID del deposito
            total_demand = sum(demands[node] for node in route[1:-1])  # Escludi il deposito
            print(f"Route #{index + 1}: {route_str} |total demand: {total_demand} |route cost: "
                  f"{sum(weights[route[i]][route[i + 1]] for i in range(len(route) - 1))}")
        print(f"Cost {cw_cost}")
    return cw_cost, routes, status  # todo invertire


def solve_clarke_and_wright_from_file(file_path):
    print("Parsing: ", file_path)
    instance = Parser.make_instance_from_path_name(file_path)
    return solve_clarke_and_wright_on_instance(instance)


# -------------------------- Test -----------------------------
#solve_clarke_and_wright_from_file("../resources/vrplib/Instances/Antwerp1.vrp")
