from src.main.ParseInstances import work_on_instance
import matplotlib.pyplot as plt

nameInstance = "resources/vrplib/Instances/P-n16-k8.vrp"


def direct_tour(clients, depots):
    x_dep = 0
    y_dep = 0

    for d in depots: #SOLAMENTE UNO
        x_dep = d.get_x()
        y_dep = d.get_y()

    for c in clients:
        x_coord = c.get_x()
        y_coord = c.get_y()

        plt.plot([x_dep, x_coord], [y_dep, y_coord])
        plt.plot([x_coord, x_dep], [y_coord, y_dep])


def plot():
    clients, depots, truck = work_on_instance(nameInstance)

    x_coords = []
    y_coords = []

    # Estrai le coordinate x e y dei client
    for c in clients:
        x_coords.append(c.get_x())
        y_coords.append(c.get_y())

    # Crea il grafico a dispersione
    plt.scatter(x_coords, y_coords, color='blue')

    for d in depots:
        plt.scatter(d.get_x(), d.get_y(), color='red')

    # Collega i punti con delle rette
    #plt.plot(x_coords, y_coords)

    # Aggiungi titolo e etichette agli assi
    plt.title('Grafico dei Nodi')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    direct_tour(clients, depots)
    # Mostra il grafico
    plt.show()


plot()
