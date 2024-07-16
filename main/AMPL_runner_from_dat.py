import os
import time
import pandas as pd
from amplpy import AMPL, Environment

import ParseInstances

VERBOSE = True
MODEL_PATH = 'VRP_Andrea.mod' # Se si vuole cambiare modello basta cambiare qui
AMPL_ENVIROMENT_PATH = "C:\\Users\\andre\\AMPL"
DATS_DIR = '../resources/vrplib/DATs'
OUTPUT_PATH = 'Results/Modello_AMPL'
OUTPUT_BASE_FILE_NAME = 'AMPL_results'
NAME_BY_SIZE_DIR = "../resources/vrplib/Name_of_instances_by_dimension/"

# Se impostati a True, eseguirà il modello MIP per VRP per le istanze di quel tipo
SMALL = False
MID_SMALL = False
MID = False
MID_LARGE = False
LARGE = False
X_LARGE = False

# Per eseguire su una singola istanza
File_to_solve = os.path.join(DATS_DIR, 'P-n22-k8.dat')


# SOLO PER TESTARE SE IL VALORE DELLA SOLUZIONE OTTIMA CORRISPONDE AL COSTO DLLE ROUTES UTILIZZATE
#instance = Parser.make_instance_from_path_name('../resources/vrplib/Instances/P-n22-k8.vrp')
#weights = Parser.get_edge_weight(instance)
#demands = Parser.get_node_demands(instance)


def solve_ampl_model(model_file, data_file):
    """
    Esegue un modello AMPL con un file di dati specifico.

    Parameters:
    - model_file (str): Il percorso al file del modello AMPL (.mod).
    - data_file (str): Il percorso al file dei dati AMPL (.dat).

    Returns:
    - dict: Risultati del risolutore AMPL.
    """
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Il file del modello {model_file} non esiste.")

    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Il file dei dati {data_file} non esiste.")

    ampl = AMPL(Environment(AMPL_ENVIROMENT_PATH))

    ampl.read(model_file)
    ampl.readData(data_file)

    # Impostare il solver CPLEX con timeout di 180 secondi
    ampl.setOption('solver', 'cplex')
    ampl.setOption('cplex_options', 'timelimit=300')

    # Stampare le informazioni sui set
    if VERBOSE:
        print(ampl.getData('V'))
        print(ampl.getData('V_CUST'))
        print(ampl.getData('K'))
        print(ampl.getParameter('C'))
        print(ampl.getParameter('d').getValues().toDict())
        print(ampl.getParameter('c').getValues().toPandas())

    start_time = time.perf_counter()
    ampl.solve()
    end_time = time.perf_counter()
    print(f"Tempo di esecuzione: {end_time - start_time} secondi")

    # Estrarre i risultati
    x = ampl.getVariable('x').getValues().toPandas()
    y = ampl.getVariable('y').getValues().toPandas()
    total_cost = ampl.getObjective('Total_Cost').value()

    results = {
        'x': x,
        'y': y,
        'Total_Cost': total_cost,
        'Execution_time': end_time - start_time
    }
    return results


def calculate_routes_from_matrix(x_val, y_val):
    routes = []
    # Trova il numero di veicoli
    num_vehicles = len(y_val.index.levels[1])

    for h in range(1, num_vehicles + 1):
        route = []
        current_node = 1  # partiamo dal deposito

        while True:
            # Aggiungi il nodo corrente alla route se viene servito dal veicolo h
            if y_val.loc[(current_node, h), 'y.val'] == 1:
                route.append(current_node - 1)

            # Trova il prossimo nodo nell'arco percorso dal veicolo h
            next_node = None
            for j in range(1, len(x_val.index.levels[1]) + 1):
                if x_val.loc[(current_node, j, h), 'x.val'] == 1:
                    next_node = j
                    break

            # Se il prossimo nodo è il deposito, termina la route
            if next_node == 1:
                break

            # Vai al prossimo nodo
            current_node = next_node

        # Aggiungi l'ultima visita al deposito per completare il ciclo
        route.append(0)

        # Aggiungi la route trovata alla lista delle routes
        routes.append(route)

    return routes


def solve_single_instance(model_file, data_file):
    """
    Esegue un modello AMPL su un singolo file di dati specificato.

    Parameters:
    - model_file (str): Il percorso al file del modello AMPL (.mod).
    - data_file (str): Il percorso al file dei dati AMPL (.dat).
    """
    print(f"Solving for {data_file}")
    results = solve_ampl_model(model_file, data_file)
    routes = calculate_routes_from_matrix(results['x'], results['y'])
    if VERBOSE:
        for r in routes:
            print(r)
        print(results['Total_Cost'])

    return routes, results['Total_Cost'], results['Execution_time']


def solve_multiple_instances(size, model_file, names_file):

    if not os.path.exists(names_file):
        print("Il file non esiste")
        return

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    out_filename = size + "_" + OUTPUT_BASE_FILE_NAME + '.csv'

    f = open(f"{OUTPUT_PATH}{out_filename}", "w")
    n = open(names_file, "r")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,#Node,#Truck,Capacity,Optimal_Cost,AMPL_cost,APX,Execution_time\n")

    for filename in n:
        file_name = filename.strip()

        if file_name.endswith(".vrp"):
            instance_name = os.path.splitext(filename)[0]

            if instance_name in results_df['Instance_Name'].values:
                print(f"{instance_name} già risolto.")
                continue

            data_file = os.path.join(DATS_DIR, filename)
            routes, cost, exec_time = solve_single_instance(model_file, data_file)

            # Ottieni dettagli sull'istanza dai dati (per esempio, numero di nodi, veicoli, capacità)
            # Qui suppongo che queste informazioni siano disponibili nei dati o nel nome del file
            # Modifica questo codice per estrarre correttamente le informazioni necessarie
            # Per esempio:
            num_nodes = None
            num_trucks = len(routes)
            capacity = None  # Sostituisci con il valore corretto
            optimal_cost = None # Sostituisci con il valore corretto
            apx = None

            new_row = {
                'Size': size,
                'Instance_Name': instance_name,
                '#Node': num_nodes,
                '#Truck': num_trucks,
                'Capacity': capacity,
                'Optimal_Cost': optimal_cost,
                'Model_cost': cost,
                'APX': apx,
                'Execution_time': exec_time
            }
            results_df = results_df.append(new_row, ignore_index=True)

    results_df.to_csv(output_file, index=False)



#Utils.calculate_routes_cost([[ 0,  2,  0 ],[ 0,  6,  0 ],[ 0,  8,  0 ],[ 0, 15, 12, 10,  0 ],[ 0, 14,  5,  0 ],[ 0, 13,  9,  7,  0 ],[ 0, 11,  4,  0 ],[ 0,  3,  1,  0 ]], weights, demands)
#print(weights)
solve_single_instance(MODEL_PATH, File_to_solve)

if SMALL:
    solve_multiple_instances("small", MODEL_PATH, f"{NAME_BY_SIZE_DIR}small_instances_name.txt")
if MID_SMALL:
    solve_multiple_instances("mid_small", MODEL_PATH, f"{NAME_BY_SIZE_DIR}mid_small_instances_name.txt")
if MID:
    solve_multiple_instances("mid", MODEL_PATH, f"{NAME_BY_SIZE_DIR}mid_instances_name.txt")
if MID_LARGE:
    solve_multiple_instances("mid_large", MODEL_PATH, f"{NAME_BY_SIZE_DIR}mid_large_instances_name.txt")
if LARGE:
    solve_multiple_instances("large", MODEL_PATH, f"{NAME_BY_SIZE_DIR}large_instances_name.txt")
if X_LARGE:
    solve_multiple_instances("x_large", MODEL_PATH, f"{NAME_BY_SIZE_DIR}x_large_instances_name.txt")
