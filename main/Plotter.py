import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


def plot_routes_graph(nodes, routes):
    # Creazione del grafo
    G = nx.Graph()

    # Aggiunta dei nodi con attributi (indice) in una posizione specifica
    for n in nodes:
        G.add_node(n.get_id(), pos=(n.get_x(), n.get_y()), weight=n.get_demand())

        if n.get_is_depots():
            G.nodes[n.get_id()]['color'] = 'red'
        else:
            G.nodes[n.get_id()]['color'] = 'cyan'

    # Aggiunta degli archi con colori specifici per ogni routes
    colori = ['blue', 'green', 'magenta', 'black', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'maroon',
              'cyan', 'teal', 'navy', 'lime', 'gold', 'indigo', 'coral', 'khaki', 'yellow']

    for index, r in enumerate(routes):
        colore_arco = colori[index % len(colori)]  # Seleziona un colore dalla lista, usa modulo per evitare errori di indice
        for i in range(len(r)-1):
            G.add_edge(r[i], r[i+1], color=colore_arco, weight=2.5)

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
    plt.figure(figsize=(10, 7), dpi=100)  # Dimensioni in pollici (larghezza, altezza) e dpi per la risoluzione

    nx.draw(G, pos, node_size=500, node_color=colors, edge_color=edge_colors)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)

    # Mostra il grafo
    plt.show()


def plot_if_not_explicit(routes, nodes):
    if nodes[0].get_x() is not None:
        plot_routes_graph(nodes, routes)
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

def evaluate_two_column(csv_file, column1, column2, column3, title):
    # Carica i dati dal file CSV usando il delimitatore ';'
    data = pd.read_csv(csv_file, delimiter=',')

    # Crea il grafico
    plt.figure(figsize=(10, 6))

    # Raggruppa i dati
    grouped_data = data.groupby(column1)[column2].mean().reset_index()

    #Raggruppa i dati e calcola la media di column2 e column3 per ogni valore di column1
    grouped_data = data.groupby(column1).agg({column2: 'mean', column3: 'mean'}).reset_index()

    # Ordina i dati in base alla colonna numerica
    grouped_data = grouped_data.sort_values(by=column3)

    plt.plot(grouped_data[column1], grouped_data[column2], marker='o', linestyle='-', markersize=5)

    # Aggiungi annotazioni per alcuni valori di column3
    num_annotations = 10  # Numero di annotazioni da mostrare
    step = max(1, len(grouped_data) // num_annotations)  # Passo per selezionare le annotazioni
    for i in range(0, len(grouped_data), step):
        plt.annotate(f'{grouped_data[column3].iloc[i]:.2f}',
                     (grouped_data[column1].iloc[i], grouped_data[column2].iloc[i]),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center',
                     fontsize=8)

    # Etichette del grafico
    plt.title(title)
    plt.xlabel('Instance ordered by dimension')
    plt.ylabel('Secondi')

    # Personalizza la griglia per mostrare solo le linee orizzontali
    plt.grid(True, which='both', axis='y', linestyle='--')

    # Nascondi le etichette dell'asse x ma mostra la label
    plt.xticks([])  # Rimuove i numeri delle etichette dell'asse x

    # Mostra il grafico
    plt.show()


def evaluate_3_columns(csv_file, column1, column2, column3, title):
    # Carica i dati dal file CSV usando il delimitatore ','
    data = pd.read_csv(csv_file, delimiter=',')

    # Calcola il rapporto tra column1 e column2
    data['Ratio'] = data[column1] / data[column2]

    # Ordina i dati in base al rapporto
    data_sorted = data.sort_values(by='Ratio')

    # Crea il grafico
    plt.figure(figsize=(10, 6))

    # Crea il grafico: rapporto sull'asse x e column3 sull'asse y
    plt.plot(data_sorted['Ratio'], data_sorted[column3], marker='o', linestyle='-', markersize=5, label=f'{column3}')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel(f'Ratio ({column1} / {column2})')
    plt.ylabel(column3)
    plt.legend()

    # Personalizza la griglia per mostrare solo le linee orizzontali
    plt.grid(True, which='both', axis='y', linestyle='--')

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


def evaluate_apx_sweep(csv_file, title):
    # Carica i dati dal file CSV usando il delimitatore ';'
    data = pd.read_csv(csv_file, delimiter=',')

    # Estrai le colonne di interesse
    apx1 = data['Execution_time_NoOpt']
    apx2 = data['Execution_time_2Opt']
    apx3 = data['Execution_time_3Opt']

    # Crea il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(apx1, marker='o', linestyle='-', label='Sweep')
    plt.plot(apx2, marker='s', linestyle='--', label='2 Opt')
    plt.plot(apx3, marker='x', linestyle='-.', label='3 Opt')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel('Istanze')
    plt.ylabel('Tempo di esecuzione')
    plt.legend()
    plt.grid(True)

    # Determine the range of your data to set appropriate y-ticks
    y_min = min(min(apx1), min(apx2), min(apx3))
    y_max = max(max(apx1), max(apx2), max(apx3))

    # Set y-ticks at more granular intervals
    plt.yticks(np.arange(y_min, y_max, step=(y_max - y_min) / 20))  # Adjust the step as needed

    # Show the plot
    plt.show()


def valuate_truck(csv_file, title):
    # Carica i dati dal file CSV usando il delimitatore ';'
    data = pd.read_csv(csv_file, delimiter=',')

    # Estrai le colonne di interesse
    truck = data['#Truck']
    used_truck = data['Used_Truck']

    # Crea il grafico
    plt.figure(figsize=(12, 10))

    feasible = 0
    infeasible = 0
    for i in range(len(truck)):
        if used_truck[i] <= truck[i] or truck[i] == 0 or truck[i] == None:
            feasible += 1
        else:
            infeasible += 1

    # Grafico a torta
    labels = ['Feasible', 'Infeasible']
    sizes = [feasible, infeasible]
    colors = ['#4CAF50', '#F44336']  # Verde e Rosso per facilitare la distinzione
    explode = (0.1, 0)  # Esplodi il segmento "Feasible" per evidenziarlo

    # Crea il grafico a torta
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, shadow=True, textprops={'fontsize': 24})

    # Etichetta del grafico
    plt.title(title, fontsize=24)

    # Mostra il grafico
    plt.show()




# Esempio di utilizzo

RESULT_SWEEP = 'Results/Heuristic_Solutions/Sweep/'
RESULT_CW = 'Results/Heuristic_Solutions/Clarke_&_Wright_run/'
RESULT_RANDOM = 'Results/Random_Solutions/'

SMALL_SWEEP = RESULT_SWEEP + 'small_Sweep_APX_and_Time.csv'
MID_SMALL_SWEEP = RESULT_SWEEP + 'mid_small_Sweep_APX_and_Time.csv'
MID_SWEEP = RESULT_SWEEP + 'mid_Sweep_APX_and_Time.csv'
MID_LARGE_SWEEP = RESULT_SWEEP + 'mid_large_Sweep_APX_and_Time.csv'
LARGE_SWEEP = RESULT_SWEEP + 'large_Sweep_APX_and_Time.csv'
X_LARGE_SWEEP = RESULT_SWEEP + 'x_large_Sweep_APX_and_Time_Timeout.csv'

SMALL_RANDOM = RESULT_RANDOM + "small_Random_APX_and_Time.csv"

SMALL_CW = RESULT_CW + 'small_CW_APX_and_Time.csv'
LARGE_CW = RESULT_CW + 'large_CW_APX_and_Time.csv'

ALL_SWEEP = RESULT_SWEEP + 'Sweep_all.csv'
ALL_CW = RESULT_CW + 'CW_All.csv'
ALL_RANDOM = RESULT_RANDOM + 'Random_All.csv'

PLOT = True
if PLOT:
    # evaluate_apx_sweep(SMALL_SWEEP, 'Performance dell\'Algoritmo di Sweep nel VRP - small')
    #     evaluate_apx_sweep(MID_SMALL_SWEEP, 'Performance dell\'Algoritmo di Sweep nel VRP - mid small')
    #     evaluate_apx_sweep(MID_SWEEP, 'Performance dell\'Algoritmo di Sweep nel VRP - mid')
    #     evaluate_apx_sweep(MID_LARGE_SWEEP, 'Performance dell\'Algoritmo di Sweep nel VRP - mid large')
    #     evaluate_apx_sweep(LARGE_SWEEP, 'Performance dell\'Algoritmo di Sweep nel VRP - large')
    #     evaluate_apx_sweep(X_LARGE_SWEEP, 'Performance dell\'Algoritmo di Sweep nel VRP - x large')
    #evaluate_single_column_two_files(SMALL_SWEEP, SMALL_CW, SMALL_RANDOM, 'APX', 'Confronto tra Sweep, Clarke & Wright e Random')
    #evaluate_two_column(ALL_CW, 'Instance_Name', 'Execution_time', '#Node', 'Clarke & Wright - Apx_3Opt per Size')
    #evaluate_3_columns(ALL_SWEEP, '#Node', 'Capacity', 'Execution_time_3Opt','Sweep - Apx_3Opt per Size')
    valuate_truck(ALL_SWEEP, 'Sweep - Feasibility of the solution')
    valuate_truck(ALL_CW, 'Clarke & Wright - Feasibility of the solution')
    valuate_truck(ALL_RANDOM, 'Random - Feasibility of the solution')






