import array
import vrplib
from src.main.Client import Client

nameInstance = "resources/vrplib/Instances/A-n32-k5.vrp"


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


def work_on_instance(path):
    instance = make_instance_from_path_name(path)
    print(instance)

    depots = get_depots_index(instance)
    print(f"Indici dei Depositi: {depots}")

    ids = get_nodes_dimension(instance) - len(depots)  # Ottengo il numero dei clienti

    coordinates = get_node_coords(instance)
    if coordinates is None:
        print("L'istanza ha formato 'EXPLICIT', non è possibile ricavare le coordinate dei nodi.")
    else:
        print(f"Coordinate: {coordinates}")
        distances = calculate_distance_from_coords(coordinates)
        print(f"Distanze: {distances}")

    edge_weight = get_edge_weight(instance)
    print(f"Edge weight: {edge_weight}")

    demands = get_node_demands(instance)  # Ottengo le domande dei clienti

    for d in depots:  # Rimuovo i depositi dalle liste
        coordinates.pop(d)
        demands.pop(d)

    print(f"id: {ids}")
    print(f"coordinates: {coordinates}")
    print(f"demands: {demands}")

    clients = []
    for i in range(ids):
        clients.append(Client(i, coordinates[i][0], coordinates[i][1], demands[i]))
        print(clients[i])


work_on_instance(nameInstance)
