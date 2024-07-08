import os


# Scorre tutti i file nella directory delle istanze e cerca le istanze di tipo MDVRP (Multi Depot VRP)
# Restituisce una lista con i nomi dei file delle istanze MDVRP e il numero di istanze trovate
def found_mdvrp_instances(directory_path="resources/vrplib/Instances"):
    mdvrp_file = []
    file_count = 0
    mdvrp_count = 0
    for file in os.listdir(directory_path):
        if file.endswith(".vrp"):
            file_count += 1
            with open(os.path.join(directory_path, file), "r") as f:
                content = f.read()
                if 'DEPOT_SECTION' in content:
                    depot_section = content.split('DEPOT_SECTION')[1].split('EOF')[0]
                    depots = depot_section.strip().split('\n')
                    print(depots)
                    if len(depots) > 1:
                        #print(depots)
                        mdvrp_file.append(file)
                        mdvrp_count += 1
    print(f"Trovate: {mdvrp_count} MDVRP istanze su {file_count} istanze totali")
    for i in mdvrp_file:
        print(i)
    return mdvrp_file, mdvrp_count


# Scorre tutti i file nella directory delle istanze e cerca le istanze di tipo AVRP
# Restituisce una lista con i nomi dei file delle istanze AVRP e il numero di istanze trovate
# Se il campo 'edge_weight_type' è EXPLICIT, sono fornite le distanze come matrice in due modi differenti,
# specificati dal campo 'edge_weight_format':
# LOWER_ROW: matrice triangolare inferiore senza diagonale (Per definizione Simmetrica)
# FULL_MATRIX: matrice completa (Non è detto che descriva un grafo Simmetrico)
def found_avrp_instances(directory_path="resources/vrplib/Instances"):
    avrp_file = []
    file_count = 0
    avrp_count = 0
    for file in os.listdir(directory_path):
        if file.endswith(".vrp"):
            file_count += 1
            with open(os.path.join(directory_path, file), "r") as f:
                content = f.read(1000) # Leggo solo i primi 1000 caratteri per ridurre il tempo di esecuzione
                if 'FULL_MATRIX' in content:
                    avrp_file.append(file)
                    avrp_count += 1
    print(f"Trovate: {avrp_count} istanze con pesi formattati come FULL_MATRIX, su {file_count} istanze totali")
    for i in avrp_file:
        print(i)
    return avrp_file, avrp_count


# Algoritmo per contare il numero di istanze di tipo small, mid-small, mid, mid-large, large e x-large
def found_instance_size(directory_path="resources/vrplib/Instances"):
    small = 0
    mid_small = 0
    mid = 0
    mid_large = 0
    large = 0
    x_large = 0
    for file in os.listdir(directory_path):
        if file.endswith(".vrp"):
            with open(os.path.join(directory_path, file), "r") as f:
                content = f.read()
                if 'DIMENSION' in content:
                    dimension = int(content.split('DIMENSION : ')[1].split('\n')[0])
                    if dimension <= 50:
                        small += 1
                    elif dimension <= 100:
                        mid_small += 1
                    elif dimension <= 250:
                        mid += 1
                    elif dimension <= 500:
                        mid_large += 1
                    elif dimension <= 1000:
                        large += 1
                    else:
                        print(file, dimension)
                        x_large += 1
    print(f"Small: {small}")
    print(f"Mid-Small: {mid_small}")
    print(f"Mid: {mid}")
    print(f"Mid-Large: {mid_large}")
    print(f"Large: {large}")
    print(f"X-Large: {x_large}")


#found_avrp_instances()
#found_mdvrp_instances()
found_instance_size()
