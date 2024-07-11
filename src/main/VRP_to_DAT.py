import os
import ParseInstances as Parser

FILES_DIRECTORY = '../resources/vrplib/Instances'
OUTPUT_DIRECTORY = '../resources/vrplib/DATs'


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
        file.write("param d :\n")
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
def Generate_All_Dats_from_vrp(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.vrp'):
            vrp_data = parse_vrp(os.path.join(input_dir, filename))
            output_file = os.path.join(output_dir, f"{vrp_data['name']}.dat")
            generate_ampl_data_from_vrp(vrp_data, output_file)
            print(f"Generated {output_file}")


def Generate_Dat_from_vrp(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    vrp_data = parse_vrp(input_file)
    output_file = os.path.join(output_dir, f"{vrp_data['name']}.dat")
    generate_ampl_data_from_vrp(vrp_data, output_file)
    print(f"Generated {output_file}")


Generate_Dat_from_vrp('../resources/vrplib/Instances/A-n32-k5.vrp', OUTPUT_DIRECTORY)
#Generate_All_Dats_from_vrp(FILES_DIRECTORY, OUTPUT_DIRECTORY)
