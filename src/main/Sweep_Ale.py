from src.main.Plotter import plot_roots_graph
from src.main.Utils import calculate_cost

TWO_OPT = True
THREE_OPT = False

PRINT = True

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

            current_cluster = []  # Svuoto il cluster corrente
            current_cluster.append(id_depots)  # Aggiungo il deposito in prima posizione
            current_cluster.append(client.get_id())  # Aggiungo il cliente sarà sicuramente possibile servire
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

    if TWO_OPT or THREE_OPT:
        plot_roots_graph(nodes, clusters)
        clusters = optimize_clusters(clusters, nodes)

    return clusters


def optimize_clusters(clusters, nodes):
    # Return immediately if no optimization is enabled
    if not (TWO_OPT or THREE_OPT):
        return clusters

    optimized_clusters = []
    optimization_function = None

    # Determine which optimization function to use
    if TWO_OPT:
        optimization_function = two_opt
    elif THREE_OPT:
        optimization_function = three_opt

    # Apply the selected optimization function to each cluster
    for cluster in clusters:
        optimized_cluster, _ = optimization_function(cluster, nodes)
        optimized_clusters.append(optimized_cluster)

    return optimized_clusters


def two_opt(route, nodes):
    best_route = route
    best_distance = 0
    improved = True

    while improved:
        improved = False
        best_distance = calculate_total_distance(best_route)
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: continue  # Salta i nodi adiacenti
                new_route = two_opt_swap(best_route, i, j)
                new_distance = calculate_total_distance(new_route)
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
    return best_route, best_distance


def calculate_total_distance(route):
    """
    Calcola la distanza totale di un tour dato.
    :param route: Lista degli indici dei nodi che rappresentano il tour.
    :return: Distanza totale del tour.
    """
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += matrix_distance[route[i]][route[i + 1]]
    return total_distance


def two_opt_swap(route, i, k):
    new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route


def three_opt(route, nodes):
    """
    Algoritmo 3-opt per migliorare una soluzione di un problema di instradamento dei veicoli (VRP).

    :param route: Lista degli indici dei nodi che rappresentano il route.
    :param nodes: Lista di tutti i nodi.
    :return: Un route ottimizzato e la sua distanza totale.
    """
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 3):  # Inizia da 1 per mantenere fisso il deposito all'inizio
            for j in range(i + 2, len(route) - 2):  # Evita l'ultimo nodo (deposito)
                for k in range(j + 2, len(route) - 1):  # Evita l'ultimo nodo (deposito)
                    new_tour = apply_3opt(route, i, j, k, nodes)
                    if calculate_total_distance(new_tour) < calculate_total_distance(route):
                        route = new_tour
                        improved = True

    return route, calculate_total_distance(route)


def apply_3opt(tour, i, j, k, nodes):
    """
    Applica una mossa 3-opt al tour dato i, j, k.

    :param tour: Lista degli indici dei nodi che rappresentano il tour.
    :param i, j, k: Indici dei nodi in cui verrà applicata la mossa 3-opt.
    :param nodes: Lista di tutti i nodi.
    :return: Nuovo tour dopo aver applicato la mossa 3-opt.
    """

    new_tours = []

    # Segmenti: [0...i-1], [i...j-1], [j...k-1], [k...n-1]

    # Nessun cambiamento (Originale)
    new_tours.append(tour[:])

    # Cambia il segmento (i...j-1)
    new_tours.append(tour[:i] + tour[i:j][::-1] + tour[j:])

    # Cambia il segmento (j...k-1)
    new_tours.append(tour[:j] + tour[j:k][::-1] + tour[k:])

    # Cambia i segmenti (i...j-1) e (j...k-1)
    new_tours.append(tour[:i] + tour[i:j][::-1] + tour[j:k][::-1] + tour[k:])

    # Cambia i segmenti (i...k-1)
    new_tours.append(tour[:i] + tour[i:k][::-1] + tour[k:])

    # Scambio tra i segmenti
    new_tours.append(tour[:i] + tour[j:k] + tour[i:j] + tour[k:])
    new_tours.append(tour[:i] + tour[j:k][::-1] + tour[i:j][::-1] + tour[k:])
    new_tours.append(tour[:i] + tour[j:k][::-1] + tour[i:j] + tour[k:])
    new_tours.append(tour[:i] + tour[j:k] + tour[i:j][::-1] + tour[k:])

    best_tour = min(new_tours, key=lambda t: calculate_total_distance(t))

    return best_tour
