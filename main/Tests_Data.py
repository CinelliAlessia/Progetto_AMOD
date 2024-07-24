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

SMALL_RANDOM_1K = RESULT_RANDOM + "small_Random_APX_and_Time1K.csv"
SMALL_RANDOM_10K = RESULT_RANDOM + "small_Random_APX_and_Time10K.csv"
SMALL_RANDOM_100K = RESULT_RANDOM + "small_Random_APX_and_Time100K.csv"
SMALL_RANDOM_1M = RESULT_RANDOM + "small_Random_APX_and_Time1M.csv"
SMALL_RANDOM_5min = RESULT_RANDOM + "small_Random_APX_and_Time_5min.csv"
MID_SMALL_RANDOM_1K = RESULT_RANDOM + "mid_small_Random_APX_and_Time1K.csv"
MID_RANDOM_1K = RESULT_RANDOM + "mid_Random_APX_and_Time1K.csv"
MID_LARGE_RANDOM_1K = RESULT_RANDOM + "mid_large_Random_APX_and_Time1K.csv"
LARGE_RANDOM_1K = RESULT_RANDOM + "large_Random_APX_and_Time1K.csv"
X_LARGE_RANDOM_1K = RESULT_RANDOM + "x_large_Random_APX_and_Time1K.csv"


SMALL_CW = RESULT_CW + 'small_CW_APX_and_Time.csv'
MID_SMALL_CW = RESULT_CW + 'mid_small_CW_APX_and_Time.csv'
MID_CW = RESULT_CW + 'mid_CW_APX_and_Time.csv'
MID_LARGE_CW = RESULT_CW + 'mid_large_CW_APX_and_Time.csv'
LARGE_CW = RESULT_CW + 'large_CW_APX_and_Time.csv'
X_LARGE_CW = RESULT_CW + 'x_large_CW_APX_and_Time.csv'

ALL_SWEEP = RESULT_SWEEP + 'Sweep_all.csv'
ALL_CW = RESULT_CW + 'CW_All.csv'
ALL_RANDOM_1K = RESULT_RANDOM + 'All_Random_1K.csv'
ALL_RANDOM_10K = RESULT_RANDOM + 'All_Random_10K.csv'


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
    ordered_sizes = ['small', 'mid_small', 'mid', 'mid_large', 'large']

    # Estrai i dati per il box plot
    boxplot_data = [grouped_data[size] for size in ordered_sizes]

    # Crea il box plot
    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data, labels=ordered_sizes)
    plt.title(f'Apx per Size - {title}')
    plt.xlabel('')
    plt.ylabel('Apx')

    # Imposta i ticks dell'asse y da 0 a 1 con passo 0.1
    # Filtra i valori per evitare "inf" e calcolare min_y e max_y
    all_values = [value for values in grouped_data.values() for value in values if value != float('inf')]
    if all_values:
        min_y = min(all_values)
        max_y = max(all_values)
        plt.yticks(np.arange(min_y, max_y + 0.05, step=(max_y - min_y) / 10))

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
    for i, t in enumerate(truck):
        if (used_truck[i] <= truck[i] and used_truck[i] != 0) or truck[i] == 0 or truck[i] == None:
            feasible += 1
        else:
            infeasible += 1

    # Grafico a torta
    labels = ['Feasible', 'Infeasible']
    sizes = [feasible, infeasible]
    colors = ['#4CAF50', '#F44336']  # Verde e Rosso per facilitare la distinzione
    explode = (0.1, 0)  # Esplodi il segmento "Feasible" per evidenziarlo

    # Crea il grafico a torta
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, shadow=True,
            textprops={'fontsize': 24})

    # Etichetta del grafico
    plt.title(title, fontsize=24)

    # Mostra il grafico
    plt.show()


def evaluate_3time(column, title):
    csv_file1 = SMALL_SWEEP
    csv_file2 = SMALL_CW
    csv_file3 = SMALL_RANDOM_1K

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


def evaluate_time_CW_Sweep(column, title, csv):
    # Definisci i percorsi dei file CSV in base all'argomento 'csv'
    if csv == 'SMALL':
        csv_file1 = SMALL_CW
        csv_file2 = SMALL_SWEEP
    elif csv == 'MID_SMALL':
        csv_file1 = MID_SMALL_CW
        csv_file2 = MID_SMALL_SWEEP
    elif csv == 'MID':
        csv_file1 = MID_CW
        csv_file2 = MID_SWEEP
    elif csv == 'MID_LARGE':
        csv_file1 = MID_LARGE_CW
        csv_file2 = MID_LARGE_SWEEP
    elif csv == 'LARGE':
        csv_file1 = LARGE_CW
        csv_file2 = LARGE_SWEEP
    else:
        print("CSV type non riconosciuto.")
        return

    # Carica i dati dai file CSV
    data1 = pd.read_csv(csv_file1, delimiter=',')
    data2 = pd.read_csv(csv_file2, delimiter=',')

    # Rinomina le colonne di interesse
    data1 = data1.rename(columns={'Execution_time': 'Execution_time_CW'})
    data2 = data2.rename(columns={'Execution_time_2Opt': 'Execution_time_SWEEP2'})

    # Unisci i dati sui nodi e le colonne di interesse
    merged_data = data1[['#Node', 'Instance_Name', 'Execution_time_CW']].merge(
        data2[['#Node', 'Instance_Name', 'Execution_time_SWEEP2']],
        on='Instance_Name',
        how='outer')

    # Unisci le colonne '#Node_x' e '#Node_y' in una sola colonna '#Node'
    # Evita avvisi utilizzando numpy.where per gestire i NaN
    merged_data['#Node'] = np.where(
        merged_data['#Node_x'].notna(),
        merged_data['#Node_x'],
        merged_data['#Node_y']
    )

    # Rimuovi le colonne temporanee
    merged_data = merged_data.drop(columns=['#Node_x', '#Node_y'])

    # Ordina i dati in base alla dimensione del nodo
    merged_data = merged_data.sort_values(by='#Node')

    # Estrai le colonne di interesse
    nodes = merged_data['#Node'].values  # Usa i valori direttamente
    instance_name = merged_data['Instance_Name'].values
    t1 = merged_data['Execution_time_CW'].values
    t2 = merged_data['Execution_time_SWEEP2'].values

    # Crea il grafico
    plt.figure(figsize=(14, 10))

    # Usa gli indici numerici per l'asse x
    plt.plot(np.arange(len(nodes)), t1, marker='s', linestyle='--', label='CW')
    plt.plot(np.arange(len(nodes)), t2, marker='o', linestyle='-', label='SWEEP 2-Opt')

    # Etichette del grafico
    plt.title(title, fontsize=18)
    plt.xlabel("Istanze " + csv, fontsize=18)
    plt.ylabel(column, fontsize=18)
    plt.legend(fontsize=18)

    plt.grid(True)

    y_min = min(t1.min(), t2.min())
    y_max = max(t1.max(), t2.max())

    # Imposta i tick dell'asse x e y
    # plt.xticks(ticks=np.arange(len(instance_name)), labels=instance_name, rotation=90)
    plt.yticks(np.arange(0, y_max, step=(y_max - y_min) / 20))  # Adjust the step as needed

    plt.tick_params(labelsize=18)

    # Migliora l'adattamento del layout
    plt.tight_layout()
    plt.show()


def evaluate_2time_sweep(column, title, csv):
    if csv == 'SMALL':
        csv_file1 = SMALL_SWEEP
    elif csv == 'MID_SMALL':
        csv_file1 = MID_SMALL_SWEEP
    elif csv == 'MID':
        csv_file1 = MID_SWEEP
    elif csv == 'MID_LARGE':
        csv_file1 = MID_LARGE_SWEEP
    elif csv == 'LARGE':
        csv_file1 = LARGE_SWEEP
    elif csv == 'X_LARGE':
        csv_file1 = X_LARGE_SWEEP
    else:
        return

    # Carica i dati dai file CSV usando il delimitatore ';'
    data1 = pd.read_csv(csv_file1, delimiter=',').sort_values(by="#Node")

    data1 = data1.rename(columns={
        'Execution_time_2Opt': 'Execution_time_SWEEP2'})
    data2 = data1.rename(columns={
        'Execution_time_3Opt': 'Execution_time_SWEEP3'})

    # Unisci i dati sui nodi
    merged_data = data1[['Instance_Name', 'Execution_time_SWEEP2']].merge(
        data2[['Instance_Name', 'Execution_time_SWEEP3']],
        on='Instance_Name',
        how='outer')

    # Verifica i nomi delle colonne dopo la rinominazione
    print("Colonne merged_data dopo rinominazione:", merged_data.columns)

    # Estrai le colonne di interesse
    nodes = merged_data['Instance_Name']
    t1 = merged_data['Execution_time_SWEEP2']
    t2 = merged_data['Execution_time_SWEEP3']

    # Crea il grafico
    plt.figure(figsize=(14, 10))
    plt.plot(nodes, t1, marker='o', linestyle='-', label='SWEEP 2-Opt')
    plt.plot(nodes, t2, marker='x', linestyle='-.', label='SWEEP 3-Opt')

    # Etichette del grafico
    plt.title(title, fontsize=18)
    plt.xlabel(f'Istanze {csv}', fontsize=18)
    plt.ylabel(column, fontsize=18)
    plt.legend(fontsize=18)

    plt.tick_params(labelsize=18)
    plt.grid(True)

    # Determine the range of your data to set appropriate y-ticks
    y_min = min(t1.min(), t2.min())
    y_max = max(t1.max(), t2.max())

    # Set y-ticks at more granular intervals
    plt.xticks("")
    #plt.xticks(np.arange(len(nodes)), nodes, rotation=90)
    plt.yticks(np.arange(y_min, y_max, step=(y_max - y_min) / 20))  # Adjust the step as needed

    # Mostra il grafico
    plt.show()


def winner_algorithm():
    # Carica i dati dai file CSV usando il delimitatore ';'
    data1 = pd.read_csv(SMALL_SWEEP, delimiter=',').sort_values(by="#Node")
    data2 = pd.read_csv(SMALL_CW, delimiter=',').sort_values(by="#Node")
    data3 = pd.read_csv(SMALL_RANDOM_1K, delimiter=',').sort_values(by="#Node")

    data1 = data1.rename(columns={
        'Cost_3Opt': 'Cost_SWEEP',
        'Apx_3Opt': 'Apx_SWEEP'})
    data2 = data2.rename(columns={
        'CW_cost': 'Cost_CW',
        'APX': 'Apx_CW'})
    data3 = data3.rename(columns={
        'BEST_Random': 'Cost_RANDOM',
        'APX': 'Apx_RANDOM'})

    # Unisci i dati sui nodi
    merged_data = data1[['Instance_Name', 'Cost_SWEEP', 'Apx_SWEEP']].merge(
        data2[['Instance_Name', 'Cost_CW', 'Apx_CW']],
        on='Instance_Name',
        how='outer'
    ).merge(
        data3[['Instance_Name', 'Cost_RANDOM', 'Apx_RANDOM']],
        on='Instance_Name',
        how='outer'
    )

    print("dataset")
    for r in merged_data:
        print(merged_data[r])

    # Estrai le colonne di interesse
    instance = merged_data['Instance_Name']
    t1 = merged_data['Cost_SWEEP']
    t2 = merged_data['Cost_CW']
    t3 = merged_data['Cost_RANDOM']

    apx1 = merged_data['Apx_SWEEP']
    apx2 = merged_data['Apx_CW']
    apx3 = merged_data['Apx_RANDOM']

    # Controlla il vincitore per ogni istanza
    winner = []

    for i in range(len(instance)):
        t1_valid = t1[i] != "NaN" and apx1[i] != "NaN" and apx1[i] >= 1 and t1[i] != float('inf')
        t2_valid = t2[i] != "NaN" and apx2[i] != "NaN" and apx2[i] >= 1 and t2[i] != float('inf')
        t3_valid = t3[i] != "NaN" and apx3[i] != "NaN" and apx3[i] >= 1 and t3[i] != float('inf')

        if t1_valid and (t1[i] <= t2[i] or not t2_valid) and (t1[i] <= t3[i] or not t3_valid):
            winner.append('SWEEP')
        elif t2_valid and (t2[i] <= t1[i] or not t1_valid) and (t2[i] <= t3[i] or not t3_valid):
            winner.append('CW')
        elif t3_valid and (t3[i] <= t1[i] or not t1_valid) and (t3[i] <= t2[i] or not t2_valid):
            winner.append('RANDOM')
        else:
            winner.append('UNKNOWN')

    # Crea il grafico a torta
    plt.figure(figsize=(14, 10))
    labels = ['SWEEP', 'CW', 'RANDOM', 'UNKNOWN']
    sizes = [winner.count('SWEEP'), winner.count('CW'), winner.count('RANDOM'), winner.count('UNKNOWN')]
    colors = ['#FFC107', '#4CAF50', '#800080', '#F44336']  # Giallo, Verde, Viola, Rosso

    # Rimuovi le etichette con valore zero
    labels, sizes = zip(*((label, size) for label, size in zip(labels, sizes) if size != 0))

    # Esplosione delle sezioni
    explode = [0.05] * len(sizes)  # Leggera esplosione di tutte le sezioni

    # Grafico a torta con miglioramenti estetici
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, shadow=True, explode=explode,
            textprops={'fontsize': 20})

    # Etichetta del grafico
    plt.title("Distribuzione delle strategie vincenti", fontsize=24)

    # Mostra il grafico
    plt.show()


def plot_apx_all_random(file, title):
    """
    Crea un grafico basato sui dati della colonna APX nel file ALL_RANDOM
    :param file: file CSV
    :param title: titolo del grafico
    """
    plt.figure(figsize=(15, 10))  # Dimensione della figura

    # Carica il file CSV
    data = get_data_csv_all(file)

    # Ordina i dati in base alla colonna '#Node'
    data_sorted = data.sort_values(by='#Node')

    # Filtra i dati per rimuovere le righe con inf in APX
    data_filtered = data_sorted[data_sorted['APX'] != float('inf')]

    # Estrai i dati di interesse
    instance_names = data_filtered['Instance_Name']
    apx_values = data_filtered['APX']

    # Aggiungi una linea al grafico
    plt.plot(instance_names, apx_values, marker='o', linestyle='-', markersize=7, label='Random 1K')

    # Configura il grafico
    plt.title(title, fontsize=20)  # Aumenta la dimensione del titolo
    plt.xlabel('Istanze ordinate al crescere di N', fontsize=18)  # Aumenta la dimensione dell'etichetta dell'asse x
    plt.ylabel('APX', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse y
    plt.legend(fontsize=20)  # Legenda più grande

    # Imposta i valori dei tick dell'asse y per maggiore chiarezza
    y_min = min(apx_values)
    y_max = max(apx_values)
    plt.yticks(np.arange(y_min, y_max + 0.1, step=(y_max - y_min) / 50), fontsize=11)  # Imposta ticks e dimensione

    plt.xticks([], fontsize=12)  # Rimuove le etichette dell'asse x ma mantiene la label
    plt.grid(axis='y', linestyle='--', linewidth=0.7)
    # Mostra il grafico
    plt.show()


def apx_for_num_run_1plot_for_files(files, title, labels=['1', '2', '3', '4']):
    """
    Crea un grafico con una linea per ogni file basato sui dati della colonna APX
    :param files: lista di file CSV
    :param title: titolo del grafico
    :param labels: etichette per le linee
    """
    plt.figure(figsize=(15, 10))  # Dimensione della figura e DPI elevato

    markers = ['o', 's', '^', 'x']  # cerchio, quadrato, triangolo, croce
    #colors = ['b', '#FFA500', 'g', 'r']  # blu, arancione, verde, rosso
    linestyles = ['-', '--', '-.', ':']  # stili delle righe

    all_apx_values = []

    for i, file in enumerate(files):
        # Carica il file CSV
        data = get_data_csv_all(file)

        # Ordina i dati in base alla colonna '#Node'
        data_sorted = data.sort_values(by='#Node')

        # Filtra i dati per rimuovere le righe con inf in APX
        data_filtered = data_sorted[data_sorted['APX'] != float('inf')]

        # Estrai i dati di interesse
        instance_names = data_filtered['Instance_Name']
        apx_values = data_filtered['APX']

        all_apx_values.append(apx_values)  # Raccogli i valori APX per calcolare i tick dell'asse y

        # Aggiungi una linea al grafico
        plt.plot(instance_names, apx_values, marker=markers[i], linestyle=linestyles[i], markersize=7, label=labels[i])

    # Concatena tutti i valori APX in una singola Serie
    all_apx_values_series = pd.concat(all_apx_values)

    # Filtra i valori 'inf'
    all_apx_values_filtered = all_apx_values_series[all_apx_values_series != float('inf')]

    # Imposta i valori dei tick dell'asse y per maggiore chiarezza
    if not all_apx_values_filtered.empty:
        min_y = all_apx_values_filtered.min()
        max_y = all_apx_values_filtered.max()
        plt.yticks(np.arange(min_y, max_y + 0.05, step=(max_y - min_y) / 20))

    # Configura il grafico
    plt.title(title, fontsize=20)  # Aumenta la dimensione del titolo
    plt.xlabel('Istanze ordinate al crescere di N', fontsize=11)  # Aumenta la dimensione dell'etichetta dell'asse x
    plt.ylabel('APX', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse y
    plt.legend(fontsize=18)  # Legenda più grande
    #plt.xticks([])  # Nascondi le etichette dell'asse x
    plt.grid(axis='y', linestyle='--', linewidth=0.7)  # Solo griglie orizzontali

    # Mostra il grafico
    plt.show()


ANDREA = True
if ANDREA:
    #random_files = [SMALL_RANDOM_1K, SMALL_RANDOM_10K, SMALL_RANDOM_100K, SMALL_RANDOM_1M]
    random_5minVS1M = [RESULT_RANDOM + "small_Random_APX_and_Time_5min.csv", SMALL_RANDOM_1M]
    #apx_for_num_run_1plot_for_files(random_5minVS1M, "Confronto APX Random(5min) vs Random(1M) per istanze Small", ['5 min', '1 M'])
    #plot_apx_all_random(ALL_RANDOM_1K, "APX di Random 1K al crescere di n (Tutte le istanze)")


def graph_mip(title):
    data1 = pd.read_csv('Results/MIP/MIP_Solutions.csv', delimiter=',').sort_values(by="#Node")

    plt.figure(figsize=(10, 8))
    plt.bar(data1['Instance_Name'], data1['Execution_time'], color='skyblue')
    plt.title(title, fontsize=20)
    plt.xlabel('Istanze ordinate al crescere di N', fontsize=18)
    plt.ylabel('Secondi', fontsize=18)
    plt.xticks(rotation=90, fontsize=12)
    plt.yticks(fontsize=18)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


BOX_PLOT = False
if BOX_PLOT:
    boxPlot_apx(ALL_SWEEP, 'Apx_3Opt', "Sweep 3-Opt")
    boxPlot_apx(ALL_RANDOM_10K, 'APX', "Random 10K")
    boxPlot_apx(ALL_CW, 'APX', "Clarke & Wright")

ECX_TIME = True
if ECX_TIME:
    evaluate_time_CW_Sweep("Secondi", "Confronto dei Tempi di Esecuzione", "SMALL")
    evaluate_time_CW_Sweep("Secondi", "Confronto dei Tempi di Esecuzione", "MID")
    evaluate_time_CW_Sweep("Secondi", "Confronto dei Tempi di Esecuzione", "LARGE")
    #evaluate_2time_sweep("Secondi", "Confronto dei Tempi di Esecuzione", "MID")

WINNER_COST = False
if WINNER_COST:
    winner_algorithm()

PROBLEM_TRUCK = False
if PROBLEM_TRUCK:
    valuate_truck(ALL_SWEEP, "Sweep - Tutte le istanze")
    valuate_truck(ALL_CW, "Clarke & Wright - Tutte le istanze")
    valuate_truck(ALL_RANDOM_10K, " Random 1K - Tutte le istanze")
