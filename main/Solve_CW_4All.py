import time

import Clarke_Wright_Andrea as CwAndre
import Clarke_Wright_Alessia as CwAle
import ParseInstances as Parser
import os
import Utils

# ------------------------------------------------------------------------------------------------------------
CW_SELECTOR = 0
# Selezionando come primo parametro selector = 0, verrà eseguito l'algoritmo di Clarke e Wright di Andrea
# Selezionando come primo parametro selector = 1, verrà eseguito l'algoritmo di Clarke e Wright di Alessia
# ------------------------------------------------------------------------------------------------------------
OUTPUT_BASE_FILE_NAME = "CW_APX_and_Time"  # Nome base del file di output, verranno aggiunti prefisso e suffisso
# ------------------------------------------------------------------------------------------------------------
ACTIONS = True  # Impostare a True se si sta eseguendo il codice dalle github Actions, False se in locale

if ACTIONS:
    # Directory dei file contenenti i nomi delle istanze
    NAME_BY_SIZE_PATH = "./resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "./main/Results/Heuristic_Solutions/Clarke_&_Wright_run/"  # Directory di output per i risultati
    INSTANCES_DIRECTORY = "./resources/vrplib/Instances/"  # Directory delle istanze
else:
    # Directory dei file contenenti i nomi delle istanze
    NAME_BY_SIZE_PATH = "../resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "Results/Heuristic_Solutions/Clarke_&_Wright_run/"  # Directory di output per i risultati
    INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze

# ------------------------------------------------------------------------------------------------------------
# Se impostati a True, eseguirà l'euristica di Clarke e Wright per le istanze di quel tipo
SMALL = False
MID_SMALL = False
MID = False
MID_LARGE = False
LARGE = False
X_LARGE = True
# ------------------------------------------------------------------------------------------------------------


def solve_cw_for_instance_name_in_file(size, file_path):
    """
    Esegui l'euristica di Clarke e Wright per le istanze elencate nel file_path (tramite nome), le istanze verranno
    :param size: nome della dimensione delle istanze
    :param file_path: path del file contenente i nomi delle istanze
    :return:
    """
    print(f"Starting solving for {size} instances")

    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(file_path):
        print(f"Il file {file_path} non esiste")
        return

    # Apro il file in lettura per leggere i nomi delle istanze separate per dimensione
    n = open(file_path, "r")

    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{OUTPUT_PATH}"):
        os.makedirs(OUTPUT_PATH)

    # Apri un nuovo file di output per salvare i risultati
    # Prima devo vedere l'ultimo file creato e incrementare il numero
    filename = size + "_" + OUTPUT_BASE_FILE_NAME

    i = 0
    while os.path.exists(f"{OUTPUT_PATH}{filename}.csv"):
        i += 1
        filename = f"{size}_{OUTPUT_BASE_FILE_NAME}({i})"

    f = open(f"{OUTPUT_PATH}{filename}.csv", "w")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,#Node,#Truck,Capacity,Optimal_Cost,CW_cost,APX,Execution_time,Status\n")

    # ----------------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Clarke e Wright sull'istanza corrispondente
    cw_cost = 0
    execution_time = 0
    status = "Finished"
    for line in n:
        file_name = line.strip()
        if file_name.endswith(".vrp"):
            print(f"Solving {file_name}...")

            instance = Parser.make_instance_from_path_name(f"{INSTANCES_DIRECTORY}{file_name}")
            print("Fine parsing")
            if CW_SELECTOR == 0:  # CW Andrea

                start_time = time.perf_counter()    # Registra il tempo di inizio
                cw_cost, _, status = CwAndre.solve_clarke_and_wright_on_instance(instance)
                end_time = time.perf_counter()  # Registra il tempo di fine
                execution_time = end_time - start_time  # Calcola la durata dell'esecuzione

            elif CW_SELECTOR == 1:  # CW Alessia
                nodes, truck = Parser.work_on_instance(instance, True)
                start_time = time.perf_counter()    # Registra il tempo di inizio
                routes = CwAle.start(nodes, truck)
                cw_cost = Utils.calculate_cost(routes, nodes)
                end_time = time.perf_counter()  # Registra il tempo di fine
                execution_time = end_time - start_time  # Calcola la durata dell'esecuzione

            path = INSTANCES_DIRECTORY + file_name
            opt = Parser.get_optimal_cost_from_path(path)

            if opt is not None:
                apx = cw_cost / opt
            else:
                apx = None
            # Recupera informazioni sull'istanza: numero di nodi, numero di veicoli, capacità dei veicoli
            n_nodes = Parser.get_nodes_dimension(instance)
            n_truck = Parser.get_truck(instance).get_min_num()
            if n_truck == 0:
                n_truck = None
            capacity = Parser.get_truck(instance).get_capacity()
            # Stampa il valore ottimo affiancato al risultato dell'euristica
            print("Costo ottimo: ", opt, "| CW_cost:", cw_cost, "| APX: ", apx, "| Tempo di esecuzione: ",
                  execution_time, "Stato", status)
            # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
            f.write(f"{size},{file_name},{n_nodes},{n_truck},{capacity},{opt},{cw_cost},{apx},{execution_time},"
                    f"{status}\n")
    print(f"Finished solving for {size} instances")
    f.close()


if SMALL:
    solve_cw_for_instance_name_in_file("small", f"{NAME_BY_SIZE_PATH}small_instances_name.txt")
if MID_SMALL:
    solve_cw_for_instance_name_in_file("mid_small", f"{NAME_BY_SIZE_PATH}mid_small_instances_name.txt")
if MID:
    solve_cw_for_instance_name_in_file("mid", f"{NAME_BY_SIZE_PATH}mid_instances_name.txt")
if MID_LARGE:
    solve_cw_for_instance_name_in_file("mid_large", f"{NAME_BY_SIZE_PATH}mid_large_instances_name.txt")
if LARGE:
    solve_cw_for_instance_name_in_file("large", f"{NAME_BY_SIZE_PATH}large_instances_name.txt")
if X_LARGE:
    solve_cw_for_instance_name_in_file("x_large", f"{NAME_BY_SIZE_PATH}x_large_instances_name.txt")
