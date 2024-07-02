# Classe Truck che identifica i veicoli nel VRP
# Attributi: numero min di veicoli,  numero massimo di veicoli, capacita dei veicoli

class Truck:
    def __init__(self, min_num, max_num, capacity):
        self.min_num = min_num
        self.max_num = max_num
        self.capacity = capacity

    def __str__(self):
        return f"Truck min:{self.min_num} Truck max: {self.max_num} capacity: {self.capacity}"

    def get_min_num(self):
        return self.min_num

    def get_max_num(self):
        return self.max_num

    def get_capacity(self):
        return self.capacity
