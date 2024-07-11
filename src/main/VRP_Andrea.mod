# Modello dell'CVRP, con variabili decisionali a 3 indici
# Senza bisogno di preprocessamento dei Gamma(minimo num veicoli per servire i clienti) per ogni Subtour

model;

# Sets
set V;  # Set of nodes
set V_CUST := V diff {1};  # Set of customer nodes, excluding the depot
set K;  # Set of vehicles

# Parameters
param C;               # Capacità del singolo veicolo
param d{V};       # Domanda dei clienti
param c{V, V};         # Costo di percorrenza tra i vertici

# Decision Variables
var x{V, V, K} binary;  # x[i,j,h] = 1 se il veicolo h percorre l'arco (i,j)
var y{V, K} binary;     # y[i,h] = 1 se il veicolo h serve il cliente i

# Objective Function
minimize Total_Cost:
sum {h in K, i in V, j in V} c[i,j] * x[i,j,h];

# Constraints

# 1. Ogni cliente deve essere servito solo una volta
subject to Visit_Once {i in V_CUST}:
sum {h in K} y[i,h] = 1;

# 2. Il deposito deve essere servito esattamente k volte
subject to Depot_Service:
sum {h in K} y[1,h] = card(K);

# 3. Vincoli di flusso
subject to Flow_In {i in V, h in K}:
sum {j in V} x[i,j,h] = y[i,h];

subject to Flow_Out {j in V, h in K}:
sum {i in V} x[i,j,h] = y[j,h];

# 4. Vincoli di capacità
subject to Capacity {h in K}:
sum {i in V_CUST} d[i] * y[i,h] <= C;

# 5. Vincoli di eliminazione dei sottotour corretto
subject to Subtour_Elimination {h in K}:
forall {S in 2..card(V_CUST)} {
    forall {subset in {S in V_CUST : subset(S, 2)}: card(S) == S} {
        sum {i in S, j in S: i != j} x[i,j,h] >= card(S) * y[S,h] - card(S) + 1;
    }
}
