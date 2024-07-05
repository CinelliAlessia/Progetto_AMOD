# Implementazione dell'euristica Sweep

import numpy as np
import ParseInstances as Parser
import Utils

VERBOSE = True  # Se True, stampa valori delle istanze e i passaggi dell'euristica di Clarke e Wright
SAVE_SOLUTION_ON_FILE = False  # Se True, salva i risultati in un file .sol
RESULT_DIRECTORY = "resources/Heuristic_Solution/Sweep_Solutions"  # Directory di output per i risultati
RUN_TWO_OPT = True  # Se True, esegue l'euristica 2-opt per migliorare la soluzione di Sweep


# Calcola le coordinate polari di un nodo rispetto al deposito
def calculate_polar_angle(client, depot):
    return np.arctan2(client[1] - depot[1], client[0] - depot[0]) % (2 * np.pi)


def calculate_tour_cost(tour, weights):
    cost = 0
    for i in range(len(tour) - 1):
        cost += weights[tour[i]][tour[i + 1]]
    return cost


# Implementazione dell'euristica 2-opt per migliorare il costo su un tour
# todo perché interrompersi al primo miglioramento?
def two_opt(tour, weights):
    saves = 0
    best = tour
    best_cost = calculate_tour_cost(tour, weights)
    improved = True
    while improved:
        improved = False
        for i in range(1, len(tour) - 2):
            for j in range(i + 1, len(tour) - 1):  # Modifica per includere tutti gli scambi possibili
                new_tour = tour[:]
                new_tour[i:j] = tour[j - 1:i - 1:-1]  # Esegue lo scambio
                new_cost = calculate_tour_cost(new_tour, weights)
                if new_cost < best_cost:  # Verifica se il nuovo tour ha un costo minore
                    saves = best_cost - new_cost
                    best = new_tour
                    best_cost = new_cost
                    improved = True
                    break  # Esce dal ciclo interno se trova un miglioramento
            if improved:
                break  # Esce dal ciclo esterno se trova un miglioramento
    return best, saves


# Calcola la soluzione di una istanza del problema CVRP, utilizzando l'euristica Sweep
# Utilizza Parser per leggere l'istanza dal file, ottenere la lista delle coordinate dei nodi e altre informazioni
def solve_sweep_on_instance(path):
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
    sorted_nodes = [x for _, x in sorted(zip(polar_angle, range(len(polar_angle))))]  # todo, non ho capito, me fido
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
            if len(current_tour) > 2:  # Assicura che ci siano almeno 2 nodi (escluso il deposito)
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
    if RUN_TWO_OPT:
        for i in range(len(tours)):
            tours[i], saves = two_opt(tours[i], weights)
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


solve_sweep_on_instance("resources/vrplib/Instances/A-n32-k5.vrp")
