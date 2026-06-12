from classes.map import Map
from classes.drone import Drone
from classes.hub import Hub
from classes.connection import Connection
from typing import List, Optional, Dict

class Schedular:

    def create_drones(self, mp: Map, paths: List[List[str]]) -> List[Drone]:
        drones = []
        for i in range(mp.nb_drones):
            path = paths[i % len(paths)]
            start_turn = i // len(paths)
            drones.append(Drone(i + 1, start_turn, path, mp.start, 0, False, False, None))
        return drones
