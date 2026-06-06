from dataclasses import dataclass
from classes.map import Map

@dataclass
class Drone:
    nb_drones: int = Map().nb_drones