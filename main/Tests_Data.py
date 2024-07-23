import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

RESULT_SWEEP = 'Results/Heuristic_Solutions/Sweep/'
RESULT_CW = 'Results/Heuristic_Solutions/Clarke_&_Wright_run/'
RESULT_RANDOM = 'Results/Random_Solutions/'

SMALL_SWEEP = RESULT_SWEEP + 'small_Sweep_APX_and_Time.csv'
MID_SMALL_SWEEP = RESULT_SWEEP + 'mid_small_Sweep_APX_and_Time.csv'
MID_SWEEP = RESULT_SWEEP + 'mid_Sweep_APX_and_Time.csv'
MID_LARGE_SWEEP = RESULT_SWEEP + 'mid_large_Sweep_APX_and_Time.csv'
LARGE_SWEEP = RESULT_SWEEP + 'large_Sweep_APX_and_Time_Timeout.csv'
X_LARGE_SWEEP = RESULT_SWEEP + 'x_large_Sweep_APX_and_Time_Timeout.csv'
SMALL_MID_SWEEP = RESULT_SWEEP + 'small_mid_sweep.csv'

SMALL_RANDOM = RESULT_RANDOM + "small_Random_APX_and_Time.csv"
SMALL_RANDOM_10k = RESULT_RANDOM + "small_Random_APX_and_Time10K.csv"
SMALL_RANDOM_100k = RESULT_RANDOM + "small_Random_APX_and_Time100K.csv"
SMALL_RANDOM_1M = RESULT_RANDOM + "small_Random_APX_and_Time1M.csv"
MID_SMALL_RANDOM = RESULT_RANDOM + "mid_small_Random_APX_and_Time.csv"
MID_RANDOM = RESULT_RANDOM + "mid_Random_APX_and_Time.csv"
MID_LARGE_RANDOM = RESULT_RANDOM + "mid_large_Random_APX_and_Time.csv"
LARGE_RANDOM = RESULT_RANDOM + "large_Random_APX_and_Time.csv"
X_LARGE_RANDOM = RESULT_RANDOM + "x_large_Random_APX_and_Time.csv"

SMALL_CW = RESULT_CW + 'small_CW_APX_and_Time.csv'
MID_SMALL_CW = RESULT_CW + 'mid_small_CW_APX_and_Time.csv'
MID_CW = RESULT_CW + 'mid_CW_APX_and_Time.csv'
MID_LARGE_CW = RESULT_CW + 'mid_large_CW_APX_and_Time.csv'
LARGE_CW = RESULT_CW + 'large_CW_APX_and_Time.csv'
X_LARGE_CW = RESULT_CW + 'x_large_CW_APX_and_Time.csv'

ALL_SWEEP = RESULT_SWEEP + 'Sweep_all.csv'
ALL_CW = RESULT_CW + 'CW_All.csv'
ALL_RANDOM = RESULT_RANDOM + 'Random_All.csv'


def get_data_csv_all(file):
    """
    Carica i dati dal file CSV
    :param file: file CSV
    :return:
    """
    return pd.read_csv(file, delimiter=',')


def boxPlot_apx(path_file, string_apx, title):
    # Carica il file CSV
    df = get_data_csv_all(path_file)

    # Seleziona solo le colonne necessarie
    df_selected = df[['Size', string_apx]]

    # Raggruppa per 'Size' e crea una lista di valori di 'Apx_3Opt' per ogni 'Size'
    grouped_data = df_selected.groupby('Size')[string_apx].apply(list).to_dict()

    # Definisci l'ordine desiderato
    ordered_sizes = ['small', 'mid_small', 'mid', 'mid_large', 'large', 'x_large']

    # Estrai i dati per il box plot
    boxplot_data = [grouped_data[size] for size in ordered_sizes]

    # Crea il box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data, labels=ordered_sizes)
    plt.title(f'Apx per Size - {title}')
    plt.xlabel('')
    plt.ylabel('Apx')

    # Imposta i ticks dell'asse y da 0 a 1 con passo 0.1
    min_y = min(min(values) for values in grouped_data.values())
    max_y = max(max(values) for values in grouped_data.values())
    plt.yticks(np.arange(min_y, max_y + 0.05, step=(max_y - min_y) / 30))

    plt.grid(True)
    plt.show()


def evaluate_two_column(csv_file, column1, column2, column3, title):
    terza_colonna = False

    # Carica i dati dal file CSV usando il delimitatore ','
    data = pd.read_csv(csv_file, delimiter=',')

    # Crea il grafico
    plt.figure(figsize=(10, 6))

    # Raggruppa i dati
    grouped_data = data.groupby(column1)[column2].mean().reset_index()

    if terza_colonna:
        # Raggruppa i dati e calcola la media di column2 e column3 per ogni valore di column1
        grouped_data = data.groupby(column1).agg({column2: 'mean', column3: 'mean'}).reset_index()

        # Ordina i dati in base alla colonna numerica
        grouped_data = grouped_data.sort_values(by=column3)

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

    plt.plot(grouped_data[column1], grouped_data[column2], marker='o', linestyle='-', markersize=5)

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


def evaluate_three_column(csv_file, column1, column2, column3, x_label, y_label, title):
    # Carica i dati dal file CSV usando il delimitatore ';'
    data = pd.read_csv(csv_file, delimiter=',')

    # Crea il grafico
    plt.figure(figsize=(10, 6))

    data = data.sort_values(by=column1)

    # Estrai i dati ordinati
    nodes = data[column1]
    data2 = data[column2]
    data3 = data[column3]

    # Crea il grafico
    plt.figure(figsize=(10, 6))

    plt.plot(nodes, data2, marker='s', linestyle='--', label='2-Opt')
    #plt.plot(nodes, data3, marker='x', linestyle='-.', label='3-Opt')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)

    # Determine the range of your data to set appropriate y-ticks
    y_min = min(data2)
    y_max = max(data2)

    # Set y-ticks at more granular intervals
    plt.xticks(np.arange(min(nodes), max(nodes) + 1, step=75))
    plt.yticks(np.arange(y_min, y_max, step=(y_max - y_min) / 20))  # Adjust the step as needed

    # Mostra il grafico
    plt.show()


def evaluate_3_columns_ratio12(csv_file, column1, column2, column3, title):
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
    apx1 = data['Apx_NoOpt']
    apx2 = data['Apx_2Opt']
    apx3 = data['Apx_3Opt']

    # Crea il grafico
    plt.figure(figsize=(10, 6))
    plt.plot(apx1, marker='o', linestyle='-', label='Sweep')
    plt.plot(apx2, marker='s', linestyle='--', label='2 Opt')
    plt.plot(apx3, marker='x', linestyle='-.', label='3 Opt')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel('Istanze')
    plt.ylabel('APX')
    plt.legend()
    plt.grid(True)

    # Determine the range of your data to set appropriate y-ticks
    y_min = min(min(apx1), min(apx2), min(apx3))
    y_max = max(max(apx1), max(apx2), max(apx3))

    # Set y-ticks at more granular intervals
    plt.yticks(np.arange(y_min, y_max, step=(y_max - y_min) / 30))  # Adjust the step as needed

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


def evaluate_3time(column, title):
    csv_file1 = SMALL_SWEEP
    csv_file2 = SMALL_CW
    csv_file3 = SMALL_RANDOM

    # Carica i dati dai file CSV usando il delimitatore ';'
    data1 = pd.read_csv(csv_file1, delimiter=',').sort_values(by="#Node")
    data2 = pd.read_csv(csv_file2, delimiter=',').sort_values(by="#Node")
    data3 = pd.read_csv(csv_file3, delimiter=',').sort_values(by="#Node")

    data1 = data1.rename(columns={
        'Execution_time_2Opt': 'Execution_time_SWEEP'})
    data2 = data2.rename(columns={
        'Execution_time': 'Execution_time_CW'})
    data3 = data3.rename(columns={
        'Execution_time': 'Execution_time_RANDOM'})

    print("Colonne merged_data dopo rinominazione:", data1.columns)
    print("Colonne merged_data dopo rinominazione:", data2.columns)
    print("Colonne merged_data dopo rinominazione:", data3.columns)

    # Unisci i dati sui nodi
    merged_data = data1[['Instance_Name', 'Execution_time_SWEEP']].merge(
        data2[['Instance_Name', 'Execution_time_CW']],
        on='Instance_Name',
        how='outer'
    ).merge(
        data3[['Instance_Name', 'Execution_time_RANDOM']],
        on='Instance_Name',
        how='outer'
    )

    # Verifica i nomi delle colonne dopo la rinominazione
    print("Colonne merged_data dopo rinominazione:", merged_data.columns)

    # Estrai le colonne di interesse
    nodes = merged_data['Instance_Name']
    t1 = merged_data['Execution_time_SWEEP']
    t2 = merged_data['Execution_time_CW']
    t3 = merged_data['Execution_time_RANDOM']

    # Crea il grafico
    plt.figure(figsize=(14, 10))
    plt.plot(nodes, t1, marker='o', linestyle='-', label='SWEEP 2-Opt')
    plt.plot(nodes, t2, marker='s', linestyle='--', label='CW')
    plt.plot(nodes, t3, marker='x', linestyle='-.', label='RANDOM 1K')

    # Etichette del grafico
    plt.title(title)
    plt.xlabel('Istanze SMALL')
    plt.ylabel(column)
    plt.legend()
    plt.grid(True)

    # Determine the range of your data to set appropriate y-ticks
    y_min = min(t1.min(), t2.min(), t3.min())
    y_max = max(t1.max(), t2.max(), t3.max())

    # Set y-ticks at more granular intervals
    #plt.xticks(np.arange(len(nodes)), nodes, rotation=90)
    plt.xticks("")
    #plt.yticks(np.arange(y_min, y_max, step=(y_max - y_min) / 20))  # Adjust the step as needed

    # Mostra il grafico
    plt.show()


def plot_apx_all_random(file, title):
    """
    Crea un grafico basato sui dati della colonna APX nel file ALL_RANDOM
    :param file: file CSV
    :param title: titolo del grafico
    """
    plt.figure(figsize=(15, 10))  # Dimensione della figura e DPI elevato

    # Carica il file CSV
    data = get_data_csv_all(file)

    # Ordina i dati in base alla colonna '#Node'
    data_sorted = data.sort_values(by='#Node')

    # Estrai i dati di interesse
    instance_names = data_sorted['Instance_Name']
    apx_values = data_sorted['APX']

    # Aggiungi una linea al grafico
    plt.plot(instance_names, apx_values, marker='o', linestyle='-', markersize=7, label='Random 1K')

    # Configura il grafico
    plt.title(title, fontsize=20)  # Aumenta la dimensione del titolo
    plt.xlabel('Istanze ordinate al crescere di N', fontsize=18)  # Aumenta la dimensione dell'etichetta dell'asse x
    plt.ylabel('APX', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse y
    plt.legend(fontsize=20)  # Legenda più grande

    # Imposta i valori dei tick dell'asse y per maggiore chiarezza
    y_min = apx_values.min()
    y_max = apx_values.max()
    plt.yticks(np.arange(y_min, y_max + 0.1, step=(y_max - y_min) / 50), fontsize=11)  # Imposta ticks e dimensione

    plt.xticks([], fontsize=12)  # Rimuove le etichette dell'asse x ma mantiene la label
    plt.grid(True)

    # Mostra il grafico
    plt.show()


def random_apx_for_num_run(files, title):
    """
    Crea un grafico con una linea per ogni file basato sui dati della colonna APX
    :param files: lista di file CSV
    :param title: titolo del grafico
    """
    plt.figure(figsize=(15, 10))  # Dimensione della figura e DPI elevato

    markers = ['o', 's', '^', 'x']  # cerchio, quadrato, triangolo, croce
    colors = ['b', '#FFA500', 'g', 'r']  # blu, arancione, verde, rosso
    linestyles = ['-', '--', '-.', ':']  # stili delle righe
    labels = ['1 K', '10 K', '100 K', '1 MLN']

    all_apx_values = []

    for i, file in enumerate(files):
        # Carica il file CSV
        data = get_data_csv_all(file)

        # Ordina i dati in base alla colonna '#Node'
        data_sorted = data.sort_values(by='#Node')

        # Estrai i dati di interesse
        instance_names = data_sorted['Instance_Name']
        apx_values = data_sorted['APX']

        all_apx_values.append(apx_values)  # Raccogli i valori APX per calcolare i tick dell'asse y

        # Aggiungi una linea al grafico
        plt.plot(instance_names, apx_values, marker=markers[i], linestyle=linestyles[i], color=colors[i], markersize=7, label=labels[i])

    # Configura il grafico
    plt.title(title, fontsize=20)  # Aumenta la dimensione del titolo
    plt.xlabel('Istanze ordinate al crescere di N', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse x
    plt.ylabel('APX', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse y
    plt.legend(fontsize=18)  # Legenda più grande
    plt.xticks([])  # Nascondi le etichette dell'asse x

    # Imposta i valori dei tick dell'asse y per maggiore chiarezza
    all_apx_values = np.concatenate(all_apx_values)  # Concatenate all APX values to get min and max
    y_min = all_apx_values.min()
    y_max = all_apx_values.max()
    plt.yticks(np.arange(y_min, y_max + 0.1, step=(y_max - y_min) / 20), fontsize=14)  # Imposta ticks e dimensione

    plt.grid(True)

    # Mostra il grafico
    plt.show()


random_files = [SMALL_RANDOM, SMALL_RANDOM_10k, SMALL_RANDOM_100k, SMALL_RANDOM_1M]
random_apx_for_num_run(random_files, "Confronto APX all'aumentare del numero di run (Small)")
#plot_apx_all_random(ALL_RANDOM, "APX di Random 1K al crescere di n (Tutte le istanze)")

BOX_PLOT = False
if BOX_PLOT:
    boxPlot_apx(ALL_SWEEP, 'Apx_3Opt', "Sweep 3-Opt")
    boxPlot_apx(ALL_RANDOM, 'APX', "Random 1K")
    boxPlot_apx(ALL_CW, 'APX', "Clarke & Wright")

ECX_TIME = True
if ECX_TIME:
    evaluate_2time_sweep("Secondi", "Confronto dei Tempi di Esecuzione")
    #evaluate_3time("Secondi", "Confronto dei Tempi di Esecuzione")

