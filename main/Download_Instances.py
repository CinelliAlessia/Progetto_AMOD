import os
import vrplib

pathInstance = "../resources/vrplib/Instances"
pathSolutions = "../resources/vrplib/Solutions"


def createFolder():
    if not os.path.exists(pathInstance):
        os.makedirs(pathInstance)
    if not os.path.exists(pathSolutions):
        os.makedirs(pathSolutions)


def download_instances():
    createFolder()

    # Elencare tutte le istanze disponibili
    instance_names = vrplib.list_names(vrp_type='cvrp')
    print("Istanze disponibili:" + str(len(instance_names)))
    for name in instance_names:
        print(name)

    for i in range(len(instance_names)):
        # Selezionare un'istanza specifica (ad esempio la prima della lista)
        selected_instance_name = instance_names[i]

        # Scaricare l'istanza selezionata
        print("Download istanza: " + selected_instance_name)
        vrplib.download_instance(selected_instance_name, path=pathInstance)
        vrplib.download_solution(selected_instance_name, path=pathSolutions)

    print("Download completato")


# download_instances()
