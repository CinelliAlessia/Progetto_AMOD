import matplotlib.pyplot as plt
import networkx as nx


def direct_tour(nodes):
    x_dep = 0
    y_dep = 0

    for dep in nodes:
        if dep.get_is_depots():
            x_dep = dep.get_x()
            y_dep = dep.get_y()
            break

    for c in nodes:
        if not c.get_is_depots():
            x_coord = c.get_x()
            y_coord = c.get_y()

            plt.plot([x_dep, x_coord], [y_dep, y_coord])
            plt.plot([x_coord, x_dep], [y_coord, y_dep])


def plotFigure(nodes):

    x_coords = []
    y_coords = []

    # Estrai le coordinate x e y dei client
    for n in nodes:
        if not n.get_is_depots():
            x_coords.append(n.get_x())
            y_coords.append(n.get_y())
        else:
            plt.scatter(n.get_x(), n.get_y(), color='red')

    # Crea il grafico a dispersione
    plt.scatter(x_coords, y_coords, color='blue')


    # Collega i punti con delle rette
    #plt.plot(x_coords, y_coords)

    # Aggiungi titolo ed etichette agli assi
    plt.title('Grafico dei Nodi')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    # Mostra il grafico
    plt.show()


def plot_roots_figure(nodes, roots):
    x_coords = []
    y_coords = []

    # Estrai le coordinate x e y dei client
    for n in nodes:
        if not n.get_is_depots():
            x_coords.append(n.get_x())
            y_coords.append(n.get_y())
        else:
            plt.scatter(n.get_x(), n.get_y(), color='red')

    # Crea il grafico a dispersione
    plt.scatter(x_coords, y_coords, color='blue')

    # Disegna le rette tra nodi consecutivi per ogni root
    for root in roots:
        for i in range(len(root)-1):
            x1, y1 = nodes[i].get_x(), nodes[i].get_y()
            x2, y2 = nodes[i+1].get_x(), nodes[i+1].get_y()
            plt.plot([x1, y1], [x2, y2], 'k-')  # 'k-' per una linea nera

    # Collega i punti con delle rette
    #plt.plot(x_coords, y_coords)

    # Aggiungi titolo ed etichette agli assi
    plt.title('Grafico dei Nodi')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    # Mostra il grafico
    plt.show()


def plot_graph(nodes):

    # Creazione del grafo
    G = nx.Graph()

    id_depot = 0

    # Aggiunta dei nodi con attributi (indice) in una posizione specifica
    for n in nodes:
        G.add_node(n.get_id(), pos=(n.get_x(), n.get_y()))
        if n.get_is_depots():
            id_depot = n.get_id()
            G.nodes[id_depot]['color'] = 'red'

    # Aggiunta degli archi
    # Esempio: G.add_edge('A', 'B')
    for c in nodes:
        if not c.get_is_depots():
            G.add_edge(id_depot, c.get_id())  # Connette ogni cliente al deposito

    # Disegno del grafo
    pos = nx.get_node_attributes(G, 'pos')

    edge_labels = {}
    # Aggiunta di etichette agli archi
    for (u, v) in G.edges:
        u = nodes[u]
        v = nodes[v]

        d = u.get_distance(v.get_id())
        print(f"(u: {u.get_id()}, v: {v.get_id()}) = {d}")

        # Aggiungi l'etichetta all'arco
        edge_labels[(u.get_id(), v.get_id())] = str(d)

    nx.draw(G, pos, with_labels=True, node_size=500, edge_color='k')

    # Disegno delle etichette sugli archi
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Mostra il grafo
    plt.show()


def plot_roots_graph(nodes, roots):
    # Creazione del grafo
    G = nx.Graph()

    # Aggiunta dei nodi con attributi (indice) in una posizione specifica
    for n in nodes:
        G.add_node(n.get_id(), pos=(n.get_x(), n.get_y()), weight=n.get_demand())

        if n.get_is_depots():
            G.nodes[n.get_id()]['color'] = 'red'
        else:
            G.nodes[n.get_id()]['color'] = 'cyan'

    # Aggiunta degli archi
    for r in roots:
        for i in range(len(r)-1):
            G.add_edge(r[i], r[i+1])

    # Disegno del grafo
    pos = nx.get_node_attributes(G, 'pos')
    colors = nx.get_node_attributes(G, 'color').values()
    weights = nx.get_node_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=False, node_size=500, node_color=colors, edge_color='k')

    # Etichette dei nodi con il loro peso
    node_labels = {node: f"{node}\n({weight})" for node, weight in weights.items()}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    # Mostra il grafo
    plt.show()