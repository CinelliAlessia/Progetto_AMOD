"""
Algoritmo Euristico di Clarke e Wright (1964) per il problema del Vehicle Routing Problem (VRP).
Utilizzato quando il numero di veicoli non è fissato a priori.

Quando due percorsi ${(0,…,i,0)}$ e ${(0,j,…,0)}$
possono essere fusi in modo fattibile in un unico percorso ${(0,…,i,j,…,0)}$,
si genera un risparmio (saves) ${s_{ij}=c_{i0}+c_{0j}-c_{ij}}$.

Passaggio 1. Calcola i risparmi ${s_{ij}=c_{i0}+c_{0j}-c_{ij}}$ per ${i,j=1,…,n}$ e ${i \neq j}$.
Crea ${n}$ percorsi di veicoli ${(0,i,0)}$ per ${i=1,…,n}$. Ordina i risparmi in modo non crescente.

Passaggio 2. Migliore fusione fattibile (versione parallela) Partendo dall'alto della lista dei risparmi, esegui quanto segue:
Dato un risparmio ${s_{ij}}$, determina se esistono due percorsi che possono essere fusi in modo fattibile:
Uno che inizia con ${(0,j)}$ Uno che termina con ${(i,0)}$ Combina questi due percorsi eliminando ${(0,j)}$ e ${(i,0)}$ e introducendo ${(i,j)}$.

L'algoritmo è basato su un'euristica di risparmio, che consiste nel calcolare il risparmio che si otterrebbe unendo due archi in un unico arco.
L'algoritmo di Clarke e Wright è molto efficiente e produce soluzioni di buona qualità, ma non garantisce di trovare la soluzione ottima.
Root da costruire: si servono nell'ordine in cui lo incontri, si possono successivamente fare degli scambi tra client
dello stesso cluster per migliorare la soluzione.
"""

import vrplib
import ParseInstances as parser


# Utilizzando i metodi definiti in ParseInstances.py,
# calcola i risparmi per ogni coppia di nodi e li ordina in modo decrescente
def calculate_saves_and_sort_descent(instance):
    dist = parser.get_edge_weight(instance)
    depots = parser.get_depots_index(instance)
    depotIndex = depots[0]  # !!!!! Assunto inizialmente un solo deposito, per semplicità di ragionamento
    n = parser.get_nodes_dimension(instance)
    saves = []
    for i in range(1, n):
        for j in range(i + 1, n):
            # formato save: (nodo, nodo, valore)
            saves.append((i, j, dist[depotIndex][i] + dist[j][depotIndex] - dist[i][j]))
    saves.sort(key=lambda x: x[2], reverse=True)
    return saves


def clarke_and_wright(path):
    # Passo 1: Calcolo saves ordinati in modo decrescente
    instance = parser.make_instance_from_path_name(path)
    saves = calculate_saves_and_sort_descent(instance)
    print(saves)

    # Passo 2: Devo definire un cammino per ogni cliente,
    # partendo dal deposito e tornando al deposito con lo stesso arco (depotIndex, i, depotIndex) per ogni i cliente
    # Inizializzo i cammini
    n = parser.get_nodes_dimension(instance)
    routes = []
    for i in range(1, n):
        routes.append([depotIndex, i, depotIndex])
