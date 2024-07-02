import vrplib
from src.main.Client import Client
from src.main.Truck import Truck

nameInstance = "resources/vrplib/Instances/Antwerp1.vrp"


# Crea l'oggetto dell'istanza
def createInstance(instance_name):
    instance = vrplib.read_instance(instance_name)
    return instance


# Restituisce gli id dei nodi andando a leggere il campo 'dimension' dell'istanza e togliendo il deposito
def get_node_ids(instance):
    return instance.get('dimension')


# Restituisce le coordinate dei nodi andando a leggere il campo 'node_coords' dell'istanza
def get_node_coords(instance):
    return instance.get('node_coord').tolist()


# Restituisce le domande dei nodi andando a leggere il campo 'demands' dell'istanza
def get_node_demands(instance):
    return instance.get('demand').tolist()


# Restituisce il deposito andando a leggere il campo 'depot' dell'istanza
def get_depot(instance):
    return instance.get('depot').tolist()


def get_truck(instance):
    # Commenti possibili
    #    1. "Min no of trucks: 5" -> num veicoli min = 5, max = inf
    #    2. "No of trucks: 5" -> num veicoli min = 5, max = 5
    #    3. Un numero es. "845.26" -> num veicoli min = 0, max = inf
    #    4. Altrimenti -> num veicoli min = 0, max = inf

    min_truck = 0
    max_truck = float('inf')

    comment = instance.get('comment')
    print(comment)

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

    print(trunk)
    return trunk


def workingInstance():
    instance = createInstance(nameInstance)
    print(instance)

    depots = get_depot(instance)
    print(f"Deposito: {depots}")

    ids = get_node_ids(instance) - len(depots)  # Ottengo il numero dei clienti

    coordinates = get_node_coords(instance)
    demands = get_node_demands(instance)

    for d in depots:
        coordinates.pop(d)
        demands.pop(d)

    print(f"id: {ids}")
    print(f"coordinates: {coordinates}")
    print(f"demands: {demands}")

    clients = []
    for i in range(ids):
        clients.append(Client(i, coordinates[i][0], coordinates[i][1], demands[i]))
        print(clients[i])

    truck = get_truck(instance)

workingInstance()
