import time

import Clarke_Wright_Andrea as CwAndre
import Clarke_Wright_Alessia as CwAle
import ParseInstances as Parser
import os
from src.main import Utils
# ------------------------------------------------------------------------------------------------------------
CW_SELECTOR = 0
# Selezionando come primo parametro selector = 0, verrà eseguito l'algoritmo di Clarke e Wright di Andrea
# Selezionando come primo parametro selector = 1, verrà eseguito l'algoritmo di Clarke e Wright di Alessia
# Selezionando come primo parametro selector = 2, verrà eseguiti entrambi, con risultati nello stesso file  # todo da fare
# ------------------------------------------------------------------------------------------------------------

OUTPUT_DIRECTORY = "Results/Heuristic_Solutions/"  # Directory di output per i risultati
BASE_FILE_NAME = "CW_APX_and_Time.csv"  # Aggiungere come prefisso il numero del run
INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze

# Directory dei file contenenti i nomi delle istanze
SIZE_BY_BAME_DIR = "../resources/vrplib/Name_of_instances_by_dimension/"

# Se impostati a True, eseguirà l'euristica di Clarke e Wright per le istanze di quel tipo
SMALL = True
MID_SMALL = False
MID = False
MID_LARGE = False
LARGE = False
X_LARGE = False


# Esegui l'euristica di Clarke e Wright per le istanze elencate nel file_path (tramite nome), le istanze verranno
# recuperate nella directory "Results/vrplib/Instances"
def solve_cw_for_instance_name_in_file(size, file_path):
    global BASE_FILE_NAME
    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(file_path):
        print("Il file non esiste")
        return
    # Apro il file in lettura
    n = open(file_path, "r")
    # Apri un nuovo file di output per salvare i risultati
    # Prima devo vedere l'ultimo file creato e incrementare il numero
    i = 0
    while os.path.exists(f"{OUTPUT_DIRECTORY}{BASE_FILE_NAME}"):
        i += 1
        BASE_FILE_NAME = f"{size}_CW_APX_and_Time({i}).csv"
    f = open(f"{OUTPUT_DIRECTORY}{BASE_FILE_NAME}", "w")
    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,Optimal_Cost,CW_cost,APX,Execution_time\n")
    # -----------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Clarke e Wright sull'istanza corrispondente
    i = 0
    cw_cost = 0
    execution_time = 0
    for line in n:
        i += 1
        file_name = line.strip()
        if file_name.endswith(".vrp"):
            print(f"Solving {file_name}...")
            instance = Parser.make_instance_from_path_name(f"../resources/vrplib/Instances/{file_name}")
            print("Fine parsing")
            if CW_SELECTOR == 0:  # CW Andrea
                # Registra il tempo di inizio
                start_time = time.perf_counter()
                # Chiamata alla funzione che vuoi misurare
                cw_cost, _ = CwAndre.solve_clarke_and_wright_on_instance(instance)
                # Registra il tempo di fine
                end_time = time.perf_counter()
                # Calcola la durata dell'esecuzione
                execution_time = end_time - start_time
            elif CW_SELECTOR == 1:  # CW Alessia
                nodes, truck = Parser.work_on_instance(instance)
                # Registra il tempo di inizio
                start_time = time.perf_counter()
                # Chiamata alla funzione che vuoi misurare
                routes = CwAle.start(nodes, truck)
                # Registra il tempo di fine
                end_time = time.perf_counter()
                cw_cost = Utils.calculate_cost(routes, nodes)

                # Calcola la durata dell'esecuzione
                execution_time = end_time - start_time

            path = INSTANCES_DIRECTORY + file_name
            opt = Parser.get_optimal_cost_from_path(path)
            if opt is not None:
                apx = cw_cost / opt
            else:
                apx = None
            # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli
            # Stampa il valore ottimo affiancato al risultato dell'euristica
            print("Costo ottimo: ", opt, "| CW_cost:", cw_cost, "|APX: ", apx, "|Tempo di esecuzione: ",
                  execution_time)
            # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
            f.write(f"{size},{file_name},{opt},{cw_cost},{apx},{execution_time}\n")


if SMALL:
    solve_cw_for_instance_name_in_file("small", f"{SIZE_BY_BAME_DIR}small_instances_name.txt")
elif MID_SMALL:
    solve_cw_for_instance_name_in_file("mid_small", f"{SIZE_BY_BAME_DIR}mid_small_instances_name.txt")
elif MID:
    solve_cw_for_instance_name_in_file("mid", f"{SIZE_BY_BAME_DIR}mid_instances_name.txt")
elif MID_LARGE:
    solve_cw_for_instance_name_in_file("mid_large", f"{SIZE_BY_BAME_DIR}mid_large_instances_name.txt")
elif LARGE:
    solve_cw_for_instance_name_in_file("large", f"{SIZE_BY_BAME_DIR}large_instances_name.txt")
elif X_LARGE:
    solve_cw_for_instance_name_in_file("x_large", f"{SIZE_BY_BAME_DIR}x_large_instances_name.txt")