#
def check_merge(r_i, r_j, capacity, nodes):
    # Controllo se la capacità del veicolo è rispettata
    demand = sum([nodes[elem_i].get_demand() for elem_i in r_i[:-1]]) + sum([nodes[elem_j].get_demand() for elem_j in r_j[1:]])
    if demand > capacity:
        return False
    return True


def start(nodes, truck):

    depots = []
    clients = []
    roots = []  # Lista delle rotte, tanti quanti sono i nodi

    for u in nodes:
        if u.get_is_depots():
            depots.append(u)
        else:
            clients.append(u)
    depots = depots[0] # !!! todo Attenzione, ora il deposito è sempre e solo uno

    # Calcolo della matrice dei costi
    costo = get_distance(nodes)

    # Creo le root iniziali
    for c in clients:
        roots.append([depots.get_id(), c.get_id(), depots.get_id()])
    print(roots)

    # Calcolo i savings
    savings = calculate_saving(costo, roots)

    for saving in savings:
        if saving[2] >= 0:
            mergedRoots(saving, roots, truck, nodes)

    demands_roots = []
    total_cost = []

    for r in roots:
        cost = 0
        demand = 0
        for i in range(len(r)-1):
            cost += costo[r[i]][r[i+1]]
            demand = demand + nodes[r[i]].get_demand()

        print(f"Route: {r} - Cost: {cost} - Demand: {demand}")
        total_cost.append(cost)
        demands_roots.append(demand)

    print(f"Total cost: {sum(total_cost)}")

    return roots, total_cost


def get_distance(nodes):
    # Calcolo della matrice dei costi
    costo = [[0 for _ in range(len(nodes))] for _ in range(len(nodes))]
    for u in nodes:
        for v in nodes:
            if u.get_id() != v.get_id():
                costo[u.get_id()][v.get_id()] = u.get_distance()[v.get_id()]
    return costo


# Calcolo i savings ! attenzione se inserisce nel saving 3,8 non inserisce 8,3
def calculate_saving(costo, roots):
    saving = []
    considered_pairs = set()  # Set to track considered pairs
    for r_i in roots:
        for r_j in roots:
            if r_i != r_j:
                u = r_i[-2]
                v = r_j[1]
                # Check if the pair or its reverse has not been considered
                if (u, v) not in considered_pairs and (v, u) not in considered_pairs:
                    calculate = costo[0][u] + costo[v][0] - costo[u][v]
                    if calculate >= 0:
                        saving.append([u, v, calculate])
                        # Mark the pair as considered
                        considered_pairs.add((u, v))
    saving = sorted(saving, key=lambda x: x[2], reverse=True)
    print(saving)
    return saving


def mergedRoots(saving, roots, truck, nodes):
    for r_i in roots:
        if r_i[1] == saving[0] or r_i[-2] == saving[0]:
            for r_j in roots:
                if (r_j[1] == saving[1] or r_j[-2] == saving[1]) and r_i != r_j:
                    # Ho trovato le due root che sarebbe utile unire
                    if not check_merge(r_i, r_j, truck.get_capacity(), nodes):     # Controllo se posso unirle in base alla capacità
                        return False

                    new_root = []
                    # Se i è l'ultimo e j il primo -> i[:-1] + j[1:]
                    if r_i[-2] == saving[0] and r_j[1] == saving[1]:
                        new_root = r_i[:-1] + r_j[1:]
                    # Se j è l'ultimo e i il primo -> j[:-1] + i[1:]
                    elif r_j[-2] == saving[1] and r_i[1] == saving[0]:
                        new_root = r_j[:-1] + r_i[1:]

                    roots.remove(r_i)
                    roots.remove(r_j)
                    roots.append(new_root)
                    print(f"Merge tra {r_i} e {r_j}, new route: {new_root}")
                    return True
    return False