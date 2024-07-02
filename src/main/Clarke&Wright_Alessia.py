from src.main.ParseInstances import work_on_instance


nameInstance = "resources/vrplib/Instances/A-n32-k5.vrp"
#A-n32-k5 P-n16-k8
nodes, trunk = work_on_instance(nameInstance)
roots = []  # Strada percorsa da ciascun veicolo matrice N*N con N numero di clienti [[],[],[]]


def check_merge(r_i, r_j, capacity):
    # Controllo se la capacità del veicolo è rispettata
    if sum([nodes[i].get_demand() for i in r_i[0:-2]]) + sum([nodes[i].get_demand() for i in r_j[1:-1]]) > capacity:
        return False

    return True


def start():
    depots = []
    clients = []

    for u in nodes:
        if u.get_is_depots():
            depots.append(u)
        else:
            clients.append(u)
    depots = depots[0] # !!! Attenzione, ora il deposito è sempre e solo uno

    # Calcolo della matrice dei costi
    costo = [[0 for i in range(len(nodes))] for j in range(len(nodes))]
    for u in nodes:
        for v in nodes:
            if u.get_id() != v.get_id():
                costo[u.get_id()][v.get_id()] = u.get_distance()[v.get_id()]
                print(f"Costo tra {u.get_id()} e {v.get_id()}: {u.get_distance()[v.get_id()]}")

    # Creo le root iniziali
    for c in clients:
        roots.append([depots.get_id(), c.get_id(), depots.get_id()])
    print(roots)

    go = True
    while go:
        # Calcolo i savings
        savings = calculate_saving(costo)

        for saving in savings:
            if (saving[2] > 0) & (mergedRoots(saving, trunk)):
                # Se ho unito due roots, ricomincio il ciclo while
                break
        else:
            # Se sono qui non ci sono più root da mergiare
            go = False
    return roots


def calculate_saving(costo):
    print("calcolo")
    saving = []
    for r_i in roots:
        for r_j in roots:
            if r_i != r_j:
                u = r_i[-2]
                v = r_j[1]
                saving.append([u, v, costo[0][u] + costo[v][0] - costo[u][v]])
    saving = sorted(saving, key=lambda x: x[2], reverse=True)
    return saving


def mergedRoots(saving, trunk):
    for r_i in roots:
        if r_i[1] == saving[0]:
            for r_j in roots:
                if r_j[-2] == saving[1]:
                    # Ho trovato le due root che sarebbero utili unire
                    # Controllo se posso unirle
                    if check_merge(r_i, r_j, trunk.capacity):
                        print(f"Merge tra {r_i} e {r_j}")
                        roots.remove(r_i)
                        roots.remove(r_j)
                        roots.append(r_i[:-1] + r_j[1:])
                        return True
    return False

print(start())
print("FINE CALCOLO")
