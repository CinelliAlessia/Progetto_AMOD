Introduction
============

Created by Geoffrey De Smet.
Shared under the Apache License 2.0.

References
==========

To reference these files in papers, please use this BibTeX reference:

@manual{optaplanner,
  author        = {Geoffrey De Smet et al},
  title         = {OptaPlanner VRP examples: Belgium 2017 dataset},
  organization  = {Red Hat and the community},
  url           = {https://www.optaplanner.org},
  note          = {OptaPlanner is an open source constraint satisfaction solver in Java}
}

NAME: Il nome dell'istanza.
COMMENT: Un commento o una descrizione dell'istanza.
TYPE: Il tipo di problema. In questo caso, CVRP indica un problema di routing dei veicoli con capacità.
DIMENSION: Il numero di nodi nel problema, inclusi il deposito e i clienti.
EDGE_WEIGHT_TYPE: Il tipo di pesi sugli archi. EUC_2D indica che i pesi sono calcolati come la distanza euclidea in due dimensioni.
CAPACITY: La capacità dei veicoli.
NODE_COORD_SECTION: Una lista di nodi con le loro coordinate geografiche e i nomi delle città.
DEMAND_SECTION: Una lista che rappresenta la domanda di ogni cliente.
DEPOT_SECTION: I nodi che rappresentano i depositi.