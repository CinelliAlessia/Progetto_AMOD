import time
import Sweep_Ale as sweepAle
import Sweep_Andrea as sweepAndrea
import ParseInstances as Parser
import os

# ------------------------------------------------------------------------------------------------------------
SWEEP_SELECTOR = 1
# Selezionando come primo parametro selector = 0, verrà eseguito l'algoritmo di Sweep di Andrea
# Selezionando come primo parametro selector = 1, verrà eseguito l'algoritmo di Sweep di Alessia
# Selezionando come primo parametro selector = 2, verrà eseguiti entrambi, con risultati nello stesso file  # todo da fare
# ------------------------------------------------------------------------------------------------------------

OPT_2 = False
OPT_3 = True

# Esegui l'euristica per tutte le size delle istanze
path_dim = "../resources/vrplib/Name_of_instances_by_dimension/"

SMALL = True
MID_SMALL = True
MID = False
MID_LARGE = False
LARGE = False
X_LARGE = False


OUTPUT_DIRECTORY = "Results/Heuristic_Solutions/"  # Directory di output per i risultati
BASE_FILE_NAME = "Sweep_APX_and_Time.csv"  # Aggiungere come prefisso il numero del run
INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"  # Directory delle istanze


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

    output_directory = OUTPUT_DIRECTORY + calculate_directory() + "/"

    # Verifico che la directory di output esista, altrimenti la creo
    if not os.path.exists(f"{output_directory}"):
        os.makedirs(output_directory)

    name_file = calculate_FileName(size)

    # Apri il file di output per salvare i risultati
    f = open(f"{output_directory}{name_file}", "w")

    # Scrivi nel file l'intestazione
    f.write("Size,Instance_Name,Optimal_Cost,Cost_NoOpt,Apx,Execution_time_NoOpt\n")

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

        if SWEEP_SELECTOR == 0:  # CW Andrea
            # Chiamata alla funzione che vuoi misurare
            costs, routes = sweepAndrea.solve_sweep_on_instance(instance)

        elif SWEEP_SELECTOR == 1:  # SWEEP Alessia

            nodes, truck = Parser.work_on_instance(instance, False)
            routes, costs = sweepAle.sweep_algorithm(nodes, truck.get_capacity(), OPT_2, OPT_3)

        print("Costo Sweep: ", costs)

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


def calculate_FileName(size):
    if OPT_2:
        name = "2_opt_"
    elif OPT_3:
        name = "3_opt_"
    else:
        name = "no_opt_"

    filename = size + "_" + name + BASE_FILE_NAME
    return filename


def calculate_directory():
    if OPT_2:
        name = "2_OPT"
    elif OPT_3:
        name = "3_OPT"
    else:
        name = "NO_OPT"
    return name


def add_column():
    # Aggiungere una colonna al file di output
    pass

    # import csv
    #
    # # Percorso del file CSV originale
    # file_path = 'percorso/del/tuo/file.csv'
    # # Percorso del file CSV modificato (può essere lo stesso del file originale per sovrascriverlo)
    # new_file_path = 'percorso/del/tuo/file_modificato.csv'
    #
    # # Leggi il contenuto del file CSV originale
    # with open(file_path, mode='r', newline='') as file:
    #     reader = csv.reader(file)
    #     # Converti il lettore CSV in una lista di righe
    #     rows = list(reader)
    #     # Aggiungi l'intestazione della nuova colonna alla prima riga
    #     rows[0].append('NuovaColonna')
    #
    #     # Aggiungi i valori della nuova colonna alle altre righe
    #     for row in rows[1:]:
    #         row.append('ValoreNuovaColonna')  # Sostituisci 'ValoreNuovaColonna' con il valore effettivo
    #
    # # Scrivi i dati modificati nel nuovo file CSV
    # with open(new_file_path, mode='w', newline='') as new_file:
    #     writer = csv.writer(new_file)
    #     writer.writerows(rows)

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