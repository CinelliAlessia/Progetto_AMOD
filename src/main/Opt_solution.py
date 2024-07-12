import time
from gurobipy import Model, GRB, quicksum
from src.main import ParseInstances as ip
from amplpy import AMPL, Environment, ampl_notebook
from src.main.ParseInstances import get_truck, get_nodes_dimension, get_node_demands, get_edge_weight, get_depots_index
from src.main.Utils import get_license

VERBOSE = False


def solve_vrp(instance):
    # Parametri del problema
    n_customers = ip.get_nodes_dimension(instance)  # Numero di nodi nel sistema, incluso il deposito
    vehicle_capacity = ip.get_truck(instance).get_capacity()  # Capacità del veicolo

    # Domanda di ogni cliente
    demands = ip.get_node_demands(instance)

    # Matrice delle distanze (simmetrica)
    dist = ip.get_edge_weight(instance)
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
    m.setParam(GRB.Param.MIPGap, 0.01)

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


def solve_vrp_with_ampl(instance):

    # 1. Leggere i dati dell'istanza utilizzando le tue funzioni esistenti
    truck = get_truck(instance)
    num_of_nodes = get_nodes_dimension(instance)
    edge_weight = get_edge_weight(instance)
    demands = get_node_demands(instance)
    list_of_depots = get_depots_index(instance)

    # Aggiungi il percorso di installazione di AMPL
    ampl_env = Environment(r"C:\Users\cinel\AMPL")
    ampl = AMPL(ampl_env)

    ampl = ampl_notebook(
        modules=["highs", "cbc", "gurobi", "cplex"],     # pick from over 20 modules including most commercial and open-source solvers
        license_uuid=get_license())    # your course UUID

    # 2. Creare il modello AMPL
    with open('VRP_Andrea.mod', 'r') as f:
        ampl.eval(f.read())

    big_m = 1000000  # Esempio di valore Big M

    # Definizione dei dati letti dall'istanza VRP
    ampl.set['V'] = range(num_of_nodes)
    ampl.set['K'] = {i: i for i in range(truck.get_min_num())}   # Numero minimo di veicoli necessari
    ampl.param['C'] = truck.get_capacity()
    ampl.param['d'] = {i: demands[i] for i in range(num_of_nodes)}

    ampl.param['c'] = {(i, j): edge_weight[i][j] if edge_weight[i][j] != 0 else big_m for i in range(num_of_nodes) for j in range(num_of_nodes)}

    if VERBOSE:
        print("V:", ampl.getData('V'))
        print("V_CUST:", ampl.getData('V_CUST'))
        print(truck.get_min_num())
        print("K:", ampl.getData('K'))
        print("C:", ampl.getData('C'))
        print("d:", ampl.getData('d'))
        print("c:", ampl.getData('c'))

    # 3. Specifica del solver (ad esempio, CPLEX)
    ampl.setOption('solver', 'cplex')  # Sostituisci 'cplex' con il solver che desideri utilizzare

    start_time = time.perf_counter()

    # 4. Risoluzione del modello AMPL
    ampl.solve()

    end_time = time.perf_counter()
    print(f"Tempo di esecuzione: {end_time - start_time} secondi")

    # 5. Estrarre i risultati
    x = ampl.getVariable('x').getValues().toPandas()
    y = ampl.getVariable('y').getValues().toPandas()
    total_cost = ampl.getObjective('Total_Cost').value()
    print("Costo totale del percorso: ", total_cost)

    nodes_in_tour = []
    for k in range(truck.get_min_num()):
        nodes = []
        for i in range(num_of_nodes):
            if y.loc[(i, k), 'y.val'] > 0.5:
                nodes.append(i)
        nodes_in_tour.append(nodes)

    for node in nodes_in_tour:
        node.append(0)
        print(node)

    roots = []
    for k in range(len(nodes_in_tour)):  # Itera per ogni veicolo o tour
        root = [0]  # Inizia ogni tour dal deposito
        start_node = 0
        while len(nodes_in_tour[k]) > 1:  # Continua finché ci sono nodi da visitare (escludendo il deposito finale)
            for i in range(len(nodes_in_tour[k])):
                next_node = nodes_in_tour[k][i]
                if x.loc[(start_node, next_node, k), 'x.val'] > 0.5:
                    if start_node != 0:  # Se non è il deposito, aggiungi il nodo di partenza al percorso
                        root.append(start_node)
                    nodes_in_tour[k].remove(start_node)  # Rimuovi il nodo di partenza dai nodi da visitare
                    start_node = next_node  # Imposta il prossimo nodo come nuovo nodo di partenza
                    break  # Esce dal ciclo for una volta trovato il prossimo nodo

        root.append(0)  # Assicurati di aggiungere il deposito alla fine del tour
        roots.append(root)  # Aggiungi il percorso completato all'elenco dei percorsi

        print(f"Tour {k}: {root}")

    total_cost = []

    for h, r in enumerate(roots):
        cost = 0
        for i in range(len(r)-1):
            cost += edge_weight[r[i]][r[i + 1]]

        total_cost.append(cost)
        print(f"Costo del tour {h}: {cost}")

    print(f"Costo totale: {sum(total_cost)}")

    # 6. Chiusura dell'istanza AMPL
    ampl.close()

    return total_cost


# Esempio di utilizzo
instance_path = "../resources/vrplib/Instances/E-n13-k4.vrp"
make_instance = ip.make_instance_from_path_name(instance_path)
optimal_cost = solve_vrp_with_ampl(make_instance)

#solve_vrp(make_instance)


print(f"Costo totale ottimale: {optimal_cost}")