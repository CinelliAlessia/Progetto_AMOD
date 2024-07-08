from src.main.Plotter import plot_roots_graph
from src.main.Utils import calculate_cost

TWO_OPT = True
THREE_OPT = False


# Calcolo l'angolo tra tutti i nodi e il deposito
def initialize(nodes):
    nodes.sort(key=lambda node: node.get_id())
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
        client.angle = client.calculate_angle_to_depots(x_dep, y_dep)

    # Ordino tutti i nodi in base all'angolo minore
    nodes.sort(key=lambda c: c.angle)
    return nodes, id_depots


def sweep_algorithm(nodes, vehicle_capacity):
    nodes, id_depots = initialize(nodes)  # Ottengo i nodi ordinati per angolo minore
    print("Nodi ordinati:")
    for n in nodes:
        print(n.get_id(), n.angle)

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

    plot_roots_graph(nodes, clusters)

    print("Clusters non opt:")
    for c in clusters:
        print(c)
    print(calculate_cost(clusters, nodes))

    optimized_clusters = optimize_clusters(clusters, nodes)

    print("Clusters opt:")
    for c in optimized_clusters:
        print(c)

    return optimized_clusters


def two_opt(route, nodes):
    best_route = route
    best_distance = calculate_total_distance(best_route, nodes)
    improved = True
    while improved:
        improved = False
        best_distance = calculate_total_distance(best_route, nodes)
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: continue  # Salta i nodi adiacenti
                new_route = two_opt_swap(best_route, i, j)
                new_distance = calculate_total_distance(new_route, nodes)
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
    return best_route, best_distance


def three_opt(route, nodes):
    # TODO
    return []


def optimize_clusters(clusters, nodes):
    optimized_clusters = []
    for cluster in clusters:
        if TWO_OPT:
            optimized_cluster, _ = two_opt(cluster, nodes)
        elif THREE_OPT:
            optimized_cluster = three_opt(cluster, nodes)
        else:
            return
        optimized_clusters.append(optimized_cluster)
    return optimized_clusters


def find_node_by_id(node_id, nodes):
    for node in nodes:
        if node.get_id() == node_id:
            return node
    return None


def calculate_total_distance(route, nodes):
    total_distance = 0
    for i in range(len(route) - 1):
        node = find_node_by_id(route[i], nodes)
        if node is not None:
            total_distance += node.get_distance(route[i + 1])
    return total_distance


def two_opt_swap(route, i, k):
    new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
    return new_route
