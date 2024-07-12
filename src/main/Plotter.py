import matplotlib.pyplot as plt
import networkx as nx


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

    # Aggiunta degli archi con colori specifici per ogni root
    colori = ['blue', 'green', 'magenta', 'black', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'maroon',
              'cyan', 'teal', 'navy', 'lime', 'gold', 'indigo', 'coral', 'khaki', 'yellow']
    for index, r in enumerate(roots):
        colore_arco = colori[index % len(colori)]  # Seleziona un colore dalla lista, usa modulo per evitare errori di indice
        for i in range(len(r)-1):
            G.add_edge(r[i], r[i+1], color=colore_arco)

    # Disegno del grafo
    pos = nx.get_node_attributes(G, 'pos')
    colors = [G.nodes[n]['color'] for n in G.nodes()]
    edge_colors = [G[u][v]['color'] for u, v in G.edges()]

    # Etichette dei nodi con il loro peso o solo ID in base al numero di nodi
    if len(G.nodes()) <= 50:
        node_labels = {node: f"{node}\n({G.nodes[node]['weight']})" for node in G.nodes()}
    else:
        node_labels = {node: f"{node}" for node in G.nodes()}

    # Imposta la dimensione della figura e la risoluzione
    plt.figure(figsize=(20, 15), dpi=200)  # Dimensioni in pollici (larghezza, altezza) e dpi per la risoluzione

    nx.draw(G, pos, node_size=200, node_color=colors, edge_color=edge_colors)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)

    # Mostra il grafo
    plt.show()

# Esempio di utilizzo (devi fornire implementazioni per Node e Root)
# nodes = ...
# roots = ...
# plot_roots_graph(nodes, roots)
