import itertools
from src.main.Utils import calculate_cost
import Plotter as plotter

TWO_OPT = True
THREE_OPT = True
PRINT = False

distance_matrix = []


# Calcolo l'angolo tra tutti i nodi e il deposito
def initialize(nodes):
    distance_matrix.clear()

    id_depots = 0
    x_dep = 0
    y_dep = 0
    for n in nodes:
        if n.get_is_depots():
            id_depots = n.get_id()
            x_dep = n.get_x()
            y_dep = n.get_y()
            break

    for client in nodes:
        distance_matrix.append(client.get_all_distance())
        client.angle = client.calculate_angle_to_depots(x_dep, y_dep)

    # Ordino tutti i nodi in base all'angolo minore
    nodes.sort(key=lambda c: c.angle)
    return nodes, id_depots


def sweep_algorithm(nodes, vehicle_capacity):
    nodes, id_depots = initialize(nodes)  # Ottengo i nodi ordinati per angolo minore

    clusters = []
    current_cluster = []
    current_capacity = 0

    # Form clusters
    for client in nodes:
        if current_capacity + client.get_demand() <= vehicle_capacity:
            current_cluster.append(client.get_id())
            current_capacity += client.get_demand()
        else:
            current_cluster.append(id_depots)  # Aggiungo il deposito in ultima posizione
            clusters.append(current_cluster)  # Aggiungo il cluster alla lista

            current_cluster = [id_depots, client.get_id()]  # Svuoto il cluster corrente
            current_capacity = client.get_demand()  # Aggiorno la capacità

    # Se l'ultimo cluster non contiene il deposito, lo aggiungo
    if current_cluster[-1] != id_depots:
        current_cluster.append(id_depots)
        clusters.append(current_cluster)

    if PRINT:
        print("Clusters non opt:")
        for c in clusters:
            print(c)
        print(calculate_cost(clusters, nodes))
        plotter.plot_roots_graph(nodes, clusters)

    clusters_2 = None
    clusters_3 = None

    if TWO_OPT or THREE_OPT:
        clusters_2, clusters_3 = optimize_clusters(clusters)

    return clusters, clusters_2, clusters_3


def optimize_clusters(clusters):
    # Return immediately if no optimization is enabled
    if not (TWO_OPT or THREE_OPT):
        return clusters

    optimized_clusters_2 = []
    optimized_clusters_3 = []

    # Determine which optimization function to use
    if TWO_OPT:
        optimization_function = two_opt
        for cluster in clusters:
            optimized_cluster_2, _ = optimization_function(cluster)
            optimized_clusters_2.append(optimized_cluster_2)

    if THREE_OPT:
        for cluster in clusters:
            optimized_cluster_3, _ = three_opt(cluster)
            optimized_clusters_3.append(optimized_cluster_3)

    return optimized_clusters_2, optimized_clusters_3


def two_opt_swap(tour, i, j):
    new_tour = tour[:i+1] + tour[i+1:j+1][::-1] + tour[j+1:]
    return new_tour


def two_opt(tour):
    num_nodes = len(tour)
    best_tour = tour
    best_distance = calculate_total_distance(tour)
    improved = True

    while improved:
        improved = False
        for i in range(1, num_nodes - 2):
            for j in range(i + 1, num_nodes - 1):
                if j - i == 1:
                    continue  # No need to reverse two adjacent edges
                # Calculate the change in distance
                new_tour = two_opt_swap(best_tour, i, j)
                new_distance = calculate_total_distance(new_tour)
                delta_distance = new_distance - best_distance
                if delta_distance < 0:
                    # Perform 2-opt swap
                    # print(f"2-opt swap: {i} {j}")
                    # print(f"Before: {best_tour}")
                    best_tour = new_tour
                    # print(f"After: {best_tour}")
                    improved = True
                    best_distance = new_distance

    return best_tour, best_distance


def calculate_total_distance(route):
    """
    Calcola la distanza totale di un tour dato.
    :param route: Lista degli indici dei nodi che rappresentano il tour.
    :return: Distanza totale del tour.
    """
    distance = 0
    for i in range(len(route) - 1):
        start_node = route[i]
        next_node = route[i + 1]
        distance += distance_matrix[start_node][next_node]
    return distance


def three_opt(route):
    """
    Algoritmo 3-opt per migliorare una soluzione di un problema di instradamento dei veicoli (VRP).
    :param route: Lista degli indici dei nodi che rappresentano il percorso.
    :return: Un percorso ottimizzato e la sua distanza totale.
    """
    num_nodes = len(route)
    best_route = route
    best_distance = calculate_total_distance(route)
    improved = True

    while improved:
        improved = False
        for (i, j, k) in itertools.combinations(range(1, num_nodes - 1), 3):
            if not j - i > 1 and not k - j > 1:
                continue

            # print(f"3-opt swap: {i} {j} {k}")
            new_route, new_distance = apply_3opt(best_route, i, j, k)
            if new_distance < best_distance:
                best_route = new_route
                best_distance = new_distance
                improved = True
                # print(f"local best root {best_route}")
                break
        if improved:    # Se ho trovato un miglioramento, continuo, se non ne ho trovato, esco
            continue

    return best_route, best_distance


def apply_3opt(route, i, j, k):
    new_tours = [
        route[:i] + route[i:j] + route[j:k] + route[k:],  # No change
        route[:i] + route[i:j] + route[j:k][::-1] + route[k:],  # Reversing tour[j:k]
        route[:i] + route[i:j][::-1] + route[j:k] + route[k:],  # Reversing tour[i:j]
        route[:i] + route[i:j][::-1] + route[j:k][::-1] + route[k:],  # Reversing both
        route[:i] + route[j:k] + route[i:j] + route[k:],  # Swapping tour[i:j] with tour[j:k]
        route[:i] + route[j:k] + route[i:j][::-1] + route[k:],  # Swapping and reversing tour[i:j]
        route[:i] + route[j:k][::-1] + route[i:j] + route[k:],  # Swapping and reversing tour[j:k]
        route[:i] + route[j:k][::-1] + route[i:j][::-1] + route[k:]  # Swapping and reversing both
    ]
    opt_cost = float("inf")
    opt_route = []
    for r in new_tours:
        distance = calculate_total_distance(r)
        if distance < opt_cost:
            opt_cost = distance
            opt_route = r
    return opt_route, opt_cost
