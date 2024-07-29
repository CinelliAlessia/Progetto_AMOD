import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from Tests_Ale import get_data_csv_all

RESULT_SWEEP = 'Results/Heuristic_Solutions/Sweep/'
RESULT_CW = 'Results/Heuristic_Solutions/Clarke_&_Wright_run/'
RESULT_RANDOM = 'Results/Random_Solutions/'
RESULT_MIP = 'Results/MIP/'

# SWEEP
SMALL_SWEEP = RESULT_SWEEP + 'small_Sweep_APX_and_Time.csv'
MID_SMALL_SWEEP = RESULT_SWEEP + 'mid_small_Sweep_APX_and_Time.csv'
MID_SWEEP = RESULT_SWEEP + 'mid_Sweep_APX_and_Time.csv'
MID_LARGE_SWEEP = RESULT_SWEEP + 'mid_large_Sweep_APX_and_Time.csv'
LARGE_SWEEP = RESULT_SWEEP + 'large_Sweep_APX_and_Time_Timeout.csv'
X_LARGE_SWEEP = RESULT_SWEEP + 'x_large_Sweep_APX_and_Time_Timeout.csv'
SMALL_MID_SWEEP = RESULT_SWEEP + 'small_mid_sweep.csv'

# RANDOM
SMALL_RANDOM_1K = RESULT_RANDOM + "small_Random_APX_and_Time1K.csv"
SMALL_RANDOM_100K = RESULT_RANDOM + "small_Random_APX_and_Time100K.csv"
SMALL_RANDOM_1M = RESULT_RANDOM + "small_Random_APX_and_Time1M.csv"
SMALL_RANDOM_5min = RESULT_RANDOM + "small_Random_APX_and_Time_5min.csv"
MID_SMALL_RANDOM_5min = RESULT_RANDOM + "mid_small_Random_APX_and_Time_5min.csv"
MID_RANDOM_5min = RESULT_RANDOM + "mid_Random_APX_and_Time_5min.csv"
MID_LARGE_RANDOM_5min = RESULT_RANDOM + "mid_large_Random_APX_and_Time_5min.csv"
LARGE_RANDOM_5min = RESULT_RANDOM + "large_Random_APX_and_Time_5min.csv"
X_LARGE_RANDOM_5min = RESULT_RANDOM + "x_large_Random_APX_and_Time_5min.csv"
MID_SMALL_RANDOM_1K = RESULT_RANDOM + "mid_small_Random_APX_and_Time1K.csv"
MID_RANDOM_1K = RESULT_RANDOM + "mid_Random_APX_and_Time1K.csv"
MID_LARGE_RANDOM_1K = RESULT_RANDOM + "mid_large_Random_APX_and_Time1K.csv"
LARGE_RANDOM_1K = RESULT_RANDOM + "large_Random_APX_and_Time1K.csv"
X_LARGE_RANDOM_1K = RESULT_RANDOM + "x_large_Random_APX_and_Time1K.csv"

#10K
SMALL_RANDOM_10K = RESULT_RANDOM + "small_Random_APX_and_Time10K.csv"
MID_SMALL_RANDOM_10K = RESULT_RANDOM + "mid_small_Random_APX_and_Time10K.csv"
MID_RANDOM_10K = RESULT_RANDOM + "mid_Random_APX_and_Time10K.csv"
MID_LARGE_RANDOM_10K = RESULT_RANDOM + "mid_large_Random_APX_and_Time10K.csv"
LARGE_RANDOM_10K = RESULT_RANDOM + "large_Random_APX_and_Time10K.csv"
X_LARGE_RANDOM_10K = RESULT_RANDOM + "x_large_Random_APX_and_Time10K.csv"

# CW
SMALL_CW = RESULT_CW + 'small_CW_APX_and_Time.csv'
MID_SMALL_CW = RESULT_CW + 'mid_small_CW_APX_and_Time.csv'
MID_CW = RESULT_CW + 'mid_CW_APX_and_Time.csv'
MID_LARGE_CW = RESULT_CW + 'mid_large_CW_APX_and_Time.csv'
LARGE_CW = RESULT_CW + 'large_CW_APX_and_Time.csv'
X_LARGE_CW = RESULT_CW + 'x_large_CW_APX_and_Time.csv'

# MIP
SMALL_MIP = RESULT_MIP + 'small_MIP_Solutions.csv'
MID_SMALL_MIP = RESULT_MIP + 'mid_small_MIP_Solutions.csv'
MID_MIP = RESULT_MIP + 'mid_MIP_Solutions.csv'
MID_LARGE_MIP = RESULT_MIP + 'mid_large_MIP_Solutions.csv'

# ALL
ALL_MIP = RESULT_MIP + 'MIP_Solutions.csv'
ALL_SWEEP = RESULT_SWEEP + 'Sweep_all.csv'
ALL_CW = RESULT_CW + 'CW_All.csv'
ALL_RANDOM_1K = RESULT_RANDOM + 'All_Random_1K.csv'
ALL_RANDOM_10K = RESULT_RANDOM + 'All_Random_10K.csv'
ALL_RANDOM_5MIN = RESULT_RANDOM + 'All_Random_5min.csv'


def time_vs_capacity_1plot_for_files(files, title, labels=['1', '2', '3', '4']):
    """
    Crea un grafico con una linea per ogni file basato sui dati della colonna Execution_time
    :param files: lista di file CSV
    :param title: titolo del grafico
    :param labels: etichette per le linee
    """
    plt.figure(figsize=(15, 10))  # Dimensione della figura

    markers = ['o', 's', '^', 'x']  # cerchio, quadrato, triangolo, croce
    linestyles = ['-', '-', '-', '-']  # stili delle righe

    for i, file in enumerate(files):
        # Carica il file CSV
        data = pd.read_csv(file)

        # Se il file contiene il nome Sweep
        if 'Sweep' in file:
            print("Colonna rinominata")
            data = data.rename(columns={'Execution_time_2Opt': 'Execution_time'})

        # Controlla il tipo di dati della colonna '#Node'
        if not pd.api.types.is_numeric_dtype(data['#Node']):
            data['#Node'] = pd.to_numeric(data['#Node'], errors='coerce')

        # Ordina i dati in base alla colonna 'Capacity'
        data_sorted = data.sort_values(by='Capacity')

        # Filtra i dati per rimuovere le righe con inf o None in Execution_time
        data_filtered = data_sorted[~data_sorted['Execution_time'].isin([float('inf'), None])]

        # Estrai i dati di interesse
        instance_names = data_filtered['Instance_Name']
        execution_times = data_filtered['Execution_time']

        # Aggiungi una linea al grafico
        plt.plot(instance_names, execution_times, marker=markers[i], linestyle=linestyles[i], markersize=7, label=labels[i])

    # Configura il grafico
    plt.title(title, fontsize=20)  # Aumenta la dimensione del titolo
    plt.xlabel('Istanze ordinate al crescere di Capacity', fontsize=11)  # Aumenta la dimensione dell'etichetta dell'asse x
    plt.ylabel('Execution Time', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse y
    plt.legend(fontsize=18)  # Legenda più grande
    plt.xticks(rotation=90)  # Ruota le etichette dell'asse x per una migliore leggibilità
    plt.grid(axis='y', linestyle='--', linewidth=0.7)  # Solo griglie orizzontali

    # Mostra il grafico
    plt.show()


def apx_for_num_run_1plot_for_files(files, title, labels=['1', '2', '3', '4']):
    """
    Crea un grafico con una linea per ogni file basato sui dati della colonna APX
    :param files: lista di file CSV
    :param title: titolo del grafico
    :param labels: etichette per le linee
    """
    plt.figure(figsize=(15, 10))  # Dimensione della figura

    markers = ['o', 's', '^', 'x']  # cerchio, quadrato, triangolo, croce
    linestyles = ['-', '-', '-', '-']  # stili delle righe

    all_apx_values = []
    instance_node_map = {}

    # Raccogli informazioni su instance names e numero di nodi
    for file in files:
        data = get_data_csv_all(file)
        for _, row in data.iterrows():
            instance_node_map[row['Instance_Name']] = row['#Node']

    # Ordina le istanze in base al numero di nodi
    instance_names_all = sorted(instance_node_map.keys(), key=lambda x: instance_node_map[x])

    for i, file in enumerate(files):
        # Carica il file CSV
        data = get_data_csv_all(file)

        # se il file contiene il nome Sweep
        if 'Sweep' in file:
            print("Colonna rinominata")
            data = data.rename(columns={'Apx_2Opt': 'APX'})

        # Controlla il tipo di dati della colonna '#Node'
        if not pd.api.types.is_numeric_dtype(data['#Node']):
            data['#Node'] = pd.to_numeric(data['#Node'], errors='coerce')

        # Ordina i dati in base alla colonna '#Node'
        data_sorted = data.sort_values(by='#Node')

        # Filtra i dati per rimuovere le righe con inf o None in APX
        data_filtered = data_sorted[~data_sorted['APX'].isin([float('inf'), None])]

        # Estrai i dati di interesse
        instance_names = data_filtered['Instance_Name']
        apx_values = data_filtered['APX']
        # Crea un DataFrame per unire i dati basato sui nomi delle istanze
        df_temp = pd.DataFrame({'Instance_Name': instance_names, 'APX': apx_values})
        df_temp = df_temp.set_index('Instance_Name')

        # Allinea i dati con i nomi delle istanze
        df_temp = df_temp.reindex(instance_names_all)

        all_apx_values.append(df_temp['APX'])  # Raccogli i valori APX per calcolare i tick dell'asse y

        # Aggiungi una linea al grafico
        plt.plot(instance_names_all, df_temp['APX'], marker=markers[i], linestyle=linestyles[i], markersize=7, label=labels[i])

    # Concatena tutti i valori APX in una singola Serie
    all_apx_values_series = pd.concat(all_apx_values)

    # Imposta i valori dei tick dell'asse y per maggiore chiarezza
    if not all_apx_values_series.empty:
        min_y = all_apx_values_series.min()
        max_y = all_apx_values_series.max()
        plt.yticks(np.arange(min_y, max_y + 0.05, step=(max_y - min_y) / 20))

    # Configura il grafico
    plt.title(title, fontsize=20)  # Aumenta la dimensione del titolo
    plt.xlabel('Istanze ordinate al crescere di N', fontsize=18)  # Aumenta la dimensione dell'etichetta dell'asse x
    plt.ylabel('APX', fontsize=20)  # Aumenta la dimensione dell'etichetta dell'asse y
    plt.legend(fontsize=18)  # Legenda più grande
    plt.xticks([])
    plt.yticks(fontsize=18)
    #plt.xticks(rotation=90)  # Ruota le etichette dell'asse x per una migliore leggibilità
    plt.grid(axis='y', linestyle='--', linewidth=0.7)  # Solo griglie orizzontali

    # Mostra il grafico
    plt.tight_layout()
    plt.show()


def plot_apx_1file(file, title, legend):
    """
    Crea un grafico basato sui dati della colonna APX nel file ALL_RANDOM
    :param legend:
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
    plt.plot(instance_names, apx_values, marker='o', linestyle='-', markersize=7, label=legend)

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


ANDREA = True
if ANDREA:
    #random_files = [SMALL_RANDOM_1K, SMALL_RANDOM_10K, SMALL_RANDOM_100K, SMALL_RANDOM_1M]
    #random_5minVS1M = [RESULT_RANDOM + "small_Random_APX_and_Time_5min.csv", SMALL_RANDOM_1M]
    #apx_for_num_run_1plot_for_files(random_files, "Confronto APX Random(5min) vs Random(1M) per istanze Small", ['1K', '10K', '100K', '1M'])
    #plot_apx_1file('Results/MIP/MIP_Solutions.csv', "APX del modello MIP", 'MIP')
    all_small = [SMALL_CW, SMALL_SWEEP,SMALL_RANDOM_5min, SMALL_MIP]
    all_mid_small = [MID_SMALL_CW, MID_SMALL_SWEEP, MID_SMALL_RANDOM_5min, MID_SMALL_MIP]
    all_mid = [MID_CW, MID_SWEEP, MID_RANDOM_5min, MID_MIP]
    all_mid_large = [MID_LARGE_CW, MID_LARGE_SWEEP, MID_LARGE_RANDOM_5min, MID_LARGE_MIP]
    all_large = [LARGE_CW, LARGE_SWEEP, LARGE_RANDOM_5min]
    all_x_large = [X_LARGE_CW, X_LARGE_SWEEP, X_LARGE_RANDOM_5min]
    apx_for_num_run_1plot_for_files(all_small, "Confronto APX per istanze Small", ['CW', 'SWEEP-2Opt', 'RANDOM', 'MIP'])
    apx_for_num_run_1plot_for_files(all_mid_small, "Confronto APX per istanze Mid Small", ['CW', 'SWEEP-2Opt', 'RANDOM', 'MIP'])
    apx_for_num_run_1plot_for_files(all_mid, "Confronto APX per istanze Mid", ['CW', 'SWEEP-2Opt', 'RANDOM', 'MIP'])
    apx_for_num_run_1plot_for_files(all_mid_large, "Confronto APX per istanze Mid Large", ['CW', 'SWEEP-2Opt', 'RANDOM', 'MIP'])
    apx_for_num_run_1plot_for_files(all_large, "Confronto APX per istanze Large", ['CW', 'SWEEP-2Opt', 'RANDOM'])
    apx_for_num_run_1plot_for_files(all_x_large, "Confronto APX per istanze X Large", ['CW', 'SWEEP-2Opt', 'RANDOM'])

