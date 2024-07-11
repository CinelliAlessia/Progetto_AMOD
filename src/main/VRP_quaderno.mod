# Sets
set V;  # Set of nodes
set V_CUST := V diff {0};  # Set of customer nodes, excluding the depot
set K;  # Set of vehicles

# Parameters
param num_truck; # Numero di veicoli minimo per servire tutti i clienti
param C >= 0;  # Capacity of each vehicle
param d{i in V} >= 0;  # Demand of each customer node
param c{i in V, j in V} >= 0;  # Distance (or cost) between nodes i and j

# Decision Variables
var x{i in V, j in V, k in K} binary;  # 1 if vehicle k travels from i to j, 0 otherwise
var y{i in V, k in K} binary;  # 1 if customer i is served by vehicle k, 0 otherwise
var u{i in V_CUST, k in K} >= 0;  # Auxiliary variables for subtour elimination

# Objective Function
minimize Total_Cost:
sum{k in K, i in V, j in V} c[i, j] * x[i, j, k];

# Constraints

# Each customer must be visited exactly once (Assegnamento)
subject to VisitOnce {i in V_CUST}:
sum{k in K} y[i, k] = 1;
# sum{k in K} y[0, k] := num_truck;

# Each vehicle must leave from and return to the depot (node 0)
# subject to DepotService {k in K}:
# sum{i in V_CUST} y[i, k] = 1;

# Flow conservation constraints (Flusso 1) e (Flusso 2)
subject to FlowConservation1 {i in V, k in K}:
sum{j in V} x[i, j, k] = y[i, k];

subject to FlowConservation2 {j in V, k in K}:
sum{i in V} x[i, j, k] = y[j, k];

# Capacity constraint for each vehicle (Capacità)
subject to CapacityConstraint {k in K}:
sum{i in V} d[i] * y[i, k] <= C;

# Subtour elimination constraints
subject to SubtourElimination {i in V_CUST, j in V_CUST, k in K: i != j}:
u[i, k] - u[j, k] + card(V_CUST) * x[i, j, k] <= card(V_CUST) - 1;

subject to SubtourStart {i in V_CUST, k in K}:
u[i, k] >= d[i] * y[i, k];

subject to SubtourBound {i in V_CUST, k in K}:
u[i, k] <= C * y[i, k];
