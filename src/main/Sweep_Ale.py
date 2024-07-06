from src.main.Plotter import plot_roots_graph


def sweep_algorithm(nodes, vehicle_capacity):
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

    # Calculate angles for all clients
    for client in nodes:
        client.angle = client.calculate_angle_to_depots(x_dep, y_dep)

    # Sort clients by angle
    nodes.sort(key=lambda c: c.angle)

    clusters = []
    current_cluster = []
    current_capacity = 0

    # Form clusters
    for client in nodes:
        if current_capacity + client.get_demand() <= vehicle_capacity:
            current_cluster.append(client.get_id())
            current_capacity += client.get_demand()
        else:
            current_cluster.append(id_depots) # Add the depot to the end of the cluster
            clusters.append(current_cluster)

            current_cluster = []
            current_cluster.append(id_depots)
            current_cluster.append(client.get_id())  # Add the depot to the first cluster
            current_capacity = client.get_demand()

    # Add the last cluster if it's not empty
    if len(current_cluster) > 0:
        current_cluster.append(id_depots)
        clusters.append(current_cluster)

    plot_roots_graph(nodes, clusters)

    print("Clusters non opt:")
    for c in clusters:
        print(c)

    optimized_clusters = optimize_clusters(clusters, nodes)

    print("Clusters opt:")
    for c in optimized_clusters:
        print(c)

    return optimized_clusters


def two_opt(route, nodes):
    best_route = route
    improved = True
    while improved:
        improved = False
        best_distance = calculate_total_distance(best_route, nodes)
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                if j - i == 1: continue  # Salta i nodi adiacenti
                new_route = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
                new_distance = calculate_total_distance(new_route, nodes)
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improved = True
    return best_route


def optimize_clusters(clusters, nodes):
    optimized_clusters = []
    for cluster in clusters:
        optimized_cluster = two_opt(cluster, nodes)
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
        node1 = find_node_by_id(route[i], nodes)
        if node1 is not None:
            total_distance += node1.get_distance(route[i + 1])
    return total_distance
