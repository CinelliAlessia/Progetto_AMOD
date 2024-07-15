import os
import time

from amplpy import AMPL, Environment
import ParseInstances as Parser
import Utils

VERBOSE = True
MODEL_PATH = 'VRP_Andrea.mod'
DATS_DIR = '../resources/vrplib/DATs'

File_to_solve = os.path.join(DATS_DIR, 'E-n13-k4.dat')

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

    ampl = AMPL(Environment(r"C:\Users\andre\AMPL"))

    ampl.read(model_file)
    ampl.readData(data_file)

    # Impostare il solver CPLEX con timeout di 180 secondi
    ampl.setOption('solver', 'cplex')
    #ampl.setOption('cplex_options', 'timelimit=300')

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
        'Total_Cost': total_cost
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

    return routes, results['Total_Cost']


def solve_multiple_instances(model_file, data_dir):
    """
    Esegue un modello AMPL su tutti i file di dati in una directory specificata.

    Parameters:
    - model_file (str): Il percorso al file del modello AMPL (.mod).
    - data_dir (str): Il percorso alla directory contenente i file dei dati (.dat).
    """
    for filename in os.listdir(data_dir):
        if filename.endswith('.dat'):
            # Utilizza la funzione sopra
            solve_single_instance(model_file, os.path.join(data_dir, filename))


#Utils.calculate_routes_cost([[ 0,  2,  0 ],[ 0,  6,  0 ],[ 0,  8,  0 ],[ 0, 15, 12, 10,  0 ],[ 0, 14,  5,  0 ],[ 0, 13,  9,  7,  0 ],[ 0, 11,  4,  0 ],[ 0,  3,  1,  0 ]], weights, demands)
#print(weights)
#solve_single_instance(MODEL_PATH, File_to_solve)
#solve_multiple_instances(MODEL_PATH, data_dir)
