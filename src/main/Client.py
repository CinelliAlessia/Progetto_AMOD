# Classe client che identifica il cliente nel VRP
# Attributi: id cliente, coordinate, domanda

class Client:
    def __init__(self, id, x, y, demand, distance):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.distance = distance

    def __str__(self):
        return f"Client {self.id} ({self.x}, {self.y}) demand: {self.demand} distanza: {self.distance}"

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_demand(self):
        return self.demand

    def get_distance(self):
        return self.distance
