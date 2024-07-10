import os
import vrplib


FILES_DIRECTORY = '../resources/vrplib/Instances'
OUTPUT_DIRECTORY = '../resources/vrplib/DATs'
# Path della directory dei file dats (servirà ad ampl)
# C:\Users\andre\PycharmProjects\Progetto_AMOD\src\resources\vrplib\DATs


def parse_vrp(file_path):
    instance = vrplib.read_instance(file_path)

    # Estrazione dei dati necessari dall'istanza
    name = instance.get('name')
    capacity = instance.get('capacity')
    demands = instance.get('demand').tolist()
    nodes = instance.get('node_coord').tolist()
    depot = instance.get('depot')[0]

    return {
        'name': name,
        'capacity': capacity,
        'demands': demands,
        'nodes': nodes,
        'depot': depot,
        'edge_weight': instance.get('edge_weight')
    }


def generate_ampl_data_from_vrp(vrp_data, output_file):
    with open(output_file, 'w') as file:
        file.write("data;\n\n")

        # Set di vertici
        file.write("set V := " + " ".join(str(i + 1) for i in range(len(vrp_data['nodes']))) + ";\n")
        file.write("set V_CUST := " + " ".join(str(i + 1) for i in range(len(vrp_data['nodes']))
                                               if i + 1 != vrp_data['depot']) + ";\n")

        # Set di veicoli
        num_vehicles = sum(vrp_data['demands']) // vrp_data['capacity'] + 1
        file.write(f"set K := {' '.join(str(i) for i in range(1, num_vehicles + 1))};\n")

        # Capacità
        file.write(f"param C := {vrp_data['capacity']};\n")

        # Domanda dei clienti
        file.write("param d :=\n")
        for i, demand in enumerate(vrp_data['demands']):
            file.write(f" {i + 1} {demand}\n")
        file.write(";\n")

        # Distanze (costi di percorrenza)
        file.write("param c:\n")
        file.write(" " + " ".join(str(i + 1) for i in range(len(vrp_data['nodes']))) + " :=\n")

        for i, node_i in enumerate(vrp_data['nodes']):
            file.write(f"{i + 1} ")
            for j, node_j in enumerate(vrp_data['nodes']):
                dist = ((node_i[0] - node_j[0]) ** 2 + (node_i[1] - node_j[1]) ** 2) ** 0.5
                file.write(f" {dist}")
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


Generate_All_Dats_from_vrp(FILES_DIRECTORY, OUTPUT_DIRECTORY)
