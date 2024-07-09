import itertools
from src.main.Utils import calculate_cost

TWO_OPT = True
THREE_OPT = True
PRINT = False

matrix_distance = []


# Calcolo l'angolo tra tutti i nodi e il deposito
def initialize(nodes):
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
        matrix_distance.append(client.get_all_distance())
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

    clusters_2 = None
    clusters_3 = None

    if TWO_OPT or THREE_OPT:
        clusters_2, clusters_3 = optimize_clusters(clusters)

    return clusters_2, clusters_3


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


def two_opt(route):
    best_route = route
    best_distance = calculate_total_distance(route)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue  # no point in reversing two adjacent edges
                new_route = route[:]
                new_route[i:j] = route[j - 1:i - 1:-1]  # reverse the subsection
                new_distance = calculate_total_distance(new_route)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_route = new_route
                    route = best_route
                    improved = True
    return best_route, best_distance


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
        distance += matrix_distance[start_node][next_node]
    return distance


def three_opt(route):
    """
    Algoritmo 3-opt per migliorare una soluzione di un problema di instradamento dei veicoli (VRP).

    :param route: Lista degli indici dei nodi che rappresentano il percorso.
    :return: Un percorso ottimizzato e la sua distanza totale.
    """

    best_distance = calculate_total_distance(route)
    best_route = route

    for (i, j, k) in itertools.combinations(range(1, len(route) - 1), 3):
        new_routes = apply_3opt(route, i, j, k)

        for new_route in new_routes:
            new_distance = calculate_total_distance(new_route)
            if new_distance < best_distance:
                best_route = new_route
                best_distance = new_distance

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
    return new_tours
