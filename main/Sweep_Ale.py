import itertools
from tornado import concurrent
from Utils import calculate_cost, verify_if_feasible

PRINT = False
distance_matrix = []

TIMEOUT = 30
global inc_route, inc_cost, vehicles_capacity, nodes_global


def update_incumbent(routes, costs):
    global inc_route, inc_cost
    if verify_if_feasible(routes, vehicles_capacity, nodes_global):
        inc_route, inc_cost = routes, costs


def initialize(nodes):
    """
    Inizializza la matrice delle distanze e calcola l'angolo tra tutti i nodi e il deposito.
    :param nodes: Lista dei nodi.
    :return: Lista dei nodi ordinati per angolo minore e l'id del deposito.
    """

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

    nodes = nodes[:id_depots] + nodes[id_depots + 1:]  # Rimuovo il deposito dalla lista dei clienti

    # Ordino tutti i nodi in base all'angolo minore
    nodes.sort(key=lambda c: c.angle)

    return nodes, id_depots


def sweep_inner(nodes, vehicle_capacity, opt_2, opt_3):
    global vehicles_capacity, nodes_global
    vehicles_capacity = vehicle_capacity
    nodes_global = nodes

    nodes, id_depots = initialize(nodes)  # Ottengo i nodi ordinati per angolo minore

    clusters = []
    costs = []

    current_cluster = [id_depots]
    current_capacity = 0
    cost = 0

    last_client = None

    # Form clusters
    for client in nodes:
        # Se il cliente rispetta la capacità del veicolo, lo aggiungo al cluster
        if current_capacity + client.get_demand() <= vehicle_capacity:
            cost += client.get_distance(current_cluster[-1])  # Aggiungo il costo del cliente al costo totale
            current_capacity += client.get_demand()
            current_cluster.append(client.get_id())

        # Altrimenti, chiudo il cluster e ne inizializzo un altro
        else:
            current_cluster.append(id_depots)  # Aggiungo il deposito in ultima posizione
            cost += last_client.get_distance(id_depots)  # Aggiungo il costo dal cliente al deposito
            costs.append(cost)
            clusters.append(current_cluster)  # Aggiungo il cluster alla lista

            # Inizializzo il nuovo cluster
            cost = client.get_distance(id_depots)  # Aggiungo il costo dal deposito al cliente
            current_cluster = [id_depots, client.get_id()]  # Svuoto il cluster corrente
            current_capacity = client.get_demand()  # Aggiorno la capacità

        last_client = client

    # Se l'ultimo cluster non contiene il deposito, lo aggiungo
    if current_cluster[-1] != id_depots:
        current_cluster.append(id_depots)
        cost += last_client.get_distance(id_depots)  # Aggiungo il costo dal cliente al deposito
        costs.append(cost)
        clusters.append(current_cluster)

    if PRINT:
        print_result("Clusters non ottimizzati", clusters, nodes)

    if not opt_2 and not opt_3:
        best_route, best_costs = clusters, sum(costs)
        update_incumbent(best_route, best_costs)
        return best_route, best_costs
    else:
        return optimize_2opt(clusters, opt_3)


def sweep_algorithm(nodes, vehicle_capacity, opt_2, opt_3):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(sweep_inner, nodes, vehicle_capacity, opt_2, opt_3)
        try:
            return future.result(timeout=TIMEOUT)  # Timeout di 5 minuti (300 secondi)
        except concurrent.futures.TimeoutError:
            print("Timeout! Restituisco l'incumbent trovato fino ad ora.", opt_2, opt_3)
            return inc_route, inc_cost


def print_result(string, clusters, nodes):
    if len(nodes) < 50:
        print(string)
        for c in clusters:
            print(c)

    print(f"Costo {string}: {calculate_cost(clusters, nodes)}")
    # Plotter.plot_if_not_explicit(clusters, nodes)


def optimize_2opt(clusters, opt_3):

    optimized_clusters_2 = []
    costs_2opt = []

    for cluster in clusters:
        cluster_2opt, cost = two_opt(cluster)

        costs_2opt.append(cost)
        optimized_clusters_2.append(cluster_2opt)

    best_route, best_costs = optimized_clusters_2, sum(costs_2opt)
    update_incumbent(best_route, best_costs)

    if not opt_3:
        return best_route, best_costs
    else:
        return opt3_on_opt2(best_route, best_costs)


def opt3_on_opt2(clusters_2opt, costs_2opt):
    """
    Applica l'algoritmo 2-opt e successivamente 3-opt su ogni cluster ottimizzato con 2-opt.
    :param clusters_2opt:
    :param costs_2opt:
    :return: Le routes ottimizzate con 2-opt o 3-opt.
    """

    optimized_clusters_3 = []
    costs_3opt = []

    for cluster in clusters_2opt:
        cluster_3opt, cost = three_opt(cluster)
        costs_3opt.append(cost)
        optimized_clusters_3.append(cluster_3opt)

    costs_3opt = sum(costs_3opt)

    if costs_2opt <= costs_3opt:
        if PRINT: print("Soluzione scelta: 2-opt")
        best_route, best_costs = clusters_2opt, costs_2opt
        update_incumbent(best_route, best_costs)
    else:
        if PRINT: print("Soluzione scelta: 3-opt")
        best_route, best_costs = optimized_clusters_3, costs_3opt
        update_incumbent(best_route, best_costs)
    return best_route, best_costs


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
                    best_tour, best_distance = new_tour, new_distance
                    improved = True

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


def calculate_saving(i, j, tour):
    # Calcolo del costo attuale
    current_cost = distance_matrix[tour[i]][tour[i+1]] + distance_matrix[tour[j]][tour[j+1]]
    # Calcolo del costo dopo lo swap
    new_cost = distance_matrix[tour[i]][tour[j]] + distance_matrix[tour[i+1]][tour[j+1]]
    return new_cost - current_cost  # Se è negativo, allora conviene fare lo swap


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
                best_route, best_distance = new_route, new_distance
                improved = True
                break   # Esco dal ciclo for

        if improved:    # Se ho trovato un miglioramento, continuo, se non ne ho trovato, esco
            continue

    return best_route, best_distance


def apply_3opt(route, i, j, k):
    new_tours = [
        route[:i] + route[i:j] + route[j:k] + route[k:],  # No change (a)
        route[:i] + route[i:j] + route[j:k][::-1] + route[k:],  # Reversing tour[j:k] (c)
        route[:i] + route[i:j][::-1] + route[j:k] + route[k:],  # Reversing tour[i:j] (d)
        route[:i] + route[i:j][::-1] + route[j:k][::-1] + route[k:],  # Reversing both (e)
        route[:i] + route[j:k] + route[i:j] + route[k:],  # Swapping tour[i:j] with tour[j:k] (h)
        route[:i] + route[j:k] + route[i:j][::-1] + route[k:],  # Swapping and reversing tour[i:j] (g)
        route[:i] + route[j:k][::-1] + route[i:j] + route[k:],  # Swapping and reversing tour[j:k] (f)
        route[:i] + route[j:k][::-1] + route[i:j][::-1] + route[k:]  # Swapping and reversing both (b)
    ]

    opt_cost = float("inf")
    opt_route = []
    for r in new_tours:
        distance = calculate_total_distance(r)
        if distance < opt_cost:
            opt_route, opt_cost = r, distance
    return opt_route, opt_cost
