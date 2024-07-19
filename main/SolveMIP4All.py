import time
import os
import pandas as pd
import ParseInstances as Parser
import Config
from Gurobi_Model import solve_vrp_with_gurobi
# ------------------------------------------------------------------------------------------------------------
# Configurazioni
OUTPUT_BASE_FILE_NAME = "MIP_APX_and_Time"  # Nome base del file di output
MAX_TIME_SECONDS = 300  # Tempo massimo di esecuzione in secondi (Sovrascrive quello di default del MIP che è 300)
GAP = 0.0001
INTEGRALITY_FOCUS = 1
# ------------------------------------------------------------------------------------------------------------

# Determina i percorsi in base alla variabile ACTION
if Config.ACTION_MIP:
    NAME_BY_SIZE_PATH = "./resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "./main/Results/MIP_Solutions/"
    INSTANCES_DIRECTORY = "./resources/vrplib/Instances/"
else:
    NAME_BY_SIZE_PATH = "../resources/vrplib/Name_of_instances_by_dimension/"
    OUTPUT_PATH = "Results/MIP_Solutions/"
    INSTANCES_DIRECTORY = "../resources/vrplib/Instances/"

# Esegui per le diverse dimensioni delle istanze
SMALL = True
MID_SMALL = False
MID = False
MID_LARGE = False
LARGE = False
X_LARGE = False


def solve_vrp_for_instance_names_in_file(size, file_path):
    """
    Esegui la risoluzione del VRP per le istanze elencate nel file_path e salva i risultati.
    """
    print(f"Starting solving for {size} instances")

    if not os.path.exists(file_path):
        print(f"Il file {file_path} non esiste")
        return

    # Crea la directory di output se non esiste
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    # Determina il nome del file di output
    filename = size + "_" + OUTPUT_BASE_FILE_NAME
    i = 0
    while os.path.exists(f"{OUTPUT_PATH}{filename}.csv"):
        i += 1
        filename = f"{size}_{OUTPUT_BASE_FILE_NAME}({i})"

    # Apre il file di output in modalità scrittura
    with open(f"{OUTPUT_PATH}{filename}.csv", "w") as f:
        # Scrivi l'intestazione nel file di output
        f.write("Size,Instance_Name,#Node,#Truck,Capacity,Optimal_Cost,MIP,APX,Execution_time,Status\n")

    # Leggi il file contenente i nomi delle istanze e risolvi il problema per ogni istanza
    with open(file_path, "r") as n:
        for line in n:
            file_name = line.strip()
            with open(f"{OUTPUT_PATH}{filename}.csv", "w") as f:
                if file_name.endswith(".vrp"):
                    print(f"Solving {file_name}...")

                    # Prepara l'istanza
                    instance = Parser.make_instance_from_path_name(f"{INSTANCES_DIRECTORY}{file_name}")

                    # Esegui la risoluzione del problema
                    routes, total_cost, execution_time, status = solve_vrp_with_gurobi(instance,True, MAX_TIME_SECONDS)

                    # Ottieni il costo ottimo
                    path = INSTANCES_DIRECTORY + file_name
                    opt = Parser.get_optimal_cost_from_path(path)

                    # Calcola l'APX
                    apx = total_cost / opt if opt is not None else None
                    n_nodes = Parser.get_nodes_dimension(instance)
                    n_truck = Parser.get_truck(instance).get_min_num()
                    if n_truck == 0:
                        n_truck = None
                    capacity = Parser.get_truck(instance).get_capacity()

                    print(f"Costo ottimo: {opt} | VRP_cost: {total_cost} | APX: {apx} | Tempo di esecuzione: {execution_time} | Stato: {status}")

                    # Scrivi i risultati nel file di output
                    f.write(f"{size},{file_name},{n_nodes},{n_truck},{capacity},{opt},{total_cost},{apx},{execution_time},"
                            f"{status}\n")
                    f.close()

    print(f"Finished solving for {size} instances")


if SMALL:
    solve_vrp_for_instance_names_in_file("small", f"{NAME_BY_SIZE_PATH}small_instances_name.txt")
if MID_SMALL:
    solve_vrp_for_instance_names_in_file("mid_small", f"{NAME_BY_SIZE_PATH}mid_small_instances_name.txt")
if MID:
    solve_vrp_for_instance_names_in_file("mid", f"{NAME_BY_SIZE_PATH}mid_instances_name.txt")
if MID_LARGE:
    solve_vrp_for_instance_names_in_file("mid_large", f"{NAME_BY_SIZE_PATH}mid_large_instances_name.txt")
if LARGE:
    solve_vrp_for_instance_names_in_file("large", f"{NAME_BY_SIZE_PATH}large_instances_name.txt")
if X_LARGE:
    solve_vrp_for_instance_names_in_file("x_large", f"{NAME_BY_SIZE_PATH}x_large_instances_name.txt")