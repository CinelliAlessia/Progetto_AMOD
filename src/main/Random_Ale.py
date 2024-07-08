from random import shuffle


def vrp_random_1(nodes, capacity):
    """ Prendo un cliente a caso,
    se la sua domanda è soddisfatta lo aggiungo al cluster, altrimenti continuo a cercare,
    se nessun cliente può essere aggiunto a quel determinato cluster allora lo chiudo e ne apro un altro"""

    id_depots = 0  # Assuming depot ID is 0 for simplicity
    nodes = [node for node in nodes if node.get_id() != id_depots]  # Remove depot from nodes

    shuffle(nodes)  # Shuffle nodes for random selection

    # List to store all clusters inizialmente n clusters vuoti
    roots = [[] for _ in range(len(nodes))]

    for root in roots:
        for client in nodes:
            if check_capacity(root, capacity, client):
                root.append(client)
                nodes.remove(client)
        else:
            continue

    processed_roots = []
    for root in roots:
        if root:  # Check if the root is not empty
            processed_root = [id_depots] + [c.get_id() for c in root] + [id_depots]
            processed_roots.append(processed_root)

    return processed_roots


def vrp_random_2(nodes, capacity):
    """ Preso un client a caso, controlla se puo essere aggiunto al primo cluster, se cosi non è,
    controlla se puo essere aggiunto al secondo cluster, ecc. se non puo essere aggiunto a nessun cluster
    se ne crea uno nuovo
    :param nodes:
    :param capacity:
    :return:
    """

    id_depots = 0  # Assuming depot ID is 0 for simplicity
    nodes = [node for node in nodes if node.get_id() != id_depots]  # Remove depot from nodes

    shuffle(nodes)  # Shuffle nodes for random selection
    roots = []

    for client in nodes:
        for root in roots:
            if check_capacity(root, capacity, client):
                root.append(client)
                break
        else:
            roots.append([client])

    processed_roots = []
    for root in roots:
        if root:  # Check if the root is not empty
            processed_root = [id_depots] + [c.get_id() for c in root] + [id_depots]
            processed_roots.append(processed_root)

    return processed_roots


def check_capacity(cluster, capacity, new_client):
    if len(cluster) > 0:
        current_capacity = sum(client.get_demand() for client in cluster)
        return current_capacity + new_client.get_demand() <= capacity
    else:
        return True
