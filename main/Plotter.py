import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


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


def plot_if_not_explicit(roots, nodes):
    if nodes[0].get_x() is not None:
        plot_roots_graph(nodes, roots)
    else:
        print("L'istanza ha formato 'EXPLICIT', non è possibile visualizzare i nodi su un grafico.")


def plot_statistics():
    # Carica i dati dal file CSV
    df = pd.read_csv('Results/Heuristic_Solutions/Sweep/small_Sweep_APX_and_Time.csv')

    # Filtra per la dimensione 'size'
    df_filtered = df[df['Size'] == 'small']

    # Calcola media, varianza e mediana della colonna 'Apx_3Opt'
    media = df_filtered['Apx_3Opt'].mean()
    varianza = df_filtered['Apx_3Opt'].var()
    mediana = df_filtered['Apx_3Opt'].median()

    # Crea un DataFrame con le statistiche
    stats_df = pd.DataFrame({'Statistiche': ['Media', 'Varianza', 'Mediana'],
                             'Valori': [media, varianza, mediana]})

    # Plotta un grafico a barre
    plt.figure(figsize=(8, 6))
    plt.bar(stats_df['Statistiche'], stats_df['Valori'], color=['blue', 'orange', 'green'])
    plt.title('Statistiche Apx_3Opt per Size = small')
    plt.ylabel('Valori')
    plt.show()


#plot_statistics()

def boxPlot():
    # Carica il file CSV
    df = pd.read_csv('Results/Heuristic_Solutions/Sweep/Sweep_all.csv')

    # Seleziona solo le colonne necessarie
    df_selected = df[['Size', 'Apx_3Opt']]

    # Raggruppa per 'Size' e crea una lista di valori di 'Apx_3Opt' per ogni 'Size'
    grouped_data = df_selected.groupby('Size')['Apx_3Opt'].apply(list).to_dict()

    # Estrai i dati per il box plot
    boxplot_data = [grouped_data[size] for size in sorted(grouped_data.keys())]

    # Crea il box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data, tick_labels=sorted(grouped_data.keys()))
    plt.title('Box plot di Apx_3Opt per Size')
    plt.xlabel('Size')
    plt.ylabel('Apx_3Opt')
    plt.grid(True)
    plt.show()


#boxPlot()

def evaluate_two_column(csv_file, column1, column2, title):
    # Carica i dati dal file CSV usando il delimitatore ';'
    data = pd.read_csv(csv_file, delimiter=';')

    # Crea il grafico
    plt.figure(figsize=(10, 6))

    # Raggruppa i dati
    grouped_data = data.groupby(column1)[column2].mean().reset_index()

    plt.plot(grouped_data[column1], grouped_data[column2], marker='o', linestyle='-')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.grid(True)

    # Mostra il grafico
    plt.show()


def evaluate_single_column_two_files(csv_file1, csv_file2, csv_file3, column, title):

    # Carica i dati dai file CSV usando il delimitatore ';'
    data1 = pd.read_csv(csv_file1, delimiter=',')
    data2 = pd.read_csv(csv_file2, delimiter=',')
    data3 = pd.read_csv(csv_file3, delimiter=',')

    # Estrai le colonne di interesse
    apx1 = data1['Apx_3Opt']
    apx2 = data2['APX']
    apx3 = data3['APX']

    # Crea il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(apx1, marker='o', linestyle='-', label='SWEEP')
    plt.plot(apx2, marker='s', linestyle='--', label='CW')
    plt.plot(apx3, marker='x', linestyle='-.', label='RANDOM')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel('Istanza')
    plt.ylabel(column)
    plt.legend()
    plt.grid(True)

    # Mostra il grafico
    plt.show()



# Esempio di utilizzo

SWEEP = 'Results/Heuristic_Solutions/Sweep/'
CW = 'Results/Heuristic_Solutions/Clarke_&_Wright_run/'
RANDOM = 'Results/Random_Solutions/'

csv_file = 'Results/Heuristic_Solutions/Sweep/All.csv'
evaluate_two_column(csv_file, 'Size', 'Apx_3Opt', 'Performance dell\'Algoritmo di Sweep nel VRP')


cvs1 = SWEEP + 'mid_Sweep_APX_and_Time.csv'
cvs2 = CW + 'mid_CW_APX_and_Time.csv'
cvs3 = RANDOM + "mid_Random_APX_and_Time.csv"

evaluate_single_column_two_files(cvs1, cvs2, cvs3, 'APX', 'Confronto tra Sweep, Clarke & Wright e Random')



