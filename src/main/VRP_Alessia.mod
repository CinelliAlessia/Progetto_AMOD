# Insiemi
set V;  # Insieme dei nodi
set V_CUST := V diff {0};  # Insieme dei nodi dei clienti, escludendo il deposito
set K;  # Insieme dei veicoli

# Parametri
param C >= 0;  # Capacità di ciascun veicolo
param d{V} >= 0;  # Domanda di ciascun nodo cliente
param c{V, V} >= 0;  # Distanza (o costo) tra i nodi i e j

# Variabili decisionali
var x{V, V, K} binary;  # 1 se il veicolo k viaggia da i a j, 0 altrimenti
var y{V, K} binary;  # 1 se il cliente i è servito dal veicolo k, 0 altrimenti
var u{V_CUST, K} >= 0;  # Variabili ausiliarie per eliminazione dei sottogiri

# Funzione obiettivo
minimize Total_Cost:
sum{k in K, i in V, j in V} c[i, j] * x[i, j, k];

# Vincoli

# Ogni cliente deve essere visitato esattamente una volta
subject to VisitOnce {i in V_CUST}:
sum{k in K} y[i, k] = 1;

# Ogni veicolo deve partire dal deposito (nodo 0) e tornare al deposito
subject to DepotService {k in K}:
sum{i in V_CUST} x[0, i, k] = 1;

subject to ReturnToDepot {k in K}:
sum{i in V_CUST} x[i, 0, k] = 1;

# Vincoli di conservazione del flusso
subject to FlowConservation1 {i in V, k in K}:
sum{j in V} x[i, j, k] = y[i, k];

subject to FlowConservation2 {j in V, k in K}:
sum{i in V} x[i, j, k] = y[j, k];

# Vincolo di capacità per ciascun veicolo
subject to CapacityConstraint {k in K}:
sum{i in V_CUST} d[i] * y[i, k] <= C;

# Vincoli di eliminazione dei sottogiri
subject to SubtourElimination {i in V_CUST, j in V_CUST, k in K: i != j}:
u[i,k] - u[j,k] + C * x[i,j,k] <= C - d[j];

# Vincoli per definire i valori iniziali delle variabili u
subject to UBound {i in V_CUST, k in K}:
d[i] <= u[i,k] <= C;
