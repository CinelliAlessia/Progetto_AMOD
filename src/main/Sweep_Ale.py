def sweep_algorithm(clients, vehicle_capacity):
    # Calculate angles for all clients
    for client in clients:
        client.angle = client.calculate_angle()

    # Sort clients by angle
    clients.sort(key=lambda client: client.angle)
    # for client in clients:
        # print(f"Client ID: {client.get_id()}, Coordinates: ({client.get_x()}, {client.get_y()}), Demand: {client.get_demand()}, Angle: {client.angle}")
    clusters = []
    current_cluster = []
    current_capacity = 0

    current_cluster.append(0) # Add the depot to the first cluster

    # Form clusters
    for client in clients:
        if current_capacity + client.get_demand() <= vehicle_capacity:
            current_cluster.append(client.get_id())
            current_capacity += client.get_demand()
        else:
            current_cluster.append(0) # Add the depot to the end of the cluster
            clusters.append(current_cluster)

            current_cluster = []
            current_cluster.append(0)
            current_cluster.append(client.get_id())  # Add the depot to the first cluster
            current_capacity = client.get_demand()

    # Add the last cluster if it's not empty
    if current_cluster:
        current_cluster.append(0)
        clusters.append(current_cluster)

    return clusters
