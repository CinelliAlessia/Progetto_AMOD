# Classe Depot che identifica i depositi nel VRP
# Attributi: id, coordinate

class Depot:

    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return f"Depot {self.id} ({self.x}, {self.y})"

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
