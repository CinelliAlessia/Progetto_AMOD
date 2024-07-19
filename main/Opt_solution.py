from gurobipy import Model, GRB, quicksum
import ParseInstances as Parser

VERBOSE = False


def solve_vrp_whit_gurobi(instance):
    # Parametri del problema
    n_customers = Parser.get_nodes_dimension(instance)  # Numero di nodi nel sistema, incluso il deposito
    vehicle_capacity = Parser.get_truck(instance).get_capacity()  # Capacità del veicolo

    # Domanda di ogni cliente
    demands = Parser.get_node_demands(instance)

    # Matrice delle distanze (simmetrica)
    dist = Parser.get_edge_weight(instance)
    print(dist)

    # Verifica che la matrice delle distanze abbia le dimensioni corrette
    assert dist.shape == (n_customers, n_customers), "Dimensione della matrice dist non corretta"

    # Creazione del modello
    m = Model("VRP")

    # Variabili binarie x[i, j] che indicano se l'arco (i, j) è percorso
    x = m.addVars(n_customers, n_customers, vtype=GRB.BINARY, name="x")

    # Variabili continue u[i] che rappresentano la carica di ogni veicolo dopo aver servito il cliente i
    u = m.addVars(n_customers, vtype=GRB.CONTINUOUS, name="u")

    # Funzione obiettivo: minimizzare la distanza totale percorsa
    m.setObjective(quicksum(dist[i, j] * x[i, j] for i in range(n_customers) for j in range(n_customers)), GRB.MINIMIZE)

    # Vincoli
    # 1. Ogni cliente deve essere visitato esattamente una volta
    m.addConstrs(quicksum(x[i, j] for j in range(n_customers) if i != j) == 1 for i in range(1, n_customers))
    m.addConstrs(quicksum(x[j, i] for j in range(n_customers) if i != j) == 1 for i in range(1, n_customers))

    # 2. I veicoli devono partire e tornare al deposito
    m.addConstr(quicksum(x[0, j] for j in range(1, n_customers)) == 1)
    m.addConstr(quicksum(x[j, 0] for j in range(1, n_customers)) == 1)

    # 3. Vincoli di capacità (subtour elimination constraints)
    m.addConstrs(
        (u[i] - u[j] + vehicle_capacity * x[i, j] <= vehicle_capacity - demands[j] for i in range(n_customers) for j in
         range(1, n_customers) if i != j), "Capacity")

    # 4. Domanda del deposito è zero
    m.addConstr(u[0] == 0)

    # Imposta limite di tempo (ad esempio 300 secondi) e MIP gap (ad esempio 1%)
    m.setParam(GRB.Param.TimeLimit, 300)
    m.setParam(GRB.Param.MIPGap, 0.0001)

    # Risoluzione del modello
    m.optimize()

    # Verifica lo stato del modello
    if m.status == GRB.OPTIMAL or m.status == GRB.TIME_LIMIT:
        if m.status == GRB.OPTIMAL:
            print("Soluzione ottimale trovata.")
        elif m.status == GRB.TIME_LIMIT:
            print("Tempo limite raggiunto. Soluzione migliore trovata entro il tempo limite:")
        print("Costo totale del percorso: ", m.objVal)
        try:
            solution = m.getAttr('x', x)
            route = []
            for i in range(n_customers):
                for j in range(n_customers):
                    if solution[i, j] > 0.5:
                        route.append((i, j))
            print("Route ottimale: ", route)
        except:
            print("Non è stato possibile recuperare la soluzione.")
    else:
        print("Nessuna soluzione ottimale trovata.")


# Esempio di utilizzo
instance_path = "../resources/vrplib/Instances/E-n13-k4.vrp"
make_instance = Parser.make_instance_from_path_name(instance_path)
solve_vrp_whit_gurobi(make_instance)
