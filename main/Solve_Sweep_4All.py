import time
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
MID = False
MID_LARGE = False
LARGE = True
X_LARGE = False

# Esegui l'euristica per tutte le size delle istanze GITHUB ACTION
path_dim = "./resources/vrplib/Name_of_instances_by_dimension/"
OUTPUT_DIRECTORY = "./main/Results/Heuristic_Solutions/Sweep/"  # Directory di output per i risultati
BASE_FILE_NAME = "Sweep_APX_and_Time.csv"  # Aggiungere come prefisso il numero del run
INSTANCES_DIRECTORY = "./resources/vrplib/Instances/"  # Directory delle istanze

#path_dim = "../resources/vrplib/Name_of_instances_by_dimension/"
#OUTPUT_DIRECTORY = "Results/Heuristic_Solutions/Sweep/"  # Directory di output per i risultati
#BASE_FILE_NAME = "Sweep_APX_and_Time"  # Aggiungere come prefisso il numero del run
#INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze


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
        # todo CHIAMA il programma che genera i file con i nomi delle istanze
        return

    # Apro il file in lettura per leggere i nomi delle istanze separate per dimensione
    n = open(file_path, "r")

    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{OUTPUT_DIRECTORY}"):
        os.makedirs(OUTPUT_DIRECTORY)

    filename = size + "_" + BASE_FILE_NAME

    i = 0
    while os.path.exists(f"{OUTPUT_DIRECTORY}{filename + ".csv"}"):
        i += 1
        filename = f"{filename}({i})"
    f = open(f"{OUTPUT_DIRECTORY}{filename + ".csv"}", "w")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,#Node,#Truck,Capacity,Optimal_Cost,Cost_NoOpt,Apx_NoOpt,Execution_time_NoOpt,Cost_2Opt,Apx_2Opt,Execution_time_2Opt,Cost_3Opt,Apx_3Opt,Execution_time_3Opt\n")

    # -----------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Sweep sull'istanza corrispondente
    for line in n:  # Per ogni istanza scritta nel file
        write_in_csv(line, f, size)


def write_in_csv(line, f, size):
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
        opt = Parser.get_optimal_cost_from_path(INSTANCES_DIRECTORY + file_name)

        # ----- Calcolo Sweep NoOpt -----

        # Registra il tempo di inizio
        start_time_NoOpt = time.perf_counter()

        routes_NoOpt, costs_NoOpt = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), False, False)

        # Registra il tempo di fine
        end_time_NoOpt = time.perf_counter()

        # Calcola la durata dell'esecuzione
        execution_time_NoOpt = end_time_NoOpt - start_time_NoOpt

        # ----- Calcolo Sweep 2Opt -----

        # Registra il tempo di inizio
        start_time_2Opt = time.perf_counter()

        routes_2Opt, costs_2Opt = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), True, False)

        # Registra il tempo di fine
        end_time_2Opt = time.perf_counter()

        # Calcola la durata dell'esecuzione
        execution_time_2Opt = end_time_2Opt - start_time_2Opt

        # ----- Calcolo Sweep 3Opt -----

        # Registra il tempo di inizio
        start_time_3Opt = time.perf_counter()

        routes_3Opt, costs_3Opt = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), False, True)

        # Registra il tempo di fine
        end_time_3Opt = time.perf_counter()

        # Calcola la durata dell'esecuzione
        execution_time_3Opt = end_time_3Opt - start_time_3Opt

        if opt is not None:
            apx_NoOpt = costs_NoOpt / opt
            apx_2Opt = costs_2Opt / opt
            apx_3Opt = costs_3Opt / opt
        else:
            apx_NoOpt = None
            apx_2Opt = None
            apx_3Opt = None

        # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli

        n_nodes = Parser.get_nodes_dimension(instance)
        n_truck = Parser.get_truck(instance).get_min_num()
        if n_truck == 0:
            n_truck = None
        capacity = Parser.get_truck(instance).get_capacity()

        # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
        f.write(f"{size},{file_name},{n_nodes},{n_truck},{capacity},{opt},{costs_NoOpt},{apx_NoOpt},{execution_time_NoOpt},{costs_2Opt},{apx_2Opt},{execution_time_2Opt},{costs_3Opt},{apx_3Opt},{execution_time_3Opt}\n")


if SMALL:
    solve_sweep_for_instance_name_in_file("small", f"{path_dim}small_instances_name.txt")
if MID_SMALL:
    solve_sweep_for_instance_name_in_file("mid_small", f"{path_dim}mid_small_instances_name.txt")
if MID:
    solve_sweep_for_instance_name_in_file("mid", f"{path_dim}mid_instances_name.txt")
if MID_LARGE:
    solve_sweep_for_instance_name_in_file("mid_large", f"{path_dim}mid_large_instances_name.txt")
if LARGE:
    solve_sweep_for_instance_name_in_file("large", f"{path_dim}large_instances_name.txt")
if X_LARGE:
    solve_sweep_for_instance_name_in_file("x_large", f"{path_dim}x_large_instances_name.txt")