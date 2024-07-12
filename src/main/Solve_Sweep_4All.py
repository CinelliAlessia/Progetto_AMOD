import time

import Sweep_Ale as sweepAle
import Sweep_Andrea as sweepAndrea
import ParseInstances as Parser
import os
from src.main import Utils

# ------------------------------------------------------------------------------------------------------------
SWEEP_SELECTOR = 1
# Selezionando come primo parametro selector = 1, verrà eseguito l'algoritmo di Clarke e Wright di Alessia
# Selezionando come primo parametro selector = 0, verrà eseguito l'algoritmo di Clarke e Wright di Andrea
# Selezionando come primo parametro selector = 2, verrà eseguiti entrambi, con risultati nello stesso file  # todo da fare
# ------------------------------------------------------------------------------------------------------------

OUTPUT_DIRECTORY = "../Results/Heuristic_Solutions/"  # Directory di output per i risultati
BASE_FILE_NAME = "Sweep_APX_and_Time.csv"  # Aggiungere come prefisso il numero del run
INSTANCES_DIRECTORY = "../Results/vrplib/Instances/"  # Directory delle istanze


# Esegui l'euristica di Clarke e Wright per le istanze elencate nel file_path (tramite nome), le istanze verranno
# recuperate nella directory "Results/vrplib/Instances"
def solve_sweep_for_instance_name_in_file(size, file_path):
    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(file_path):
        print(f"Il file {file_path} non esiste")
        return

    # Apro il file in lettura per leggere i nomi delle istanze separate per dimensione
    n = open(file_path, "r")

    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{OUTPUT_DIRECTORY}"):
        os.makedirs(OUTPUT_DIRECTORY)

    # Apri il file di output per salvare i risultati
    f = open(f"{OUTPUT_DIRECTORY}{BASE_FILE_NAME}", "w")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,Optimal_Cost,Sw_cost,opt2,opt3,APX,Execution_time\n")

    # -----------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Sweep sull'istanza corrispondente
    i = 0
    execution_time = 0
    for line in n:
        i += 1
        file_name = line.strip()
        if file_name.endswith(".vrp"):
            print(f"Solving {file_name}...")
            # Se istanza non euclidea, saltare l'istanza
            if Parser.get_edge_weight_type_from_path(INSTANCES_DIRECTORY+file_name) == "EXPLICIT":
                print(f"Istanza {file_name} non euclidea, saltata")
                continue
            instance = Parser.make_instance_from_path_name(INSTANCES_DIRECTORY+file_name)
            print("Fine parsing")
            if SWEEP_SELECTOR == 0:  # CW Andrea
                # Registra il tempo di inizio
                start_time = time.perf_counter()
                # Chiamata alla funzione che vuoi misurare
                sw_cost, _ = sweepAndrea.solve_sweep_on_instance(instance)
                sw_cost_2 = 0
                sw_cost_3 = 0
                # Registra il tempo di fine
                end_time = time.perf_counter()
                # Calcola la durata dell'esecuzione
                execution_time = end_time - start_time
            elif SWEEP_SELECTOR == 1:  # SWEEP Alessia

                nodes, truck = Parser.work_on_instance(instance)

                # Registra il tempo di inizio
                start_time = time.perf_counter()

                routes, opt_2, opt_3 = sweepAle.sweep_algorithm(nodes, truck.get_capacity())

                sw_cost = Utils.calculate_cost(routes, nodes)
                sw_cost_2 = Utils.calculate_cost(opt_2, nodes)
                sw_cost_3 = Utils.calculate_cost(opt_3, nodes)

                # Registra il tempo di fine
                end_time = time.perf_counter()
                # Calcola la durata dell'esecuzione
                execution_time = end_time - start_time

            path = f"../resources/vrplib/Instances/{file_name}"
            opt = Parser.get_optimal_cost_from_path(path)

            if opt is not None:
                apx = sw_cost_3 / opt
            else:
                apx = None

            # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli
            # Stampa il valore ottimo affiancato al risultato dell'euristica
            print("Costo ottimo: ", opt, "| CW_cost:", sw_cost_3, "|APX: ", apx)
            # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
            diff = sw_cost_2 - sw_cost_3
            f.write(f"{size},{file_name},{opt},{sw_cost},{sw_cost_2},{sw_cost_3},{diff},{execution_time}\n")


# Esegui l'euristica per tutte le size delle istanze
path_dim = "../resources/vrplib/Name_of_instances_by_dimension/"

SMALL = True
MID_SMALL = False
MID = False
MID_LARGE = False
LARGE = False

if SMALL:
    solve_sweep_for_instance_name_in_file("small", f"{path_dim}small_instances_name.txt")
elif MID_SMALL:
    solve_sweep_for_instance_name_in_file("mid_small", f"{path_dim}mid_small_instances_name.txt")
elif MID:
    solve_sweep_for_instance_name_in_file("mid", f"{path_dim}mid_instances_name.txt")
elif MID_LARGE:
    solve_sweep_for_instance_name_in_file("mid_large", f"{path_dim}mid_large_instances_name.txt")
elif LARGE:
    solve_sweep_for_instance_name_in_file("large", f"{path_dim}large_instances_name.txt")
