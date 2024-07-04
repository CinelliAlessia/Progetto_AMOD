import gurobipy as gp
from gurobipy import GRB

from src.main.ParseInstances import work_on_instance


# Soluzione ottima delle istanze di VRP
def solve_vrp(nodes, truck, distances):
    num_nodes = len(nodes)
    V = range(num_nodes)
    A = [(i, j) for i in V for j in V if i != j]
    c = {(i, j): distances[i][j] for i, j in A}
    Q = truck.capacity

    mdl = gp.Model('VRP')

    # Variabili di decisione
    x = mdl.addVars(A, vtype=GRB.BINARY)
    u = mdl.addVars(V, vtype=GRB.CONTINUOUS)

    # Funzione obiettivo
    mdl.setObjective(gp.quicksum(x[i, j]*c[i, j] for i, j in A), GRB.MINIMIZE)

    # Vincoli
    mdl.addConstrs(gp.quicksum(x[i, j] for j in V if j != i) == 1 for i in V)
    mdl.addConstrs(gp.quicksum(x[j, i] for j in V if j != i) == 1 for i in V)

    # Vincoli di capacità ed eliminazione dei sotto cicli
    mdl.addConstrs((x[i, j] == 1) >> (u[i] + nodes[i].demand <= u[j]) for i, j in A if i != 0 and j != 0)
    mdl.addConstrs(u[i] >= nodes[i].demand for i in V if i != 0)
    mdl.addConstrs(u[i] <= Q for i in V if i != 0)

    # Ottimizzazione
    mdl.optimize()

    # Estrazione dei risultati
    routes = []
    for i, j in A:
        if x[i, j].X > 0.5:
            routes.append((i, j))

    return routes

# Assumi che `nodes` sia una lista di nodi, `truck` un oggetto camion con attributo capacità,
# e `distances` una matrice delle distanze tra i nodi.
