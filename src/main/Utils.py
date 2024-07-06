import os


def save_results_to_file(routes, cw_cost, directory, path):
    # Estrai il nome dell'istanza dal percorso
    instance_name = os.path.basename(path).split('/')[0]
    output_path = os.path.join(directory, f"{instance_name}.sol")

    # Assicurati che la directory di output esista
    os.makedirs(directory, exist_ok=True)

    # Formatta l'output
    output_lines = []
    for index, route in enumerate(routes):
        route_str = " ".join(str(node) for node in route[1:-1])  # Escludi l'ID del deposito
        output_lines.append(f"Route #{index + 1}: {route_str}")
    output_lines.append(f"Cost {cw_cost}")

    # Scrivi l'output nel file
    with open(output_path, 'w') as file:
        file.write("\n".join(output_lines))

    print(f"Results saved to {output_path}")


""" Calcola il costo totale di una lista di percorsi, sommando le distanze tra i nodi 
    roots: lista di percorsi, ognuno rappresentato come una lista di nodi
    dist: matrice delle distanze tra i nodi """


def calculateCost(roots, dist):
    total_cost = []

    for r in roots:
        cost = 0
        for i in range(len(r)-1):
            cost += dist[r[i]][r[i + 1]]

        #print(f"Route: {r} - Cost: {cost}")
        total_cost.append(cost)

    #print(f"Total cost: {sum(total_cost)}")
    return sum(total_cost)

