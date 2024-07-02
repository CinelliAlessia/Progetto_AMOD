import vrplib as vr
import os

def clarke_and_wright(customers, capacity):
    # Ottieni l'elenco di tutti i file nella directory
    files = os.listdir('vrp-all/A')
    # Ordina l'elenco dei file
    files.sort()
    # Prendi il primo file
    first_file = files[0]
    # Crea il percorso completo al file
    file_path = os.path.join('src/main/resources/[VRP]Instance[.vrp]/Vrp-All/A', first_file)
    # Carica l'istanza VRP dal file
    instance = vr.VRPInstance.read_vrp(file_path)

    # Create a new Clarke and Wright algorithm
    cw = vr.ClarkeAndWright(instance)

    # Solve the problem
    solution = cw.solve()

    # Return the solution
    return solution
