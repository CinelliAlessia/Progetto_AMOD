import time

import Clarke_Wright_Andrea as Cw
import ParseInstances as Parser
import os


# ----------- Assicurarsi che il parametro SAVE_SOLUTION_ON_FILE sia True sul file Clarke_Wright_Andrea ------------
# In questo file vengono recuperate tutte le istanze di vrp ed eseguire l'euristica di Clarke e Wright.
# È utilizzata la classe Clarke_Wright_Andrea.py per eseguire l'euristica.
def solve_cw_4all():
    # Apri file di output
    f = open("resources/Heuristic_Solutions/CW_APX_and_Time.csv", "w")
    x_large = open("resources/vrplib/Name_of_instances_by_dimension/x_large_instances_name.txt", "r")
    x_large_names = x_large.read().split("\n")
    # Per ogni file nella directory "resources/vrplib/Instances"
    i = 0
    for file in os.listdir("resources/vrplib/Instances"):
        i += 1
        if file.endswith(".vrp"):
            # Escludi dal calcolo le istanze di size x-large
            if file in x_large_names:
                continue
            print(f"Solving {file}...")
            instance = Parser.make_instance_from_path_name(f"resources/vrplib/Instances/{file}")
            print("Fine parsing")

            # Esegui l'euristica di Clarke e Wright
            # Registra il tempo di inizio
            start_time = time.time()
            # Chiamata alla funzione che vuoi misurare
            cw_cost, _ = Cw.solve_clarke_and_wright_on_instance(instance)
            # Registra il tempo di fine
            end_time = time.time()
            # Calcola la durata dell'esecuzione
            execution_time = end_time - start_time

            path = f"resources/vrplib/Instances/{file}"
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
            f.write(f"{file},{opt},{cw_cost},{apx},{execution_time}\n")


# Esegui l'euristica per tutte le istanze
solve_cw_4all()
