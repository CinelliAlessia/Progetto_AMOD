def sweep_algorithm(nodes, vehicle_capacity):
    print(f"Sweep Ale Vehicle capacity: {vehicle_capacity}")
    nodes.sort(key=lambda node: node.get_id())

    x_dep = 0
    y_dep = 0
    for n in nodes:
        if n.get_is_depots():
            x_dep = n.get_x()
            y_dep = n.get_y()
            break

    # Calculate angles for all clients
    for client in nodes:
        client.angle = client.calculate_angle_to_depots(x_dep, y_dep)

    # Sort clients by angle
    nodes.sort(key=lambda c: c.angle)
    print(f"Sorted nodes: {', '.join([f'{node.get_id()}, {node.angle}' for node in nodes])}")
    # for client in clients:
    # print(f"Client ID: {client.get_id()}, Coordinates: ({client.get_x()}, {client.get_y()}), Demand: {client.get_demand()}, Angle: {client.angle}")

    clusters = []
    current_cluster = []
    current_capacity = 0
    current_cluster.append(0) # Add the depot to the first cluster

    # Form clusters
    for client in nodes:
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
    if len(current_cluster) > 0:
        current_cluster.append(0)
        clusters.append(current_cluster)

    return clusters
