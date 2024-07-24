import os
from gurobipy import Model, GRB, quicksum
import ParseInstances as Parser
import time

VERBOSE = False
OUTPUT_PATH = "Results/MIP/"  # Directory di output per i risultati
NAME_FILE = "MIP_Solutions.csv"  # Nome del file di output
INSTANCE_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze
CURRENT_INSTANCE = None


def solve_vrp_with_gurobi(instance, verbose=False, max_time_seconds=300, gap=0.0001, integrality_focus=1):
    # Parametri del problema
    n_customers = Parser.get_nodes_dimension(instance)  # Numero di nodi nel sistema, incluso il deposito
    vehicle_capacity = Parser.get_truck(instance).get_capacity()  # Capacità del veicolo
    k = Parser.get_truck(instance).get_min_num()  # Numero di veicoli

    # Domanda di ogni cliente
    demands = Parser.get_node_demands(instance)

    # Matrice delle distanze (simmetrica)
    dist = Parser.get_edge_weight(instance)
    print(dist)

    # Verifica che la matrice delle distanze abbia le dimensioni corrette
    assert dist.shape == (n_customers, n_customers), "Dimensione della matrice dist non corretta"

    # Creazione del modello
    m = Model("VRP")

    # Parametri del modello
    m.setParam('MIPGap', gap)
    m.setParam('OutputFlag', verbose)
    m.setParam('TimeLimit', max_time_seconds)
    m.setParam('IntegralityFocus', integrality_focus)

    # Variabili binarie x[i, j, h] che indicano se l'arco (i, j) è percorso dal veicolo h
    x = m.addVars(n_customers, n_customers, k, vtype=GRB.BINARY, name="x")

    # Variabili binarie y[i, h] che indicano se il cliente i è servito dal veicolo h
    y = m.addVars(n_customers, k, vtype=GRB.BINARY, name="y")

    # Variabili continue u[i, h] che rappresentano l'ordine di visita per eliminare i sottotour
    u = m.addVars(n_customers, k, vtype=GRB.CONTINUOUS, name="u")

    # Funzione obiettivo: minimizzare la distanza totale percorsa
    m.setObjective(
        quicksum(dist[i, j] * x[i, j, h] for i in range(n_customers) for j in range(n_customers) for h in range(k)),
        GRB.MINIMIZE)

    # Vincoli
    # 1. Ogni cliente deve essere visitato esattamente una volta
    m.addConstrs(
        quicksum(x[i, j, h] for j in range(n_customers) if i != j) == y[i, h] for i in range(1, n_customers) for h in range(k))
    m.addConstrs(
        quicksum(x[j, i, h] for j in range(n_customers) if i != j) == y[i, h] for i in range(1, n_customers) for h in range(k))

    # 2. I veicoli devono partire e tornare al deposito
    m.addConstrs(quicksum(x[0, j, h] for j in range(1, n_customers)) == 1 for h in range(k))
    m.addConstrs(quicksum(x[j, 0, h] for j in range(1, n_customers)) == 1 for h in range(k))

    # 3. Ogni cliente deve essere servito da esattamente un veicolo
    m.addConstrs(quicksum(y[i, h] for h in range(k)) == 1 for i in range(1, n_customers))

    # 4. Vincoli di capacità
    m.addConstrs(
        quicksum(demands[i] * y[i, h] for i in range(1, n_customers)) <= vehicle_capacity for h in range(k))

    # 5. Vincoli di eliminazione dei sottotour (MTZ)
    m.addConstrs(u[i, h] >= 2 for i in range(1, n_customers) for h in range(k))
    m.addConstrs(u[i, h] <= n_customers for i in range(1, n_customers) for h in range(k))
    m.addConstrs(
        (u[i, h] - u[j, h] + n_customers * x[i, j, h] <= n_customers - 1 for i in range(1, n_customers) for j in range(1, n_customers) if i != j for h in range(k)),
        "SubtourElimination")

    # Risoluzione del modello
    start_time = time.perf_counter()
    m.optimize()
    execution_time = time.perf_counter() - start_time

    # Estrazione e visualizzazione della soluzione
    routes = []
    total_cost = None
    status = "Infeasible"

    if m.status == GRB.OPTIMAL or m.status == GRB.TIME_LIMIT:
        if m.status == GRB.OPTIMAL:
            print("Soluzione ottimale trovata.")
            status = "Optimal"
        elif m.status == GRB.TIME_LIMIT:
            print("Timout raggiunto")
            status = "Timeout"
        total_cost = m.objVal
        print("Costo totale del percorso: ", total_cost)

        try:
            x_val = m.getAttr('X', x)
            y_val = m.getAttr('X', y)
            routes = calculate_routes_from_gurobi_solution(x_val, y_val, n_customers, k)
        except:
            print("Non è stato possibile recuperare la soluzione.")
    else:
        print("Nessuna soluzione ottimale trovata.")

    write(routes, total_cost, execution_time, status)
    return routes, total_cost, execution_time, status


def calculate_routes_from_gurobi_solution(x_val, y_val, n_customers, k):
    routes = [[] for _ in range(k)]  # Inizializza una lista di route per ogni veicolo
    for h in range(k):  # Per ogni veicolo
        current_node = 0  # Parti dal deposito
        route = [current_node]  # Inizia la route con il deposito
        while True:
            found_next = False
            for j in range(1, n_customers):  # Cerca il nodo successivo
                if x_val.get((current_node, j, h), 0) > 0.5:  # Se x[i,j,h] indica un passaggio al nodo successivo
                    route.append(j)  # Aggiungi il nodo alla route
                    current_node = j  # Aggiorna il nodo corrente
                    found_next = True
                    break
            if not found_next or current_node == 0:  # Se non trovi un nodo successivo o sei tornato al deposito
                # Aggiungi l'ultimo nodo visitato al deposito per completare il ciclo
                route.append(0)
                break  # Termina la costruzione della route per questo veicolo
        routes[h] = route  # Assegna la route costruita al veicolo corrente
    return routes


def write(routes, total_cost, execution_time, status):
    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{OUTPUT_PATH}"):
        os.makedirs(OUTPUT_PATH)

    # Se non esiste, lo creo e scrivo l'intestazione, altrimenti appendo solamente le soluzioni
    if not os.path.exists(f"{OUTPUT_PATH}{NAME_FILE}"):
        f = open(f"{OUTPUT_PATH}{NAME_FILE}", "w")
        # Intestazione del file csv
        f.write("Instance_Name,#Node,#Truck,Capacity,Opt_cost,Incumbent,Execution_time,Status,Routes\n")
    else:
        f = open(f"{OUTPUT_PATH}{NAME_FILE}", "a")

    capacity = Parser.get_truck(instance).get_capacity()
    n_nodes = Parser.get_nodes_dimension(instance)
    n_truck = Parser.get_truck(instance).get_min_num()
    if n_truck == 0:
        n_truck = None

    opt = Parser.get_optimal_cost_from_path(INSTANCE_DIRECTORY + CURRENT_INSTANCE)

    # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
    f.write(f"{CURRENT_INSTANCE},{n_nodes},{n_truck},{capacity},{opt},{total_cost},{execution_time},{status},{routes}\n")
    f.close()


# Apro il file .txt in lettura per leggere i nomi delle istanze separate per dimensione
txt_path = "Results/MIP/remaining_small_mip.txt"
n = open(txt_path, "r")

for line in n:  # Per ogni istanza scritta nel file
    # Esempio di utilizzo
    line = line.strip()
    CURRENT_INSTANCE = line
    instance_path = "../resources/vrplib/Instances/" + line
    instance = Parser.make_instance_from_path_name(instance_path)
    solve_vrp_with_gurobi(instance, True,300,0.1,0)