import time
import Random_Ale as Random
import ParseInstances as Parser
import os
import Utils
import Config


# Se impostati a True, eseguirà l'euristica di Clarke e Wright per le istanze di quel tipo
SMALL = False
MID_SMALL = False
MID = True
MID_LARGE = False
LARGE = False
X_LARGE = True

# ------------------------------------------------------------------------------------------------------------
ACTIONS = Config.ACTION_RANDOM
TIMEOUT = False
TIMEOUT_VALUE = 300  # Timeout di 5 minuti (300 secondi)
SKIP_SOLUTION_OUT_OF_TRUCK = True
# ------------------------------------------------------------------------------------------------------------
if ACTIONS:
    # Directory dei file contenenti i nomi delle istanze
    NAME_BY_SIZE_PATH = "./resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "./main/Results/Random_Solutions/"  # Directory di output per i risultati
    INSTANCES_DIRECTORY = "./resources/vrplib/Instances/"  # Directory delle istanze

else:
    # Directory dei file contenenti i nomi delle istanze
    NAME_BY_SIZE_PATH = "../resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "Results/Random_Solutions/"  # Directory di output per i risultati
    INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze

OUTPUT_BASE_FILE_NAME = "RANDOM_APX_and_Time"  # Aggiungere come prefisso il numero del run
RANDOM_ITERATION_NUMBER = 10000


def solve_random_for_instance_name_in_file(size, file_path):
    """
    Esegue un modello Randomico per le istanze elencate nel file_path (tramite nome)
    :param size:
    :param file_path:
    :return:
    """

    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(file_path):
        print(f"Il file {file_path} non esiste")
        return

    # Apro il file in lettura per leggere i nomi delle istanze separate per dimensione
    n = open(file_path, "r")

    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{OUTPUT_PATH}"):
        os.makedirs(OUTPUT_PATH)

    filename = size + "_" + OUTPUT_BASE_FILE_NAME

    i = 0
    while os.path.exists(f"{OUTPUT_PATH}{filename}.csv"):
        i += 1
        filename = f"{size}_{OUTPUT_BASE_FILE_NAME}({i})"

    f = open(f"{OUTPUT_PATH}{filename}.csv", "w")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,#Node,#Truck,Capacity,Optimal_Cost,BEST_Random,APX,Execution_time,#Iteration,Used_truck\n")

    # -----------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Clarke e Wright sull'istanza corrispondente
    for line in n:
        file_name = line.strip()
        if file_name.endswith(".vrp"):
            print(f"Solving {file_name}...")
            instance_path = INSTANCES_DIRECTORY + file_name
            instance = Parser.make_instance_from_path_name(instance_path)
            nodes, truck = Parser.work_on_instance(instance, True)
            print("Fine parsing")

            distance = Parser.get_edge_weight(instance)

            id_depots = Parser.get_depots_index(instance)[0]
            k = truck.get_min_num()
            if k is None or k == 0:
                k = truck.get_max_num()

            best_cost = float("inf")
            best_routes = []

            if TIMEOUT:
                # Registra il tempo di inizio
                start_time = time.perf_counter()
                while time.perf_counter() - start_time < TIMEOUT_VALUE:
                    routes, costs = Random.vrp_random(nodes, truck.get_capacity(), distance, id_depots)
                    if len(routes) <= k or not SKIP_SOLUTION_OUT_OF_TRUCK:  # Se il numero di veicoli usati è minore o uguale a k
                        if costs < best_cost:
                            best_cost = costs
                            best_routes = routes
                execution_time = TIMEOUT_VALUE
            else:
                # Registra il tempo di inizio
                start_time = time.perf_counter()
                for i in range(RANDOM_ITERATION_NUMBER):  # Ripeti l'algoritmo RANDOM_ITERATION_NUMBER volte
                    routes, costs = Random.vrp_random(nodes, truck.get_capacity(), distance, id_depots)
                    if len(routes) <= k or not SKIP_SOLUTION_OUT_OF_TRUCK:  # Se il numero di veicoli usati è minore o uguale a k
                        if costs < best_cost:
                            best_cost = costs
                            best_routes = routes
                # Registra il tempo di fine
                end_time = time.perf_counter()

                # Calcola la durata dell'esecuzione
                execution_time = end_time - start_time

            opt = Parser.get_optimal_cost_from_path(instance_path)
            if opt is not None:
                apx = best_cost / opt
            else:
                apx = None
            # Recupera informazioni sull'istanza: numero di nodi, numero di veicoli, capacità dei veicoli
            n_nodes = Parser.get_nodes_dimension(instance)
            n_truck = Parser.get_truck(instance).get_min_num()
            if n_truck == 0:
                n_truck = None
            capacity = Parser.get_truck(instance).get_capacity()

            # Stampa il valore ottimo affiancato al risultato dell'euristica
            print("Costo ottimo: ", opt, "| Random_best_cost:", best_cost, "|APX: ", apx, "|Tempo di esecuzione: ",
                  execution_time)
            # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
            f.write(f"{size},{file_name},{n_nodes},{n_truck},{capacity},{opt},{best_cost},{apx},"
                    f"{execution_time},{RANDOM_ITERATION_NUMBER},{len(best_routes)}\n")

    f.close()


if SMALL:
    solve_random_for_instance_name_in_file("small", f"{NAME_BY_SIZE_PATH}small_instances_name.txt")
if MID_SMALL:
    solve_random_for_instance_name_in_file("mid_small", f"{NAME_BY_SIZE_PATH}mid_small_instances_name.txt")
if MID:
    solve_random_for_instance_name_in_file("mid", f"{NAME_BY_SIZE_PATH}mid_instances_name.txt")
if MID_LARGE:
    solve_random_for_instance_name_in_file("mid_large", f"{NAME_BY_SIZE_PATH}mid_large_instances_name.txt")
if LARGE:
    solve_random_for_instance_name_in_file("large", f"{NAME_BY_SIZE_PATH}large_instances_name.txt")
if X_LARGE:
    solve_random_for_instance_name_in_file("x_large", f"{NAME_BY_SIZE_PATH}x_large_instances_name.txt")
