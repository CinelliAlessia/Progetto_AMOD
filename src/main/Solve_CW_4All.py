import time

import Clarke_Wright_Andrea as Cw
import ParseInstances as Parser
import os


# In questo file vengono recuperate tutte le istanze di vrp ed eseguire l'euristica di Clarke e Wright.
# È utilizzata la classe Clarke_Wright_Andrea.py per eseguire l'euristica.
def solve_cw_4all():
    # Per ogni file nella directory "resources/vrplib/Instances"
    i = 0
    for file in os.listdir("resources/vrplib/Instances"):
        i += 1
        if file.endswith(".vrp"):
            path = os.path.join("resources/vrplib/Instances", file)
            print(f"Solving {file}...")
            opt = Parser.get_optimal_cost_from_path(path)
            # Esegui l'euristica di Clarke e Wright

            # Registra il tempo di inizio
            start_time = time.time()
            # Chiamata alla funzione che vuoi misurare
            cw_cost, _ = Cw.solve_clarke_and_wright(path)
            # Registra il tempo di fine
            end_time = time.time()

            # Calcola la durata dell'esecuzione
            execution_time = end_time - start_time
            print(f"Tempo di esecuzione: {execution_time} secondi")

            # Stampa informazioni sull'istanza: nome, numero di nodi, numero di veicoli
            # Stampa il valore ottimo affiancato al risultato dell'euristica
            print("#Nodi: TROVARE MODO", )
            print("Costo ottimo: ", opt, "| CW_cost:", cw_cost)
            # Mi fermo per ora ai primi 10 file
            if i == 10:
                break


# Esegui l'euristica per tutte le istanze
solve_cw_4all()
