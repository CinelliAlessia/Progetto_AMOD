from random import shuffle


def vrp_random(nodes, capacity, demands, id_depots):
    """ Preso un client a caso, controlla se puo essere aggiunto al primo cluster, se cosi non è,
    controlla se puo essere aggiunto al secondo cluster, ecc. se non puo essere aggiunto a nessun cluster
    se ne crea uno nuovo
    :param id_depots: indice del deposito
    :param demands: domanda totale di tutti i clienti
    :param nodes: lista di clienti
    :param capacity: capacità dei veicoli
    :return:
    """

    nodes = nodes[:id_depots] + nodes[id_depots + 1:]  # Rimuove il deposito dalla lista dei clienti

    truck_max = int(demands/capacity) + 1
    rem_capacities = [0 for _ in range(truck_max)]

    shuffle(nodes)  # Randomizza la lista dei clienti
    routes = []

    for client in nodes:
        for i, route in enumerate(routes):
            if rem_capacities[i] + client.get_demand() <= capacity:
                route.append(client)
                break
        else:
            routes.append([client])     # Crea una nuova rotta se non può essere aggiunto a nessun cluster

    processed_roots = []
    for route in routes:
        if route:  # Controlla se la rotta non è vuota e aggiunge il deposito all'inizio e alla fine
            processed_root = [id_depots] + [c.get_id() for c in route] + [id_depots]
            processed_roots.append(processed_root)

    # TODO calcola e restituisci il costo
    return processed_roots


def vrp_random_alternative(nodes, capacity, demands, id_depots):
    """ Prendo un cliente a caso,
    se la sua domanda è soddisfatta lo aggiungo al cluster, altrimenti continuo a cercare,
    se nessun cliente può essere aggiunto a quel determinato cluster allora lo chiudo e ne apro un altro"""

    nodes = nodes[:id_depots] + nodes[id_depots + 1:]  # Rimuove il deposito dalla lista dei clienti
    shuffle(nodes)  # Randomizza la lista dei clienti

    truck_max = int(demands/capacity) + 1

    # List to store all clusters inizialmente n clusters vuoti
    roots = [[] for _ in range(truck_max)]
    rem_capacities = [0 for _ in range(len(nodes))]

    for i, root in enumerate(roots):
        for client in nodes:
            if rem_capacities[i] + client.get_demand() <= capacity:
                rem_capacities[i] += client.get_demand()
                root.append(client)
                nodes.remove(client)

            if rem_capacities[i] == capacity:
                break

    processed_roots = []
    for root in roots:
        if root:  # Controlla se la rotta non è vuota e aggiunge il deposito all'inizio e alla fine
            processed_root = [id_depots] + [c.get_id() for c in root] + [id_depots]
            processed_roots.append(processed_root)

    return processed_roots
