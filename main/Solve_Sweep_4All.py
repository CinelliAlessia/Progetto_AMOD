import time

import Config
import Sweep_Ale as sweepAle
import ParseInstances as Parser
import os

# ------------------------------------------------------------------------------------------------------------
SWEEP_SELECTOR = 1
# Selezionando come primo parametro selector = 0, verrà eseguito l'algoritmo di Sweep di Andrea
# Selezionando come primo parametro selector = 1, verrà eseguito l'algoritmo di Sweep di Alessia
# ------------------------------------------------------------------------------------------------------------

SMALL = False
MID_SMALL = False
MID = True
MID_LARGE = False
LARGE = False
X_LARGE = False

# ------------------------------------------------------------------------------------------------------------

OPT_2 = True
OPT_3 = True

# ------------------------------------------------------------------------------------------------------------

ACTIONS = Config.ACTION_SWEEP  # Impostare a True se si sta eseguendo il codice dalle github Actions, False se in locale

if ACTIONS:
    # Esegui l'euristica per tutte le size delle istanze GITHUB ACTION
    NAME_BY_SIZE_PATH = "./resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "./main/Results/Heuristic_Solutions/Sweep/"  # Directory di output per i risultati
    INSTANCES_DIRECTORY = "./resources/vrplib/Instances/"  # Directory delle istanze
else:
    NAME_BY_SIZE_PATH = "../resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "Results/Heuristic_Solutions/Sweep/"  # Directory di output per i risultati
    INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze

OUTPUT_BASE_FILE_NAME = "Sweep_APX_and_Time"  # Aggiungere come prefisso il numero del run


# Esegui l'euristica di Sweep per le istanze elencate nel file_path (tramite nome), le istanze verranno
# recuperate nella directory "Results/vrplib/Instances"
def solve_sweep_for_instance_name_in_file(size, file_path):
    """
    Esegui l'euristica di Sweep per le istanze elencate nel file_path (tramite nome)
    :param size: nome della dimensione delle istanze
    :param file_path: path del file contenente i nomi delle istanze
    :return:
    """

    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(file_path):
        print(f"Il file {file_path} non esiste")
        return

    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{OUTPUT_PATH}"):
        os.makedirs(OUTPUT_PATH)

    # Creo il file di output
    filename = size + "_" + OUTPUT_BASE_FILE_NAME
    i = 0
    while os.path.exists(f"{OUTPUT_PATH}{filename}.csv"):
        i += 1
        filename = f"{size}_{OUTPUT_BASE_FILE_NAME}({i})"
    f = open(f"{OUTPUT_PATH}{filename}.csv", "w")

    # Intestazione del file csv
    f.write("Size,Instance_Name,#Node,#Truck,Capacity,Optimal_Cost,Cost_NoOpt,Apx_NoOpt,Execution_time_NoOpt,Cost_2Opt,Apx_2Opt,Execution_time_2Opt,Cost_3Opt,Apx_3Opt,Execution_time_3Opt,#Truck_Opt3\n")

    # -----------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Sweep sull'istanza corrispondente

    # Apro il file .txt in lettura per leggere i nomi delle istanze separate per dimensione
    n = open(file_path, "r")

    for line in n:  # Per ogni istanza scritta nel file
        calculate_sweep_and_write_in_csv(line, f, size)


def calculate_sweep_and_write_in_csv(line, f, size):
    file_name = line.strip()
    if file_name.endswith(".vrp"):
        print(f"Solving {file_name}...")
        # Se istanza non euclidea, saltare l'istanza
        if Parser.get_edge_weight_type_from_path(INSTANCES_DIRECTORY+file_name) == "EXPLICIT":
            print(f"Istanza {file_name} non euclidea, saltata")
            return
        instance = Parser.make_instance_from_path_name(INSTANCES_DIRECTORY+file_name)
        print("Fine parsing")

        nodes, truck = Parser.work_on_instance(instance, False)

        # ----- Calcolo Sweep NoOpt -----

        start_time_no_opt = time.perf_counter()     # Registra il tempo di inizio
        routes_no_opt, costs_no_opt = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), False, False)
        end_time_no_opt = time.perf_counter()      # Registra il tempo di fine
        execution_time_no_opt = end_time_no_opt - start_time_no_opt     # Calcola la durata dell'esecuzione

        # ----- Calcolo Sweep 2Opt -----

        start_time_2_opt = time.perf_counter()    # Registra il tempo di inizio
        routes_2_opt, costs_2_opt = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), OPT_2, False)
        end_time_2_opt = time.perf_counter()   # Registra il tempo di fine
        execution_time_2_opt = end_time_2_opt - start_time_2_opt   # Calcola la durata dell'esecuzione

        # ----- Calcolo Sweep 3Opt -----

        start_time_3_opt = time.perf_counter()   # Registra il tempo di inizio
        routes_3_opt, costs_3_opt = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), False, OPT_3)
        end_time_3_opt = time.perf_counter()    # Registra il tempo di fine
        execution_time_3_opt = end_time_3_opt - start_time_3_opt

        # Scrittura dei risultati nel file csv

        path = INSTANCES_DIRECTORY + file_name
        opt = Parser.get_optimal_cost_from_path(path)

        if opt is not None:
            apx_no_opt = costs_no_opt / opt
            apx_2_opt = costs_2_opt / opt
            apx_3_opt = costs_3_opt / opt
        else:
            apx_no_opt = None
            apx_2_opt = None
            apx_3_opt = None

        # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli

        capacity = Parser.get_truck(instance).get_capacity()
        n_nodes = Parser.get_nodes_dimension(instance)
        n_truck = Parser.get_truck(instance).get_min_num()
        if n_truck == 0:
            n_truck = None

        # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
        f.write(f"{size},{file_name},{n_nodes},{n_truck},{capacity},{opt},{costs_no_opt},{apx_no_opt},{execution_time_no_opt},{costs_2_opt},{apx_2_opt},{execution_time_2_opt},{costs_3_opt},{apx_3_opt},{execution_time_3_opt},{len(routes_3_opt)}\n")


if SMALL:
    solve_sweep_for_instance_name_in_file("small", f"{NAME_BY_SIZE_PATH}small_instances_name.txt")
if MID_SMALL:
    solve_sweep_for_instance_name_in_file("mid_small", f"{NAME_BY_SIZE_PATH}mid_small_instances_name.txt")
if MID:
    solve_sweep_for_instance_name_in_file("mid", f"{NAME_BY_SIZE_PATH}mid_instances_name.txt")
if MID_LARGE:
    solve_sweep_for_instance_name_in_file("mid_large", f"{NAME_BY_SIZE_PATH}mid_large_instances_name.txt")
if LARGE:
    solve_sweep_for_instance_name_in_file("large", f"{NAME_BY_SIZE_PATH}large_instances_name.txt")
if X_LARGE:
    solve_sweep_for_instance_name_in_file("x_large", f"{NAME_BY_SIZE_PATH}x_large_instances_name.txt")
