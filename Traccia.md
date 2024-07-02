**VRP**

1) **VRP** (Vehicle Routing Problem) è un problema di ottimizzazione che consiste nel determinare il percorso ottimale per un insieme di veicoli che devono servire un insieme di clienti, minimizzando il costo totale. Il problema è NP-hard e può essere formulato in diverse varianti, tra cui il VRP classico, il VRP con capacità, il VRP con finestre temporali, il VRP con pickup e delivery, il VRP con veicoli eterogenei e il VRP con veicoli multipli.

- Un paio di euristici:
  - Clarke e Wright, visto a lezione.
  - Sweep di facile implementazione, accennato solamente a lezione.
  
- Sweep: immagina di posizionare i clienti in un piano cartesiano, e di avere un veicolo che parte dall'origine deposito (0,0) e deve servire tutti i clienti. Immaginiamo una retta che spazza via il piano, come una lancetta che si muove e incontra mano mano nuovi clienti. 
  Questa procedura serve per fare un clustering dei client, cioè: i clienti incontrati via via a partire dal primo fino a saturare la capacità del veicolo. Quando si arriva a un cliente per il quale servire la sua domanda eccederebbe di capacità del singolo veicolo, la retta "fa un passo indietro" e così è formato il primo clustering. 
- Clarke e Wright: è un algoritmo di tipo costruttivo, che parte da una soluzione vuota e aggiunge iterativamente archi al grafo. L'algoritmo è basato su un'euristica di risparmio, che consiste nel calcolare il risparmio che si otterrebbe unendo due archi in un unico arco. L'algoritmo di Clarke e Wright è molto efficiente e produce soluzioni di buona qualità, ma non garantisce di trovare la soluzione ottima.
  Root da costruire: si servono nell'ordine in cui lo incontri, si possono successivamente fare degli scambi stra client dello stesso cluster per migliorare la soluzione.

Cosa fare: Confronto tra le due euristiche, tra costo complessivo delle soluzioni e tempo di calcolo, quanto ci vuole a risolvere il problema. 
è facile trovare le librerie con delle istanze di vrp, cosi da avere due vantaggi: per una parte abbiamo molto probabilmente il valore della soluzione ottima, e le istanze saranno raggruppate con delle caratteristiche. 

**Altri problemi**
2) Studio della qualità ottenuti dai rilassamenti, qualità di un bound. Esistono anche altri rilassamenti ma meglio lagrangiano, tipo ascesa duale.
3) Prestazioni dei tagli di Gomory, cosa succede se aggiungo iterativamente i tagli al PLI.
4) Algoritmi randomizzati, anche vrp, e usare un algoritmo random SEMPLICE, e vedere che soluzione esce fuori, e confrontarla con la soluzione ottima. Iterando più volte il run dell'algoritmo random e si valuta la soluzione migliore ottenuta con il valore dela soluzione ottima o con algortmi euristici.
