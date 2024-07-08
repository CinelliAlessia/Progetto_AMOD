import vrplib
from src.main.Model.Node import Node
from src.main.Model.Truck import Truck


# Crea l'oggetto dell'istanza
def make_instance_from_path_name(path):
    instance = vrplib.read_instance(path)
    return instance


def get_optimal_cost_from_path(path):
    instance = make_instance_from_path_name(path)
    comment = instance.get('comment')
    if comment is not None:
        if "Optimal value:" in comment:
            parts = comment.split("Optimal value:")[1]
            return float(parts[:-1])
    return None


# Restituisce il numero dei nodi (compreso deposito) andando a leggere il campo 'dimension' dell'istanza
def get_nodes_dimension(instance):
    return instance.get('dimension')


def get_edge_weight_type(instance):
    return instance.get('edge_weight_type')


def get_edge_weight_format(instance):
    if instance.get('edge_weight_type') == 'EXPLICIT':
        return instance.get('edge_weight_format')
    return None


# Restituisce le coordinate dei nodi andando a leggere il campo 'node_coords' dell'istanza,
# nel caso di formato: EXPLICIT restituisce None
def get_node_coords(instance):
    # Se il campo 'edge_weight_type' è EUC_2D, FLOOR_2D o EXACT_2D,
    # le coordinate sono fornite come coppie di valori (x, y)
    if instance.get('edge_weight_type') in ['EUC_2D', 'FLOOR_2D', 'EXACT_2D']:
        return instance.get('node_coord').tolist()

    # Se il campo 'edge_weight_type' è EXPLICIT, sono fornite le distanze come matrice in due modi differenti,
    # specificati dal campo 'edge_weight_format':
    # LOWE ROW: matrice triangolare inferiore senza diagonale
    # FULL_MATRIX: matrice completa
    elif instance.get('edge_weight_type') == 'EXPLICIT':
        if instance.get('edge_weight_format') == 'LOWER_ROW':
            return None
        return None


def get_truck_capacity(instance):
    return instance.get('capacity')


# Prendo il campo edge_weight dell'istanza, che esprime le distanze euclidee tra i nodi come: numpy.ndarray
def get_edge_weight(instance):
    return instance.get('edge_weight')


# Restituisce le domande dei nodi andando a leggere il campo 'demands' dell'istanza
def get_node_demands(instance):
    return instance.get('demand').tolist()


# Restituisce il deposito andando a leggere il campo 'depot' dell'istanza
def get_depots_index(instance):
    return instance.get('depot').tolist()


# Commenti possibili
#    1. "Min no of trucks: 5" -> num veicoli min = 5, max = inf
#    2. "No of trucks: 5" -> num veicoli min = 5, max = 5
#    3. Un numero es. "845.26" -> num veicoli min = 0, max = inf
#    4. Altrimenti -> num veicoli min = 0, max = inf
def get_truck(instance):
    min_truck = 0
    max_truck = float('inf')

    comment = instance.get('comment')

    # se commento non è none e non è un numero
    if comment is not None and not str(comment).replace('.', '', 1).isdigit():
        if "Min no of trucks:" in comment:
            trucks_info = comment.split("Min no of trucks:")[1].strip()
            try:
                min_truck = int(trucks_info.split(",")[0])
                max_truck = float('inf')
            except ValueError:
                print(f"Error converting '{trucks_info.split(",")[0]}' to int")

        elif "No of trucks:" in comment:
            trucks_info = comment.split("No of trucks:")[1].strip()
            try:
                min_truck = int(trucks_info.split(",")[0])
                max_truck = min_truck
            except ValueError:
                print(f"Error converting '{trucks_info.split(",")[0]}' to int")
        else:
            min_truck = 0
            max_truck = float('inf')
    capacity = instance.get('capacity')
    truck = Truck(min_truck, max_truck, capacity)

    return truck


def get_name(instance):
    return instance.get('name')


def work_on_instance(path):
    # Creo l'oggetto istanza
    instance = make_instance_from_path_name(path)
    # print(instance)

    truck = get_truck(instance)  # Ottengo il numero dei veicoli
    list_of_depots = get_depots_index(instance)  # Ottengo gli indici dei depositi
    num_of_nodes = get_nodes_dimension(instance)  # Ottengo il numero dei nodi
    num_of_clients = num_of_nodes - len(list_of_depots)  # Ottengo il numero dei clienti
    edge_weight = get_edge_weight(instance)  # Ottengo le distanze tra i nodi
    demands = get_node_demands(instance)  # Ottengo la lista delle domande dei clienti

    coordinates = get_node_coords(instance)  # Ottengo le coordinate dei nodi
    if coordinates is None:
        print("L'istanza ha formato 'EXPLICIT', non è possibile ricavare le coordinate dei nodi.")

    nodes = []
    for i in range(num_of_nodes):
        if i in list_of_depots:
            is_depots = True
        else:
            is_depots = False
        nodes.append(Node(i, coordinates[i][0], coordinates[i][1], edge_weight[i], is_depots, demands[i]))

    print(f"numero di nodi: {num_of_nodes}")
    print(f"numero di client: {num_of_clients}")
    print(f"depositi: {list_of_depots}")
    print(f"coordinates: {coordinates}")
    print(f"demands: {demands}")
    print(f"veicoli: {truck}")

    return nodes, truck
