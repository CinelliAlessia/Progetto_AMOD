# Classe Node che identifica sia il client nel VRP che
# Attributi: id cliente, coordinate, domanda
import math

import numpy as np


class Node:
    
    def __init__(self, id, x, y, distance, is_depots, demand):
        self.angle = None
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.distance = distance
        self.is_depots = is_depots

    def __str__(self):
        return f"Node {self.id}, coord ({self.x}, {self.y}), demand: {self.demand}, distanza: {self.distance}, isDepots: {self.is_depots}"

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_demand(self):
        return self.demand

    def get_all_distance(self):
        return self.distance

    def get_distance(self, id):
        return self.distance[id]

    def get_is_depots(self):
        return self.is_depots

    def calculate_angle_to_depots(self, x, y):
        self.angle = np.arctan2(self.y - y, self.x - x) % (2 * np.pi)
        return self.angle
