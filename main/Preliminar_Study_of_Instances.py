import os
import ParseInstances as Parser
from Utils import calculate_routes_cost

# Definizione delle soglie per le dimensioni delle istanze, (se cambiate, run found_instance_size() per aggiornare)
SMALL_THRESHOLD = 50
MID_SMALL_THRESHOLD = 100
MID_THRESHOLD = 250
MID_LARGE_THRESHOLD = 500
LARGE_THRESHOLD = 1350
OUTPUT_DIRECTORY = "../resources/vrplib/Name_of_instances_by_dimension"


# Scorre tutti i file nella directory delle istanze e cerca le istanze di tipo MDVRP (Multi Depot VRP)
# Restituisce una lista con i nomi dei file delle istanze MDVRP e il numero di istanze trovate
def found_mdvrp_instances(directory_path="../resources/vrplib/Instances"):
    mdvrp_file = []
    file_count = 0
    mdvrp_count = 0
    for file in os.listdir(directory_path):
        if file.endswith(".vrp"):
            file_count += 1
            with open(os.path.join(directory_path, file), "r") as f:
                content = f.read()
                if 'DEPOT_SECTION' in content:
                    depot_section = content.split('DEPOT_SECTION')[1].split('EOF')[0]
                    depots = depot_section.strip().split('\n')
                    print(depots)
                    if len(depots) > 1:
                        #print(depots)
                        mdvrp_file.append(file)
                        mdvrp_count += 1
    print(f"Trovate: {mdvrp_count} MDVRP istanze su {file_count} istanze totali")
    for i in mdvrp_file:
        print(i)
    return mdvrp_file, mdvrp_count


# Scorre tutti i file nella directory delle istanze e cerca le istanze di tipo AVRP
# Restituisce una lista con i nomi dei file delle istanze AVRP e il numero di istanze trovate
# Se il campo 'edge_weight_type' è EXPLICIT, sono fornite le distanze come matrice in due modi differenti,
# specificati dal campo 'edge_weight_format':
# LOWER_ROW: matrice triangolare inferiore senza diagonale (Per definizione Simmetrica)
# FULL_MATRIX: matrice completa (Non è detto che descriva un grafo Simmetrico)
def found_avrp_instances(directory_path="../resources/vrplib/Instances"):
    avrp_file = []
    file_count = 0
    avrp_count = 0
    for file in os.listdir(directory_path):
        if file.endswith(".vrp"):
            file_count += 1
            with open(os.path.join(directory_path, file), "r") as f:
                content = f.read(1000) # Leggo solo i primi 1000 caratteri per ridurre il tempo di esecuzione
                if 'FULL_MATRIX' in content:
                    avrp_file.append(file)
                    avrp_count += 1
    print(f"Trovate: {avrp_count} istanze con pesi formattati come FULL_MATRIX, su {file_count} istanze totali")
    for i in avrp_file:
        print(i)
    return avrp_file, avrp_count


# Algoritmo per contare il numero di istanze di tipo small, mid-small, mid, mid-large, large e x-large
def found_instance_size(directory_path="../resources/vrplib/Instances"):
    # Definizioni delle soglie come già presente
    small = 0
    mid_small = 0
    mid = 0
    mid_large = 0
    large = 0
    x_large = 0

    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    # Dizionario per tenere traccia dei file aperti
    # Se file già esistenti vengono troncati riscritti dall'inizio
    files = {
        "small": open(f"{OUTPUT_DIRECTORY}/small_instances_name.txt", "w"),
        "mid_small": open(f"{OUTPUT_DIRECTORY}/mid_small_instances_name.txt", "w"),
        "mid": open(f"{OUTPUT_DIRECTORY}/mid_instances_name.txt", "w"),
        "mid_large": open(f"{OUTPUT_DIRECTORY}/mid_large_instances_name.txt", "w"),
        "large": open(f"{OUTPUT_DIRECTORY}/large_instances_name.txt", "w"),
        "x_large": open(f"{OUTPUT_DIRECTORY}/x_large_instances_name.txt", "w")
    }
    for file in os.listdir(directory_path):
        if file.endswith(".vrp"):
            with open(os.path.join(directory_path, file), "r") as f:
                content = f.read()
                if 'DIMENSION' in content:
                    dimension = int(content.split('DIMENSION : ')[1].split('\n')[0])
                    if dimension <= SMALL_THRESHOLD:
                        small += 1
                        files["small"].write(file + "\n")
                    # Continuation of the conditionals to categorize and write instance names
                    elif dimension <= MID_SMALL_THRESHOLD:
                        mid_small += 1
                        files["mid_small"].write(file + "\n")
                    elif dimension <= MID_THRESHOLD:
                        mid += 1
                        files["mid"].write(file + "\n")
                    elif dimension <= MID_LARGE_THRESHOLD:
                        mid_large += 1
                        files["mid_large"].write(file + "\n")
                    elif dimension <= LARGE_THRESHOLD:
                        large += 1
                        files["large"].write(file + "\n")
                    else:
                        x_large += 1
                        files["x_large"].write(file + "\n")
    # Close all the files after processing
    for file in files.values():
        file.close()
    # Optionally, print the counts for each category
    print(f"Small: {small}, Mid-Small: {mid_small}, Mid: {mid}, Mid-Large: {mid_large}, Large: {large}, "
          f"X-Large: {x_large}, \nNomi delle istanze scritti in {OUTPUT_DIRECTORY}")


#found_avrp_instances()
#found_mdvrp_instances()
found_instance_size()


# ----- Aggiornamento costi nel file .sol -----

def read_sol_file(filepath):
    """
    Legge le routes e il costo da un file .sol
    :param filepath: path del file .sol
    :return: routes, costo
    """
    routes = []
    cost = None
    with open(filepath, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith('Route #'):
                route_str = line.strip().split(': ')[1]
                nodes = list(map(int, route_str.split()))
                formatted_route = [0] + nodes + [0]
                routes.append(formatted_route)
            elif line.startswith('Cost'):
                cost = float(line.split()[1].strip())

    return routes, cost


def fix_cost(directory_sol, path_file_size):
    """

    :param directory_sol:
    :return:
    """

    # Controlla che la directory dei file .sol esista
    if not os.path.isdir(directory_sol):
        print(f"Directory '{directory_sol}' non trovata.")
        return

    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(path_file_size):
        print(f"Il file {path_file_size} non esiste")
        return

    # Apro il file in lettura per leggere i nomi delle istanze separate per dimensione
    n = open(path_file_size, "r")

    for line in n:  # Per ogni istanza scritta nel file -> line = file.vrp
        sol_file = line.strip().replace(".vrp", ".sol")
        filepath = os.path.join(directory_sol, sol_file)
        print(f"Modifica del file: {filepath}")

        # Leggi le routes e il costo dal file .sol
        routes, file_cost = read_sol_file(filepath)

        name_file = sol_file.split(".")[0]

        # Carica l'istanza dal file VRP
        instance_path = f'../resources/vrplib/Instances/{name_file}.vrp'
        instance = Parser.make_instance_from_path_name(instance_path)

        # Ottieni i pesi degli archi e le richieste dei nodi
        weights = Parser.get_edge_weight(instance)
        demands = Parser.get_node_demands(instance)

        # Calcola il costo totale delle routes
        calculated_cost = calculate_routes_cost(routes, weights, demands)
        print(f"Costo calcolato dalle routes: {calculated_cost}")
        print(f"Costo indicato nel file .sol: {file_cost}")

        # Confronto tra costo calcolato e costo dal file .sol
        if calculated_cost == file_cost:
            print("I costi coincidono.")
        else:
            modify_optimal_cost_sol(filepath, calculated_cost)
            print("Attenzione: i costi non coincidono.")

        print()  # Linea vuota per separare le stampe dei vari file


def modify_optimal_value_vrp(filepath, new_optimal_value):
    """
    Modifica il costo ottimo di un'istanza VRP nel campo 'comment' se è identificato con Optimal value: {value}
    :param filepath:
    :param new_optimal_value:
    :return:
    """
    # Leggi tutte le linee dal file VRP
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Trova e modifica l'optimal value
    for i, line in enumerate(lines):
        if line.startswith('COMMENT'):
            parts = line.split('Optimal value:')
            parts[-1] = f' Optimal value: {new_optimal_value})\n'
            lines[i] = ':'.join(parts)
            break

    # Sovrascrivi il file VRP con l'optimal value modificato
    with open(filepath, 'w') as file:
        file.writelines(lines)


def modify_optimal_cost_sol(filepath, new_optimal_value):
    """
    Modifica il costo ottimo di un'istanza VRP nel campo 'Cost {value}' di un file .sol
    :param filepath: path del file .sol
    :param new_optimal_value: nuovo costo ottimo
    :return:
    """
    # Leggi tutte le linee dal file .sol
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Trova e modifica l'optimal value
    for i, line in enumerate(lines):
        if line.startswith('Cost'):
            parts = line.split('Cost')
            parts[-1] = f'Cost {new_optimal_value}\n'
            lines[i] = ''.join(parts)
            break

    # Sovrascrivi il file .sol con l'optimal value modificato
    with open(filepath, 'w') as file:
        file.writelines(lines)


# Esempio di utilizzo per la directory specificata
directory_path_sol = "../resources/vrplib/Solutions/"
directory_path_name_instances = "../resources/vrplib/Name_of_instances_by_dimension/"
#fix_cost(directory_path_sol, f"{directory_path_name_instances}x_large_instances_name.txt")
