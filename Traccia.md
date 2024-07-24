**VRP**

1) **VRP** (Vehicle Routing Problem) è un problema di ottimizzazione che consiste nel determinare il percorso ottimale per un insieme di veicoli che devono servire un insieme di clienti, minimizzando il costo totale. Il problema è NP-hard e può essere formulato in diverse varianti, tra cui il VRP classico, il VRP con capacità, il VRP con finestre temporali, il VRP con pickup e delivery, il VRP con veicoli eterogenei e il VRP con veicoli multipli.

- Un paio di euristici:
  - Clarke e Wright, visto a lezione.
  - Sweep di facile implementazione, accennato solamente a lezione.
  
- Sweep: immagina di posizionare i clienti in un piano cartesiano, e di avere un veicolo che parte dall'origine deposito (0,0) e deve servire tutti i clienti. Immaginiamo una retta che spazza via il piano, come una lancetta che si muove e incontra mano mano nuovi clienti. 
  Questa procedura serve per fare un clustering dei client, cioè: i clienti incontrati via via a partire dal primo fino a saturare la capacità del veicolo. Quando si arriva a un cliente per il quale servire la sua domanda eccederebbe di capacità del singolo veicolo, la retta "fa un passo indietro" e così è formato il primo clustering. 
- Clarke e Wright: è un algoritmo di tipo costruttivo, che parte da una soluzione vuota e aggiunge iterativamente archi al grafo. L'algoritmo è basato su un'euristica di risparmio, che consiste nel calcolare il risparmio che si otterrebbe unendo due archi in un unico arco. L'algoritmo di Clarke e Wright è molto efficiente e produce soluzioni di buona qualità, ma non garantisce di trovare la soluzione ottima.
  Root da costruire: si servono nell'ordine in cui lo incontri, si possono successivamente fare degli scambi tra client dello stesso cluster per migliorare la soluzione.

Cosa fare: Confronto tra le due euristiche, tra costo complessivo delle soluzioni e tempo di calcolo, quanto ci vuole a risolvere il problema. 
è facile trovare le librerie con delle istanze di vrp, cosi da avere due vantaggi: per una parte abbiamo molto probabilmente il valore della soluzione ottima, e le istanze saranno raggruppate con delle caratteristiche. 

**Altri problemi**
2) Studio della qualità ottenuti dai rilassamenti, qualità di un bound. Esistono anche altri rilassamenti ma meglio lagrangiano, tipo ascesa duale.
3) Prestazioni dei tagli di Gomory, cosa succede se aggiungo iterativamente i tagli al PLI.
4) Algoritmi randomizzati, anche VRP, e usare un algoritmo random SEMPLICE (rapida esecuzione) vedendo che soluzione esce fuori, e confrontarla con la soluzione ottima. 
Iterando più volte il run dell'algoritmo random e valutando la soluzione migliore ottenuta con il valore della soluzione ottima o con algoritmi euristici.


Link ai dataset: http://www.vrp-rep.org/datasets.html


# Presentazione non più di 15-20 min
- Power Point: 
  - come sono fatte le istanze
  - Solo pezzi importanti di codice se lo riteniamo necessario
  - Risultati ottenuti, con tabelle o Grafici



Certo! Ecco la formulazione matematica del problema basato sul codice che hai fornito:

### Variabili
- \( x_{i,j,h} \) variabile binaria che è 1 se il veicolo \( h \) percorre l'arco da cliente \( i \) a cliente \( j \), 0 altrimenti.
- \( y_{i,h} \) variabile binaria che è 1 se il cliente \( i \) è servito dal veicolo \( h \), 0 altrimenti.
- \( u_{i,h} \) variabile continua che rappresenta la carica del veicolo \( h \) dopo aver servito il cliente \( i \).

### Parametri
- \( n \): numero totale di clienti, incluso il deposito (dove l'indice 0 rappresenta il deposito).
- \( k \): numero totale di veicoli.
- \( d_i \): domanda del cliente \( i \).
- \( Q \): capacità del veicolo.
- \( dist_{i,j} \): distanza tra i clienti \( i \) e \( j \).

### Funzione Obiettivo
Minimizzare la distanza totale percorsa dai veicoli:
\[ \text{Min} \sum_{i=0}^{n-1} \sum_{j=0}^{n-1} \sum_{h=0}^{k-1} dist_{i,j} \cdot x_{i,j,h} \]

### Vincoli
1. **Ogni cliente deve essere visitato esattamente una volta:**
   \[ \sum_{j=0, j \neq i}^{n-1} \sum_{h=0}^{k-1} x_{i,j,h} = y_{i,h} \quad \forall i \in \{1, \ldots, n-1\}, \; \forall h \in \{0, \ldots, k-1\} \]
   \[ \sum_{i=0, i \neq j}^{n-1} \sum_{h=0}^{k-1} x_{i,j,h} = y_{j,h} \quad \forall j \in \{1, \ldots, n-1\}, \; \forall h \in \{0, \ldots, k-1\} \]

2. **I veicoli devono partire e tornare al deposito:**
   \[ \sum_{j=1}^{n-1} x_{0,j,h} = 1 \quad \forall h \in \{0, \ldots, k-1\} \]
   \[ \sum_{j=1}^{n-1} x_{j,0,h} = 1 \quad \forall h \in \{0, \ldots, k-1\} \]

3. **Ogni cliente deve essere servito da esattamente un veicolo:**
   \[ \sum_{h=0}^{k-1} y_{i,h} = 1 \quad \forall i \in \{1, \ldots, n-1\} \]

4. **Vincoli di capacità (eliminazione dei subtour):**
   \[ u_{i,h} - u_{j,h} + Q \cdot x_{i,j,h} \leq Q - d_j \quad \forall i \in \{1, \ldots, n-1\}, \; \forall j \in \{1, \ldots, n-1\}, \; \forall h \in \{0, \ldots, k-1\} \text{ con } i \neq j \]

5. **Domanda del deposito è zero:**
   \[ u_{0,h} = 0 \quad \forall h \in \{0, \ldots, k-1\} \]