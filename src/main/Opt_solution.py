from gurobipy import Model, GRB, quicksum
from src.main import ParseInstances as ip
from amplpy import ampl, add_to_path
from amplpy import AMPL, Environment
from src.main.ParseInstances import get_truck, get_nodes_dimension, get_node_demands, get_edge_weight, get_depots_index


# Risolve il problema del Vehicle Routing Problem (VRP) utilizzando il modello matematico
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

    # Risoluzione del modello
    m.optimize()

    # Verifica lo stato del modello
    if m.status == GRB.OPTIMAL:
        print("Costo totale del percorso: ", m.objVal)
        solution = m.getAttr('x', x)
        route = []
        for i in range(n_customers):
            for j in range(n_customers):
                if solution[i, j] > 0.5:
                    route.append((i, j))
        print("Route ottimale: ", route)
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
    add_to_path(r"C:\Users\cinel\AMPL")


    # 2. Creare il modello AMPL
    ampl = AMPL(Environment())

    # Lettura del modello AMPL e definizione dei dati
    with open('vrp_model.mod', 'r') as f:
        ampl.eval(f.read())

    # Definizione dei dati letti dall'istanza VRP
    ampl.set('N', num_of_nodes)
    ampl.set('capacity', truck.capacity)
    ampl.set('demand', range(1, num_of_nodes + 1), demands)

    # Definizione della matrice delle distanze
    dist = {(i, j): edge_weight[i-1][j-1] for i in range(1, num_of_nodes + 1) for j in range(1, num_of_nodes + 1)}
    ampl.set('dist', dist)

    # Definizione dei depositi
    ampl.set('depots', list_of_depots)

    # 3. Risoluzione del modello AMPL
    ampl.solve()

    # 4. Recupero dei risultati
    total_cost = ampl.getObjective('TotalCost').value()

    # 5. Chiusura dell'istanza AMPL
    ampl.close()

    return total_cost


instance_path = "resources/vrplib/Instances/E-n13-k4.vrp"
# Esempio di utilizzo
make_instance = ip.make_instance_from_path_name(instance_path)
optimal_cost = solve_vrp_with_ampl(make_instance)
print(f"Costo totale ottimale: {optimal_cost}")

#solve_vrp(make_instance)
