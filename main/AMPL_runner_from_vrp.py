import ParseInstances as ip
from amplpy import AMPL, Environment
from ParseInstances import get_truck, get_nodes_dimension, get_node_demands, get_edge_weight, get_depots_index
from AMPL_runner_from_dat import calculate_routes_from_matrix


def solve_vrp_with_ampl_andrea(instance):
    # 1. Leggere i dati dell'istanza utilizzando le tue funzioni esistenti
    num_of_nodes = get_nodes_dimension(instance)
    print("Numero di nodi:", num_of_nodes)
    demands = get_node_demands(instance)
    print("Domande dei nodi:", demands)

    truck = get_truck(instance)
    edge_weight = get_edge_weight(instance)
    list_of_depots = get_depots_index(instance)

    # Aggiungi il percorso di installazione di AMPL
    ampl_env = Environment(r"C:\Users\andre\AMPL")
    ampl = AMPL(ampl_env)

    # 2. Creare il modello AMPL
    with open('VRP_Andrea.mod', 'r') as f:
        model_content = f.read()
    ampl.eval(model_content)

    # Definizione dei dati letti dall'istanza VRP
    ampl.set['V'] = range(1, num_of_nodes+1)
    print(ampl.getData('V'))
    # ampl.set['V_CUST'] = range(2, num_of_nodes)  # Assicurati che V_CUST sia correttamente definito
    # ampl.param['num_truck'] = truck.get_min_num()
    ampl.set['K'] = range(1, truck.get_min_num()+1)
    print(ampl.getData('K'))
    ampl.param['C'] = truck.get_capacity()
    print(ampl.getData('C'))
    ampl.param['d'] = {i + 1: demands[i] for i in range(num_of_nodes)}  # Imposta i da 1 a num_of_nodes
    print(ampl.getData('d'))
    big_m = 1000000  # Esempio di valore Big M, puoi impostarlo in base alle tue esigenze
    ampl.param['c'] = {(i+1, j+1): edge_weight[i][j] if edge_weight[i][j] != 0 else big_m for i in range(num_of_nodes) for j in range(num_of_nodes)}
    print(ampl.getData('c'))

    # 3. Specifica del solver (ad esempio, CPLEX) con limite di tempo
    ampl.setOption('solver', 'cplex')
    ampl.setOption('cplex_options', 'timelimit=180')  # Limite di 180 secondi (3 minuti

    # 4. Risoluzione del modello AMPL
    ampl.solve()

    # 5. Recupero dei risultati
    total_cost = ampl.getObjective('Total_Cost').value()
    print("Costo totale del percorso:", total_cost)

    # Recupera i valori delle variabili x e y
    x_values = ampl.getVariable('x').getValues().toPandas()
    y_values = ampl.getVariable('y').getValues().toPandas()

    # Chiudi AMPL
    ampl.close()

    routes = calculate_routes_from_matrix(x_values, y_values)
    for i, tour in enumerate(routes, 1):
        print(f"Tour {i}: {routes}")

    return routes, total_cost


instance_path = "../resources/vrplib/Instances/E-n13-k4.vrp"
# Esempio di utilizzo
make_instance = ip.make_instance_from_path_name(instance_path)
optimal_cost = solve_vrp_with_ampl_andrea(make_instance)
print(f"Costo totale ottimale: {optimal_cost}")
