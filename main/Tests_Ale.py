import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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


def path_from_size(size):
    csv_files = {
        'SMALL': [SMALL_CW, SMALL_SWEEP, SMALL_RANDOM_10K, SMALL_MIP],
        'MID_SMALL': [MID_SMALL_CW, MID_SMALL_SWEEP, MID_SMALL_RANDOM_10K, MID_SMALL_MIP],
        'MID': [MID_CW, MID_SWEEP, MID_RANDOM_10K, MID_MIP],
        'MID_LARGE': [MID_LARGE_CW, MID_LARGE_SWEEP, MID_LARGE_RANDOM_10K, MID_LARGE_MIP],
        'LARGE': [LARGE_CW, LARGE_SWEEP, LARGE_RANDOM_10K, None],
        'X_LARGE': [X_LARGE_CW, X_LARGE_SWEEP, X_LARGE_RANDOM_10K, None],
        'ALL': [ALL_CW, ALL_SWEEP, ALL_RANDOM_5MIN, ALL_MIP]
    }

    return csv_files.get(size, [None, None, None, None])


def get_data_csv_all(file):
    return pd.read_csv(file, delimiter=',')


def box_plot(path_file, column, title, ordered_sizes):
    # Carica il file CSV
    df = get_data_csv_all(path_file)

    df_selected = df[['Size', column]].dropna(subset=[column])  # Seleziona solo le colonne necessarie
    df_filtered = df_selected[df_selected['Size'].isin(ordered_sizes)]  # Filtra per le dimensioni specificate in ordered_sizes e rimuove i valori Nan

    # Raggruppa per 'Size' e crea una lista di valori di 'column' per ogni 'Size'
    grouped_data = df_filtered.groupby('Size')[column].apply(list).to_dict()
    boxplot_data = [grouped_data.get(size, []) for size in ordered_sizes]

    plt.figure(figsize=(10, 6))
    plt.boxplot(boxplot_data, tick_labels=ordered_sizes)
    plt.title(f'Apx per Size - {title}')
    plt.xlabel('')
    plt.ylabel('Apx')

    all_values = [value for values in grouped_data.values() for value in values if value != float('inf') and value is not None and not np.isnan(value)]
    if all_values:
        min_y, max_y = min(all_values), max(all_values)
        print(f"min_y: {min_y}, max_y: {max_y}")

        plt.ylim(min_y - 0.05 * (max_y - min_y), max_y + 0.05 * (max_y - min_y))
        step = (max_y - min_y) / 10 or 1
        plt.yticks(np.arange(min_y, max_y + step, step))

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def evaluate_apx_sweep(csv_file, title):
    data = pd.read_csv(csv_file, delimiter=',').sort_values(by="#Node")
    apx_columns = ['Apx_NoOpt', 'Apx_2Opt', 'Apx_3Opt']
    instance_name, nodes = data['Instance_Name'], data['#Node']

    plt.figure(figsize=(10, 6))
    for col, marker, linestyle in zip(apx_columns, ['o', 's', 'x'], ['-', '--', '-.']):
        plt.plot(instance_name, data[col], marker=marker, linestyle=linestyle, label=col.replace('_', ' '))

    for i in range(0, len(instance_name), 8):
        plt.annotate(nodes.iloc[i], (instance_name.iloc[i], data[apx_columns[0]].iloc[i]), textcoords="offset points", xytext=(5, 5))

    plt.title(title, fontsize=16)
    plt.legend(fontsize=16)
    plt.ylabel('APX', fontsize=16)
    plt.grid(True)

    y_min, y_max = data[apx_columns].min().min(), data[apx_columns].max().max()
    plt.xticks(np.arange(len(instance_name), step=5), rotation=90)
    plt.yticks(np.arange(y_min, y_max, step=(y_max - y_min) / 25))

    plt.tight_layout()
    plt.show()


def valuate_truck(csv_file, title):
    data = pd.read_csv(csv_file, delimiter=',')
    truck, used_truck = data['#Truck'], data['Used_Truck']

    feasible = sum((used_truck <= truck) & (used_truck != 0) | (truck == 0))
    infeasible = len(truck) - feasible

    plt.figure(figsize=(12, 10))
    labels, sizes = ['Feasible', 'Infeasible'], [feasible, infeasible]
    colors, explode = ['#4CAF50', '#F44336'], (0.1, 0)

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, shadow=True, textprops={'fontsize': 24})
    plt.title(title, fontsize=28)
    plt.show()


def plot_execution_times(merged_data, columns, title, xlabel, ylabel):
    nodes = merged_data['Instance_Name']
    plt.figure(figsize=(14, 10))

    for col, marker, linestyle, label in columns:
        plt.plot(nodes, merged_data[col], marker=marker, linestyle=linestyle, label=label)

    y_min, y_max = min([merged_data[col].min() for col, _, _, _ in columns]), max([merged_data[col].max() for col, _, _, _ in columns])
    plt.title(title, fontsize=20)
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(ylabel, fontsize=20)
    plt.legend(fontsize=20)
    plt.grid(True)

    plt.xticks("")
    plt.yticks(np.arange(y_min, y_max + 0.001, step=(y_max - y_min) / 20), fontsize=18)

    plt.tight_layout()
    plt.show()


def evaluate_all_time(column, title, size, sorting, mip=False):
    csv_file1, csv_file2, csv_file3, csv_file4 = path_from_size(size)
    data1 = pd.read_csv(csv_file1, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time': 'Execution_time_CW'})
    data2 = pd.read_csv(csv_file2, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time_2Opt': 'Execution_time_SWEEP'})
    data3 = pd.read_csv(csv_file3, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time': 'Execution_time_RANDOM'})

    if mip:
        data4 = pd.read_csv(csv_file4, delimiter=',').sort_values(by="Capacity").rename(columns={'Execution_time': 'Execution_time_MIP'})
        merged_data = data1[['Instance_Name', sorting, 'Execution_time_CW']].merge(data2[['Instance_Name', sorting, 'Execution_time_SWEEP']], on='Instance_Name').merge(data3[['Instance_Name', sorting, 'Execution_time_RANDOM']], on='Instance_Name').merge(data4[['Instance_Name', sorting, 'Execution_time_MIP']], on='Instance_Name').sort_values(by=sorting)
        columns = [('Execution_time_CW', 's', '--', 'CW'), ('Execution_time_SWEEP', 'o', '-', 'SWEEP 2-Opt'), ('Execution_time_RANDOM', 'x', '-.', 'RANDOM 10K'), ('Execution_time_MIP', 'v', ':', 'MIP')]
    else:
        merged_data = data1[['Instance_Name', sorting, 'Execution_time_CW']].merge(data2[['Instance_Name', sorting, 'Execution_time_SWEEP']], on='Instance_Name').merge(data3[['Instance_Name', sorting, 'Execution_time_RANDOM']], on='Instance_Name').sort_values(by=sorting)
        columns = [('Execution_time_CW', 's', '--', 'CW'), ('Execution_time_SWEEP', 'o', '-', 'SWEEP 2-Opt'), ('Execution_time_RANDOM', 'x', '-.', 'RANDOM 10K')]

    plot_execution_times(merged_data, columns, title, f'Istanze {size}', column)


def evaluate_time_CW_Sweep(column, title, size, sorting):
    csv_file1, csv_file2, _, _ = path_from_size(size)
    data1 = pd.read_csv(csv_file1, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time': 'Execution_time_CW'})
    data2 = pd.read_csv(csv_file2, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time_2Opt': 'Execution_time_SWEEP'})

    merged_data = data1[['Instance_Name', sorting, 'Execution_time_CW']].merge(data2[['Instance_Name', sorting, 'Execution_time_SWEEP']], on='Instance_Name')
    if f'{sorting}_x' in merged_data.columns and f'{sorting}_y' in merged_data.columns:
        merged_data[sorting] = merged_data[f'{sorting}_x'].combine_first(merged_data[f'{sorting}_y'])
        merged_data.drop(columns=[f'{sorting}_x', f'{sorting}_y'], inplace=True)
    merged_data.sort_values(by=sorting, inplace=True)

    columns = [('Execution_time_CW', 's', '--', 'CW'), ('Execution_time_SWEEP', 'o', '-', 'SWEEP 2-Opt')]

    plot_execution_times(merged_data, columns, title, f'Istanze {size}', column)


def get_merged_data_cw_random(csv_file1, csv_file2, sorting):
    data1 = pd.read_csv(csv_file1, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time': 'Execution_time_CW'})
    data3 = pd.read_csv(csv_file2, delimiter=',').sort_values(by=sorting).rename(columns={'Execution_time': 'Execution_time_RANDOM'})

    merged_data = data1[['Instance_Name', sorting, 'Execution_time_CW']].merge(data3[['Instance_Name', sorting, 'Execution_time_RANDOM']], on='Instance_Name').sort_values(by=sorting)

    return merged_data


def evaluate_time_CW_Random(column, title, size, sorting):
    csv_file1, _, csv_file3, _ = path_from_size(size)
    merged_data = get_merged_data_cw_random(csv_file1, csv_file3, sorting)
    columns = [('Execution_time_CW', 's', '--', 'CW'), ('Execution_time_RANDOM', 'x', '-.', 'RANDOM 10K')]

    plot_execution_times(merged_data, columns, title, f'Istanze {size}', column)


def winner_algorithm():
    # Carica i dati dai file CSV usando il delimitatore ';'
    data1 = pd.read_csv(ALL_SWEEP, delimiter=',').sort_values(by="#Node")
    data2 = pd.read_csv(ALL_CW, delimiter=',').sort_values(by="#Node")
    data3 = pd.read_csv(ALL_RANDOM_5MIN, delimiter=',').sort_values(by="#Node")
    data4 = pd.read_csv(ALL_MIP, delimiter=',').sort_values(by="#Node")

    data1 = data1.rename(columns={
        'Cost_3Opt': 'Cost_SWEEP',
        'Apx_3Opt': 'Apx_SWEEP'})
    data2 = data2.rename(columns={
        'CW_cost': 'Cost_CW',
        'APX': 'Apx_CW'})
    data3 = data3.rename(columns={
        'BEST_Random': 'Cost_RANDOM',
        'APX': 'Apx_RANDOM'})
    data4 = data4.rename(columns={
        'Incumbent': 'Cost_MIP',
        'APX': 'Apx_MIP'})

    # Unisci i dati sui nodi
    merged_data = data1[['Instance_Name', 'Cost_SWEEP', 'Apx_SWEEP']].merge(
        data2[['Instance_Name', 'Cost_CW', 'Apx_CW']],
        on='Instance_Name',
        how='outer'
    ).merge(
        data3[['Instance_Name', 'Cost_RANDOM', 'Apx_RANDOM']],
        on='Instance_Name',
        how='outer'
    ).merge(
        data4[['Instance_Name', 'Cost_MIP', 'Apx_MIP']],
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
    t4 = merged_data['Cost_MIP']

    apx1 = merged_data['Apx_SWEEP']
    apx2 = merged_data['Apx_CW']
    apx3 = merged_data['Apx_RANDOM']
    apx4 = merged_data['Apx_MIP']

    # Controlla il vincitore per ogni istanza
    winner = []

    for i in range(len(instance)):
        t1_valid = t1[i] != "NaN" and apx1[i] != "NaN" and apx1[i] >= 1 and t1[i] != float('inf')
        t2_valid = t2[i] != "NaN" and apx2[i] != "NaN" and apx2[i] >= 1 and t2[i] != float('inf')
        t3_valid = t3[i] != "NaN" and apx3[i] != "NaN" and apx3[i] >= 1 and t3[i] != float('inf')
        t4_valid = t4[i] != "NaN" and apx4[i] != "NaN" and apx4[i] >= 1 and t4[i] != float('inf') and t4[i] is not None

        if t1_valid and (t1[i] <= t2[i] or not t2_valid) and (t1[i] <= t3[i] or not t3_valid) and (t1[i] <= t4[i] or not t4_valid):
            winner.append('SWEEP')
        elif t2_valid and (t2[i] <= t1[i] or not t1_valid) and (t2[i] <= t3[i] or not t3_valid) and (t2[i] <= t4[i] or not t4_valid):
            winner.append('CW')
        elif t3_valid and (t3[i] <= t1[i] or not t1_valid) and (t3[i] <= t2[i] or not t2_valid) and (t3[i] <= t4[i] or not t4_valid):
            winner.append('RANDOM')
        elif t4_valid and (t4[i] <= t1[i] or not t1_valid) and (t4[i] <= t2[i] or not t2_valid) and (t4[i] <= t3[i] or not t3_valid):
            winner.append('MIP')
        else:
            winner.append('UNKNOWN')

    # Crea il grafico a torta
    plt.figure(figsize=(14, 10))
    labels = ['SWEEP', 'CW', 'RANDOM', 'MIP', 'UNKNOWN']
    sizes = [winner.count('SWEEP'), winner.count('CW'), winner.count('RANDOM'), winner.count('MIP'), winner.count('UNKNOWN')]
    colors = ['#FFC107', '#4CAF50', '#800080', '#00BFFF', '#F44336']  # Giallo, Verde, Viola, Celeste, Rosso

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
    plt.tight_layout()
    plt.show()


def graph_mip(title, x_label, y_label):
    data1 = pd.read_csv('Results/MIP/MIP_Solutions.csv', delimiter=',').sort_values(by="#Node")

    # Filtrare righe dove 'APX' non è infinito e non è NaN
    data_filtered = data1[(data1['APX'] != float('inf')) & (pd.notna(data1['APX']))]

    plt.figure(figsize=(10, 4))
    plt.plot(data_filtered['Instance_Name'], data_filtered['APX'], marker='o', linestyle='-', markersize=5)
    #plt.bar(data1['Instance_Name'], data1['Execution_time'], color='skyblue')

    plt.title(title, fontsize=20)
    plt.xlabel(x_label, fontsize=18)
    plt.ylabel(y_label, fontsize=18)

    y_min = min(data_filtered['APX'])
    y_max = max(data_filtered['APX'])

    plt.xticks("")
    plt.yticks(np.arange(y_min, y_max + 0.05, step=(y_max - y_min) / 10), fontsize= 18)
    plt.tight_layout()
    plt.grid(True)
    plt.show()


BOX_PLOT = False
if BOX_PLOT:
    box_plot(ALL_SWEEP, 'Apx_3Opt', "Sweep 3-Opt",   ['small', 'mid_small', 'mid', 'mid_large', 'large', 'x_large'])
    box_plot(ALL_RANDOM_5MIN, 'APX', "Random 5 MIN", ['small', 'mid_small', 'mid', 'mid_large', 'large', 'x_large'])
    box_plot(ALL_CW, 'APX', "Clarke & Wright", ['small', 'mid_small', 'mid', 'mid_large', 'large'])
    box_plot(ALL_MIP, 'APX', "MIP", ['small', 'mid_small', 'mid'])
    box_plot(ALL_MIP, 'APX', "MIP", ['small', 'mid_small'])

ECX_TIME = True
if ECX_TIME:
    sort_by = "#Node"
    #evaluate_time_CW_Sweep("Secondi", "Confronto dei Tempi di Esecuzione", "SMALL", sort_by)
    #evaluate_time_CW_Sweep("Secondi", "Confronto dei Tempi di Esecuzione", "MID", sort_by)
    evaluate_time_CW_Sweep("Secondi", "Confronto dei Tempi di Esecuzione", "LARGE", sort_by)
    evaluate_all_time("Secondi", "Confronto dei Tempi di Esecuzione", "SMALL", sort_by)
    #evaluate_all_time("Secondi", "Confronto dei Tempi di Esecuzione", "SMALL", sortby)
    #evaluate_all_time("Secondi", "Confronto dei Tempi di Esecuzione", "MID_SMALL", sortby)
    #evaluate_all_time("Secondi", "Confronto dei Tempi di Esecuzione", "MID", sortby)
    #evaluate_all_time("Secondi", "Confronto dei Tempi di Esecuzione", "MID_LARGE", sortby)
    #evaluate_all_time("Secondi", "Confronto dei Tempi di Esecuzione", "LARGE", sortby)

WINNER_COST = False
if WINNER_COST:
    winner_algorithm()

PROBLEM_TRUCK = False
if PROBLEM_TRUCK:
    valuate_truck(ALL_SWEEP, "Sweep - Tutte le istanze")
    valuate_truck(ALL_CW, "Clarke & Wright - Tutte le istanze")
    valuate_truck(ALL_RANDOM_1K, " Random 1K - Tutte le istanze")
    valuate_truck(ALL_RANDOM_5MIN, " Random 5 min - Tutte le istanze")

APX_SWEEP = False
if APX_SWEEP:
    evaluate_apx_sweep(SMALL_SWEEP, "Performance di Sweep - Istanze Small")
    evaluate_apx_sweep(MID_SWEEP, "Performance di Sweep - Istanze Mid")
    evaluate_apx_sweep(LARGE_SWEEP, "Performance di Sweep - Istanze Large")

GRAPH_MIP = False
if GRAPH_MIP:
    graph_mip("APX MIP", "Istanze", "APX")