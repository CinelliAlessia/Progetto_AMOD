# Implementazione dell'euristica Sweep
import numpy as np
import ParseInstances as Parser
import Utils

VERBOSE = False  # Se True, stampa valori delle istanze e i passaggi dell'euristica di Clarke e Wright
SAVE_SOLUTION_ON_FILE = False  # Se True, salva i risultati in un file .sol
RESULT_DIRECTORY = "../resources/Heuristic_Solution/Sweep_Solutions"  # Directory di output per i risultati

# ------------ Definisco le variabili globali che descrivono l'istanza specifica ------------------------
global node_coords, weights, demands, depot_index, depot_coord, vehicle_capacity, name  # Imposto variabili globali


# Calcola le coordinate polari(solo angolo) di un nodo rispetto al deposito
def calculate_polar_angle(client, depot):
    return np.arctan2(client[1] - depot[1], client[0] - depot[0]) % (2 * np.pi)


# Funzione per calcolare il costo di un 2-opt swap
def calculate_2opt_swap_cost(tour, i, j):  # i e j esprimono la posizione degli archi da scambiare
    # Arco i, vuol dire ch l'elemento in posizione i rimarrà "fermo"
    # Arco j, vuol dire che l'elemento in posizione j verrà scambiato con l'elemento in posizione j+1
    # Mentre arco j vuol dire che l'elemento in posizione j-1, andrà subito dopo i
    prev_i = tour[i - 1]  # nodo in posizione i-1
    if j == len(tour) - 1:
        next_j = tour[0]
    else:
        next_j = tour[j + 1]  # nodo in posizione j+1

    # Calcolo del costo attuale
    current_cost = weights[tour[i]][tour[i+1]] + weights[tour[j]][next_j]  # esempio arco 4-5 + 9-0
    # Calcolo del costo dopo lo swap
    new_cost = weights[tour[i]][tour[j]] + weights[tour[i+1]][next_j]  # esempio arco 4-9 + 5-0
    return new_cost - current_cost


# Implementazione dell'algoritmo di ottimizzazione locale 2-opt
# Esempio: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0] -> [0, 1, 2, 3, 4, 9, 8, 7, 6, 5, 0] scambio tra archi #5 e #9
def two_opt(tour, initial_cost):
    length = len(tour)
    if length < 4:
        return tour, 0
    best_cost = initial_cost
    improved = True

    while improved:
        improved = False
        for i in range(1, length - 2):
            for j in range(i + 1, length - 1):
                cost_diff = calculate_2opt_swap_cost(tour, i, j)  # Valuta il costo dello swap tra arco numero i e j
                if cost_diff < 0 and j-i > 1:
                    if VERBOSE:
                        print(f"2-Opt ---> Swap between {tour[i]} and {tour[j]} with saves {abs(cost_diff)}")
                    # subito dopo i ci sarà j,
                    # e ne seguirà il cammino (al contrario) da i fino a j della route originale
                    new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]
                    best_cost += cost_diff
                    tour = new_tour
                    improved = True
    saves = initial_cost - best_cost
    return tour, saves


def three_opt(tour, initial_cost):
    return tour, 0


# Esegue l'euristica Sweep su un'istanza specifica (Istanza già creata in precedenza)
def solve_sweep_on_instance(instance, run_two_opt=False, run_three_opt=False):
    # Inizializzo le variabili globali
    global node_coords, weights, demands, depot_index, depot_coord, vehicle_capacity, name
    node_coords = Parser.get_node_coords(instance)
    weights = Parser.get_edge_weight(instance)
    demands = Parser.get_node_demands(instance)
    depot_index = Parser.get_depots_index(instance)[0]
    depot_coord = node_coords[depot_index]
    vehicle_capacity = Parser.get_truck(instance).get_capacity()  # todo attenzione, sto usando classe truck
    path = Parser.get_name(instance)
    # -----------------------------------------------------------------------
    # Convertire le coordinate cartesiane in polari e calcolare l'angolo per ogni nodo
    polar_angle = [0.0]  # Il deposito ha angolo 0 rispetto a se stesso
    for i in range(len(node_coords)):
        if i != depot_index:
            polar_angle.append(calculate_polar_angle(node_coords[i], depot_coord))
    # Ordinare i nodi in base all'angolo polare rispetto al deposito
    sorted_nodes = [x for _, x in sorted(zip(polar_angle, range(len(polar_angle))))]
    if VERBOSE:
        print(f"Sorted Nodes: {sorted_nodes}")
    # -----------------------------------------------------------------------
    # Generare, scorrendo i nodi in ordine crescente di angolo, i tour rispettando la capacità del veicolo
    sweep_cost = 0
    tours = []
    current_tour = [depot_index]  # Il primo nodo è il deposito
    current_capacity = 0
    for node in sorted_nodes:
        if node == depot_index:
            continue
        demand = demands[node]
        if current_capacity + demand <= vehicle_capacity:
            current_tour.append(node)
            current_capacity += demand
            # Calcolo del costo dell'arco aggiunto
            sweep_cost += weights[current_tour[-2]][current_tour[-1]]
        else:
            if len(current_tour) > 1:  # Verifica che il tour non sia vuoto prima di aggiungerlo
                current_tour.append(depot_index)  # Aggiungi il ritorno al deposito
                sweep_cost += weights[current_tour[-2]][depot_index]  # Costo di ritorno al deposito
                tours.append(current_tour)  # Aggiungi il tour corrente alla lista dei tour
            current_tour = [depot_index, node]  # Inizia un nuovo tour
            current_capacity = demand
            sweep_cost += weights[depot_index][node]  # Costo per il primo nodo del nuovo tour
    if len(current_tour) > 1:  # Verifica e aggiungi l'ultimo tour se non vuoto
        current_tour.append(depot_index)
        sweep_cost += weights[current_tour[-2]][depot_index]
        tours.append(current_tour)
    # -----------------------------------------------------------------------
    # Eseguo 2-opt per migliorare la soluzione se RUN_TWO_OPT è True
    if run_two_opt:
        for i in range(len(tours)):
            # Calcolo il costo di questo specifico tour
            tour_cost = 0
            for j in range(1, len(tours[i])):
                tour_cost += weights[tours[i][j - 1]][tours[i][j]]
            tours[i], saves = two_opt(tours[i], tour_cost)
            sweep_cost -= saves
    # -----------------------------------------------------------------------
    # Eseguo 3-opt per migliorare la soluzione se RUN_THREE_OPT è True
    if run_three_opt:
        for i in range(len(tours)):
            # Calcolo il costo di questo specifico tour
            tour_cost = 0
            for j in range(1, len(tours[i])):
                tour_cost += weights[tours[i][j - 1]][tours[i][j]]
            tours[i], saves = three_opt(tours[i], tour_cost)
            sweep_cost -= saves
    # -----------------------------------------------------------------------
    # Print dei risultati nello stesso formato dei file .sol
    if VERBOSE:
        print(f"Solution for instance {path}:")
        for index, route in enumerate(tours):
            route_str = " ".join(str(node) for node in route[1:-1])
            print(f"Route #{index + 1}: {route_str}")
        print(f"Cost {sweep_cost}")
    # -----------------------------------------------------------------------
    # Salva i risultati in un file .sol# Salvo i risultati su file
    if SAVE_SOLUTION_ON_FILE:
        Utils.save_results_to_file(tours, sweep_cost, RESULT_DIRECTORY, path)

    return tours, sweep_cost


# Esegue l'euristica se viene usando il file .vrp
def solve_sweep_from_file(file_path, run_two_opt=False, run_three_opt=False):
    instance = Parser.make_instance_from_path_name(file_path)
    return solve_sweep_on_instance(instance, run_two_opt, run_three_opt)


#solve_sweep_from_file("../resources/vrplib/Instances/A-n32-k5.vrp", True, False)
