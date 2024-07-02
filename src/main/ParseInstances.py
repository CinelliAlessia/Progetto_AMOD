import array
import vrplib
from src.main.Client import Client

nameInstance = "resources/vrplib/Instances/A-n32-k5.vrp"


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


workingInstance()
