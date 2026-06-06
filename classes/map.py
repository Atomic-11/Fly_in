from classes.connection import Connection
from classes.hub import Hub
from dataclasses import dataclass, field
from typing import List

@dataclass
class Map:
    hubs: dict[str, Hub]
    connections: list[Connection]
    start: Hub
    end: Hub
    nb_drones: int