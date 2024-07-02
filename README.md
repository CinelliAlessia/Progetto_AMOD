# L'euristica di Clarke e Wright
L'euristica di Clarke e Wright è un algoritmo utilizzato per risolvere il problema del routing dei veicoli (VRP). Questo algoritmo è particolarmente utile quando si cerca di minimizzare la distanza totale percorsa dai veicoli.
Ecco una descrizione passo-passo dell'euristica di Clarke e Wright:
1. Inizialmente, ogni nodo (o cliente) è servito da un veicolo separato. Quindi, se ci sono N nodi, ci sono N rotte, ognuna delle quali va dal deposito al nodo e ritorna al deposito.

2. Calcola le economie di fusione per ogni possibile coppia di rotte. L'economia di fusione è la differenza tra la distanza totale delle due rotte separate e la distanza totale se le due rotte fossero fuse in un'unica rotta. Le economie di fusione possono essere calcolate utilizzando la formula: `economia = distanza(deposito, nodo1) + distanza(deposito, nodo2) - distanza(nodo1, nodo2)`.

3. Ordina le economie di fusione in ordine decrescente.

4. Inizia a fondere le rotte a partire dalla coppia con l'economia di fusione più alta. Fonde le rotte solo se la fusione non viola le restrizioni del problema (ad esempio, la capacità del veicolo).

5. Ripeti il passaggio 4 fino a quando non è più possibile fondere ulteriori rotte.

L'euristica di Clarke e Wright è un algoritmo greedy, il che significa che prende la decisione ottimale ad ogni passaggio sperando che queste decisioni locali ottimali portino a una soluzione globale ottimale. Tuttavia, come con tutte le euristiche, non c'è garanzia che l'euristica di Clarke e Wright produca la soluzione ottimale al problema del VRP.
