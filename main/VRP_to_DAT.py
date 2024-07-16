import os
import ParseInstances as Parser

INSTANCE_DIRECTORY = '../resources/vrplib/Instances/'
OUTPUT_DIRECTORY = '../resources/vrplib/DATs/'
NAME_BY_SIZE_DIR = "../resources/vrplib/Name_of_instances_by_dimension/"

# Se impostati a True, eseguirà l'euristica la creazione dei file DAT per le istanze di quel tipo
SMALL = True
MID_SMALL = True
MID = True
MID_LARGE = True
LARGE = True
X_LARGE = False


def parse_vrp(file_path):

    instance = Parser.make_instance_from_path_name(file_path)

    # Estrazione dei dati necessari dall'istanza
    name = Parser.get_name(instance)
    capacity = Parser.get_truck_capacity(instance)
    demands = Parser.get_node_demands(instance)
    num_nodes = Parser.get_nodes_dimension(instance)  # Lista delle coordinate dei nodi
    depot = Parser.get_depots_index(instance)[0]
    weight = Parser.get_edge_weight(instance)

    return {
        'name': name,
        'capacity': capacity,
        'num_vehicles': Parser.get_truck(instance).get_min_num(),
        'demands': demands,
        'num_nodes': num_nodes,
        'depot': depot,
        'edge_weight': weight
    }


def generate_ampl_data_from_vrp(vrp_data, output_file):
    with open(output_file, 'w') as file:
        file.write("data;\n\n")
        num_nodes = vrp_data['num_nodes']
        num_vehicles = vrp_data['num_vehicles']

        # Set di vertici
        file.write(f"set V := {' '.join(str(i + 1) for i in range(num_nodes))};\n")

        # Set di veicoli
        file.write(f"set K := {' '.join(str(i) for i in range(1, num_vehicles+1))};\n")

        # Capacità
        file.write(f"param C := {vrp_data['capacity']};\n")

        # Domanda dei clienti
        file.write("param d :=\n")
        for i, demand in enumerate(vrp_data['demands']):
            file.write(f" {i + 1} {demand}\n")
        file.write(";\n")

        # Distanze (costi di percorrenza)
        file.write("param c :\n")
        file.write(" ")
        file.write(" ".join(str(i + 1) for i in range(num_nodes)) + " :=\n")

        # Scrittura della matrice di costi di percorrenza
        for i in range(num_nodes):
            file.write(f"{i + 1} ")
            for j in range(num_nodes):
                if i == j:
                    file.write(" 999999")  # Imposto una distanza elevata per la città stessa
                else:
                    file.write(f" {vrp_data['edge_weight'][i][j]}")
            file.write("\n")

        file.write(";\n")
        file.write("end;\n")


# -------------------- Generazione dei file DAT --------------------
def Generate_All_Dats_from_vrp(size, input_dir):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)

    # Verifico che il file contenente i nomi delle istanze esista
    if not os.path.exists(input_dir):
        print("Il file non esiste")
        return

    # Apro il file in lettura
    n = open(input_dir, "r")

    for filename in n:
        filename = filename.strip()
        if filename.endswith('.vrp'):
            # Se il file DATS non esiste, lo crea
            if not os.path.exists(os.path.join(OUTPUT_DIRECTORY, filename.split('.')[0]+'.dat')):
                print(f"Generating DAT for {filename}")
                vrp_data = parse_vrp(os.path.join(INSTANCE_DIRECTORY, filename))
                output_file = os.path.join(OUTPUT_DIRECTORY, f"{vrp_data['name']}.dat")
                generate_ampl_data_from_vrp(vrp_data, output_file)
                print(f"Generated {output_file}")
            else:
                print(f"File {filename} already exists")


def Generate_Dat_from_vrp(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    vrp_data = parse_vrp(input_file)
    output_file = os.path.join(output_dir, f"{vrp_data['name']}.dat")
    generate_ampl_data_from_vrp(vrp_data, output_file)
    print(f"Generated {output_file}")


#Generate_Dat_from_vrp('../resources/vrplib/Instances/P-n22-k8.vrp', OUTPUT_DIRECTORY)
if SMALL:
    Generate_All_Dats_from_vrp("small", f"{NAME_BY_SIZE_DIR}small_instances_name.txt")
if MID_SMALL:
    Generate_All_Dats_from_vrp("mid_small", f"{NAME_BY_SIZE_DIR}mid_small_instances_name.txt")
if MID:
    Generate_All_Dats_from_vrp("mid", f"{NAME_BY_SIZE_DIR}mid_instances_name.txt")
if MID_LARGE:
    Generate_All_Dats_from_vrp("mid_large", f"{NAME_BY_SIZE_DIR}mid_large_instances_name.txt")
if LARGE:
    Generate_All_Dats_from_vrp("large", f"{NAME_BY_SIZE_DIR}large_instances_name.txt")
if X_LARGE:
    Generate_All_Dats_from_vrp("x_large", f"{NAME_BY_SIZE_DIR}x_large_instances_name.txt")