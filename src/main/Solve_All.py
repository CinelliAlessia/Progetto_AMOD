import time
import Sweep_Ale as sweepAle
import Sweep_Andrea as sweepAndrea
import ParseInstances as Parser
import os

# TODO: ATTENZIONE NON FUNZIONAAAAAA

# ------------------------------------------------------------------------------------------------------------
SWEEP_SELECTOR = 0
RANDOM_SELECTOR = 0
CW_SELECTOR = 0
OPT_SELECTOR = 0
# Selezionando selector = 0, l'algoritmo non verrà eseguito
# Selezionando selector = 1, l'algoritmo verrà eseguito
# ------------------------------------------------------------------------------------------------------------


# Esegui l'euristica per tutte le size delle istanze
path_dim = "../resources/vrplib/Name_of_instances_by_dimension/"

SMALL = True
MID_SMALL = True
MID = True
MID_LARGE = True
LARGE = True
X_LARGE = True


OUTPUT_DIRECTORY = "Results/Heuristic_Solutions/"  # Directory di output per i risultati
BASE_FILE_NAME = "APX_and_Time.csv"  # Aggiungere come prefisso il numero del run
INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze


# Esegui l'euristica di Sweep per le istanze elencate nel file_path (tramite nome), le istanze verranno
# recuperate nella directory "Results/vrplib/Instances"
def solve_for_instance_name_in_file(size, file_path):
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

    # Apri il file di output per salvare i risultati
    f = open(f"{OUTPUT_DIRECTORY}{size}-{BASE_FILE_NAME}", "w")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,Optimal_Cost,Costs,Apx,Execution_time\n")

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

        # Registra il tempo di inizio
        start_time = time.perf_counter()

        if CW_SELECTOR == 1:  # CW Andrea
            # Chiamata alla funzione che vuoi misurare
            costs, routes = sweepAndrea.solve_sweep_on_instance(instance)

        elif SWEEP_SELECTOR == 1:  # SWEEP Alessia

            nodes, truck = Parser.work_on_instance(instance, False)
            routes, costs = sweepAle.sweep_algorithm(nodes, truck.get_capacity())

        elif RANDOM_SELECTOR == 1:
            pass

        # Registra il tempo di fine
        end_time = time.perf_counter()
        # Calcola la durata dell'esecuzione
        execution_time = end_time - start_time

        opt = Parser.get_optimal_cost_from_path(INSTANCES_DIRECTORY + file_name)

        if opt is not None:
            apx = costs / opt
        else:
            apx = None

        # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli
        print("Costo ottimo: ", opt, "| CW_cost:", costs, "|APX: ", apx)
        # Salva tali valori, con lo stesso formato su una nuova riga del file APX_and_Time.txt
        f.write(f"{size},{file_name},{opt},{costs},{apx},{execution_time}\n")


if SMALL:
    solve_for_instance_name_in_file("small", f"{path_dim}small_instances_name.txt")
if MID_SMALL:
    solve_for_instance_name_in_file("mid_small", f"{path_dim}mid_small_instances_name.txt")
if MID:
    solve_for_instance_name_in_file("mid", f"{path_dim}mid_instances_name.txt")
if MID_LARGE:
    solve_for_instance_name_in_file("mid_large", f"{path_dim}mid_large_instances_name.txt")
if LARGE:
    solve_for_instance_name_in_file("large", f"{path_dim}large_instances_name.txt")
if X_LARGE:
    solve_for_instance_name_in_file("x_large", f"{path_dim}x_large_instances_name.txt")