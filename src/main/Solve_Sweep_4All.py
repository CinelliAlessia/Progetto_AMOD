import time

import Sweep_Ale as sweepAle
import Sweep_Andrea as sweepAndrea
import ParseInstances as Parser
import os
from src.main import Utils
# ------------------------------------------------------------------------------------------------------------
CW_SELECTOR = 1
# Selezionando come primo parametro selector = 1, verrà eseguito l'algoritmo di Clarke e Wright di Alessia
# Selezionando come primo parametro selector = 0, verrà eseguito l'algoritmo di Clarke e Wright di Andrea
# Selezionando come primo parametro selector = 2, verrà eseguiti entrambi, con risultati nello stesso file  # todo da fare
# ------------------------------------------------------------------------------------------------------------

OUTPUT_DIRECTORY = "resources/Heuristic_Solutions/"  # Directory di output per i risultati
FILE_NAME = "Sweep_APX_and_Time.csv"  # Aggiungere come prefisso il numero del run
INSTANCES_DIRECTORY = "resources/vrplib/Instances"  # Directory delle istanze


# Esegui l'euristica di Clarke e Wright per le istanze elencate nel file_path (tramite nome), le istanze verranno
# recuperate nella directory "resources/vrplib/Instances"
def solve_sweep_for_instance_name_in_file(size, file_path):
    global FILE_NAME
    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(file_path):
        print(f"Il file {file_path} non esiste")
        return
    # Apro il file in lettura
    n = open(file_path, "r")
    # Apri un nuovo file di output per salvare i risultati
    # Prima devo vedere l'ultimo file creato e incrementare il numero
    i = 0
    while os.path.exists(f"{OUTPUT_DIRECTORY}{FILE_NAME}"):
        i += 1
        FILE_NAME = f"{size}_Sweep_APX_and_Time({i}).csv"
    f = open(f"{OUTPUT_DIRECTORY}{FILE_NAME}", "w")
    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,Optimal_Cost,Sw_cost,opt2,opt3,APX,Execution_time\n")
    # -----------------------------------------------------------------------------------------
    # Per ogni riga (riga = file_name) in n (file_path),
    # esegui l'euristica di Clarke e Wright sull'istanza corrispondente
    i = 0
    execution_time = 0
    for line in n:
        i += 1
        file_name = line.strip()
        if file_name.endswith(".vrp"):
            print(f"Solving {file_name}...")
            instance = Parser.make_instance_from_path_name(f"resources/vrplib/Instances/{file_name}")
            print("Fine parsing")
            if CW_SELECTOR == 0:  # CW Andrea
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
            else:
                nodes, truck = Parser.work_on_instance(instance)
                # Registra il tempo di inizio
                start_time = time.perf_counter()
                # Chiamata alla funzione che vuoi misurare
                routes, opt_2, opt_3 = sweepAle.sweep_algorithm(nodes, truck.get_capacity())
                # Registra il tempo di fine
                end_time = time.perf_counter()
                sw_cost = Utils.calculate_cost(routes, nodes)
                sw_cost_2 = Utils.calculate_cost(opt_2, nodes)
                sw_cost_3 = Utils.calculate_cost(opt_3, nodes)
                # Calcola la durata dell'esecuzione
                execution_time = end_time - start_time

            path = f"resources/vrplib/Instances/{file_name}"
            opt = Parser.get_optimal_cost_from_path(path)
            if opt is not None:
                apx = sw_cost_3 / opt
            else:
                apx = None
            # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli
            # Stampa il valore ottimo affiancato al risultato dell'euristica
            print("Costo ottimo: ", opt, "| CW_cost:", sw_cost_3, "|APX: ", apx, "|Tempo di esecuzione: ",
                  execution_time)
            # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
            f.write(f"{size},{file_name},{opt},{sw_cost}, {sw_cost_2},{sw_cost_3},{apx},{execution_time}\n")


# Esegui l'euristica per tutte le size delle istanze
solve_sweep_for_instance_name_in_file("small", "resources/vrplib/Name_of_instances_by_dimension/small_instances_name.txt")
#solve_cw_for_instance_name_in_file("mid_small", "resources/vrplib/Name_of_instances_by_dimension/mid_small_instances_name.txt")
#solve_cw_for_instance_name_in_file("mid", "resources/vrplib/Name_of_instances_by_dimension/mid_instances_name.txt")
#solve_cw_for_instance_name_in_file("mid_large", "resources/vrplib/Name_of_instances_by_dimension/mid_large_instances_name.txt")
#solve_cw_for_instance_name_in_file("large", "resources/vrplib/Name_of_instances_by_dimension/large_instances_name.txt")