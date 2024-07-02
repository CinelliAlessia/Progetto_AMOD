import vrplib
from src.main.Client import Client
from src.main.Truck import Truck
from src.main.Depot import Depot

nameInstance = "resources/vrplib/Instances/P-n16-k8.vrp"


# Crea l'oggetto dell'istanza
def make_instance_from_path_name(path):
    instance = vrplib.read_instance(path)
    return instance


# Restituisce il numero dei nodi (compreso deposito) andando a leggere il campo 'dimension' dell'istanza
def get_nodes_dimension(instance):
    return instance.get('dimension')


# Restituisce le coordinate dei nodi andando a leggere il campo 'node_coords' dell'istanza,
# nel caso di formato: EXPLICIT restituisce None
def get_node_coords(instance):
    # Se il campo 'edge_weight_type' è EUC_2D, FLOOR_2D o EXACT_2D,
    # le coordinate sono fornite come coppie di valori (x, y)
    if (instance.get('edge_weight_type') == 'EUC_2D'
            or instance.get('edge_weight_type') == 'FLOOR_2D'
            or instance.get('edge_weight_type') == 'EXACT_2D'):
        return instance.get('node_coord').tolist()

    # Se il campo 'edge_weight_type' è EXPLICIT, sono fornite le distanze come matrice in due modi differenti,
    # specificati dal campo 'edge_weight_format':
    # LOWE ROW: matrice triangolare inferiore senza diagonale
    # FULL_MATRIX: matrice completa
    elif instance.get('edge_weight_type') == 'EXPLICIT':
        return None


# Prendo il campo edge_weight dell'istanza, che esprime le distanze euclidee tra i nodi
def get_edge_weight(instance):
    print('Le distanze fornite dalla libreria sono:')
    return instance.get('edge_weight')


# Calcola la distanza euclidea tra nodi a partire dalla lista di coppie di coordinate, viene restituita una matrice
def calculate_distance_from_coords(list):
    n = len(list)
    dist = [[0 for i in range(n)] for j in range(n)]  # Inizializzo la matrice delle distanze
    for i in range(n):
        for j in range(n):
            dist[i][j] = ((list[i][0] - list[j][0]) ** 2 + (list[i][1] - list[j][1]) ** 2) ** 0.5
    return dist


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

    if comment is not None:
        if "Min no of trucks:" in comment:
            trucks_info = comment.split(":")[1]
            min_truck = int(trucks_info.split(",")[0])
            max_truck = float('inf')

        elif "No of trucks:" in comment:
            trucks_info = comment.split(":")[1]
            min_truck = int(trucks_info.split(",")[0])
            max_truck = min_truck

    capacity = instance.get('capacity')
    trunk = Truck(min_truck, max_truck, capacity)

    return trunk


def work_on_instance(path):
    instance = make_instance_from_path_name(path)
    print(instance)

    list_of_depots = get_depots_index(instance)     # Ottengo gli indici dei depositi
    num_of_nodes = get_nodes_dimension(instance)    # Ottengo il numero dei nodi
    num_of_clients = num_of_nodes - len(list_of_depots)  # Ottengo il numero dei clienti

    coordinates = get_node_coords(instance)         # Ottengo le coordinate dei nodi
    if coordinates is None:
        print("L'istanza ha formato 'EXPLICIT', non è possibile ricavare le coordinate dei nodi.")
    else:
        print(f"Coordinate: {coordinates}")
        distances = calculate_distance_from_coords(coordinates)
        print(f"Distanze: {distances}")

    edge_weight = get_edge_weight(instance)
    print(f"Edge weight: {edge_weight}")

    demands = get_node_demands(instance)  # Ottengo la lista delle domande dei clienti

    depots = []
    for d in list_of_depots:  # Rimuovo i depositi dalle liste
        depots.append(Depot(d, coordinates[d][0], coordinates[d][1]))
        print(depots[d])

    print(f"numero di nodi: {num_of_nodes}")
    print(f"numero di client: {num_of_clients}")
    print(f"depositi: {list_of_depots}")
    print(f"coordinates: {coordinates}")
    print(f"demands: {demands}")

    clients = []
    for i in range(num_of_nodes):
        for j in list_of_depots:
            if i != j:
                clients.append(Client(i, coordinates[i][0], coordinates[i][1], demands[i], edge_weight[i]))

    truck = get_truck(instance)

    print("Veicoli:")
    print(truck)
    print("Clienti:")
    for c in clients:
        print(c)
    print("Depositi:")
    for d in depots:
        print(d)
    return clients, depots, truck


work_on_instance(nameInstance)
