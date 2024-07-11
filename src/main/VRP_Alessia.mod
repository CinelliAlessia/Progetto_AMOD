# Sets
set V;  # Set of nodes
set V_CUST := V diff {0};  # Set of customer nodes, excluding the depot
set K;  # Set of vehicles

# Parameters
param C >= 0;  # Capacity of each vehicle
param d{i in V_CUST} >= 0;  # Demand of each customer node
param c{i in V, j in V} >= 0;  # Distance (or cost) between nodes i and j

# Decision Variables
var x{i in V, j in V, k in K} binary;  # 1 if vehicle k travels from i to j, 0 otherwise
var y{i in V_CUST, k in K} binary;  # 1 if customer i is served by vehicle k, 0 otherwise
var u{i in V_CUST, k in K} >= 0;  # Auxiliary variables for subtour elimination

# Objective Function
minimize TotalCost:
sum{k in K, i in V, j in V} c[i, j] * x[i, j, k];

# Constraints

# Each customer must be visited exactly once
subject to VisitOnce {i in V_CUST}:
sum{k in K} y[i, k] = 1;

# Each vehicle must leave from and return to the depot (node 0)
subject to DepotService {k in K}:
sum{i in V_CUST} y[i, k] = 1;

# Flow conservation constraints
subject to FlowConservation1 {i in V_CUST, k in K}:
sum{j in V} x[i, j, k] = y[i, k];

subject to FlowConservation2 {j in V_CUST, k in K}:
sum{i in V} x[i, j, k] = y[j, k];

# Capacity constraint for each vehicle
subject to CapacityConstraint {k in K}:
sum{i in V_CUST} d[i] * y[i, k] <= C;

# Subtour elimination constraints
subject to SubtourElimination {i in V_CUST, j in V_CUST, k in K: i != j}:
u[i, k] - u[j, k] + card(V_CUST) * x[i, j, k] <= card(V_CUST) - 1;

subject to SubtourStart {i in V_CUST, k in K}:
u[i, k] >= d[i] * y[i, k];

subject to SubtourBound {i in V_CUST, k in K}:
u[i, k] <= C * y[i, k];
