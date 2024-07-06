# Implementazione dell'euristica Sweep

import numpy as np
import ParseInstances as Parser
import Utils

VERBOSE = True  # Se True, stampa valori delle istanze e i passaggi dell'euristica di Clarke e Wright
SAVE_SOLUTION_ON_FILE = False  # Se True, salva i risultati in un file .sol
RESULT_DIRECTORY = "resources/Heuristic_Solution/Sweep_Solutions"  # Directory di output per i risultati


# Calcola le coordinate polari(solo angolo) di un nodo rispetto al deposito
def calculate_polar_angle(client, depot):
    return np.arctan2(client[1] - depot[1], client[0] - depot[0]) % (2 * np.pi)


def calculate_2opt_swap_cost(tour, weights, i, j):
    if i == 0:
        prev_i = tour[-1]
    else:
        prev_i = tour[i - 1]
    if j == len(tour) - 1:
        next_j = tour[0]
    else:
        next_j = tour[j + 1]

    old_edges_cost = weights[prev_i][tour[i]] + weights[tour[j]][next_j]
    new_edges_cost = weights[prev_i][tour[j]] + weights[tour[i]][next_j]
    return new_edges_cost - old_edges_cost


def calculate_3opt_swap_cost(tour, weights, i, j, k):
    prev_i = tour[i - 1]
    next_k = tour[(k + 1) % len(tour)]

    # Calcolo i valori dei costi degli archi prima dello swap
    old_edges_cost = weights[prev_i][tour[i]] + weights[tour[j]][tour[k]] + weights[tour[j + 1]][next_k]
    # Calcolo i valori dei costi degli archi dopo lo swap
    new_edges_cost = weights[prev_i][tour[j]] + weights[tour[i]][tour[k]] + weights[tour[j + 1]][next_k]

    return new_edges_cost - old_edges_cost


# Implementazione dell'algoritmo di ottimizzazione locale 2-opt per migliorare il costo di un tour (se possibile)
# Attualmente, l'euristica è implementata con la variante First Improvement
def two_opt(tour, weights, initial_cost):
    # Se il tour ha meno di 4 nodi, non è possibile eseguire 2-opt
    if len(tour) < 4:
        return tour, 0
    best = tour
    best_cost = initial_cost
    improved = True

    while improved:
        improved = False
        for i in range(1, len(best) - 2):
            for j in range(i + 1, len(best) - 1):
                cost_diff = calculate_2opt_swap_cost(best, weights, i, j)
                if cost_diff < 0:
                    if VERBOSE:
                        print(f"2-Opt ---> Swap between {best[i]} and {best[j]} with saves {abs(cost_diff)}")
                    new_tour = best[:]
                    new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
                    best = new_tour
                    best_cost += cost_diff
                    improved = True
                    break
            if improved:  # Variante First Improvement
                break
    saves = initial_cost - best_cost
    return best, saves


# Implementazione dell'algoritmo di ottimizzazione locale 3-opt per migliorare il costo di un tour (se possibile)
def three_opt(tour, weights, initial_cost):
    best = tour[:]
    best_cost = initial_cost
    improved = True

    while improved:  # Variante First Improvement
        improved = False
        for i in range(1, len(best) - 3):
            for j in range(i + 1, len(best) - 2):
                for k in range(j + 1, len(best) - 1):
                    cost_diff = calculate_3opt_swap_cost(best, weights, i, j, k)
                    if cost_diff < 0:
                        if VERBOSE:
                            print(
                                f"3-Opt | Swap between {best[i]} and {best[j]} and {best[k]} with saves {abs(cost_diff)}")
                        new_tour = best[:]
                        new_tour[i:j + 1] = reversed(new_tour[i:j + 1])
                        best = new_tour
                        best_cost += cost_diff
                        improved = True
                        break
                if improved:
                    break
            if improved:
                break

    saves = initial_cost - best_cost
    return best, saves


def solve_sweep_on_instance(path, run_two_opt=False, run_three_opt=False):
    if not path.endswith('.vrp'):
        raise ValueError('Il file deve essere un\'istanza del CVRP in formato .vrp')
    # Creare l'istanza dal file e ottenere le informazioni necessarie
    instance = Parser.make_instance_from_path_name(path)
    node_coords = Parser.get_node_coords(instance)
    weights = Parser.get_edge_weight(instance)
    demands = Parser.get_node_demands(instance)
    depot_index = Parser.get_depots_index(instance)[0]
    depot_coord = node_coords[depot_index]
    vehicle_capacity = Parser.get_truck(instance).get_capacity()  # todo attenzione, sto usando classe truck
    # -----------------------------------------------------------------------
    polar_angle = [0.0]  # Il deposito ha angolo 0 rispetto a se stesso
    # Convertire le coordinate cartesiane in polari e calcolare l'angolo per ogni nodo
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
            tours[i], saves = two_opt(tours[i], weights, tour_cost)
            sweep_cost -= saves
    # -----------------------------------------------------------------------
    # Eseguo 3-opt per migliorare la soluzione se RUN_THREE_OPT è True
    if run_three_opt:
        for i in range(len(tours)):
            # Calcolo il costo di questo specifico tour
            tour_cost = 0
            for j in range(1, len(tours[i])):
                tour_cost += weights[tours[i][j - 1]][tours[i][j]]
            tours[i], saves = three_opt(tours[i], weights, tour_cost)
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


solve_sweep_on_instance("resources/vrplib/Instances/A-n32-k5.vrp", True)
