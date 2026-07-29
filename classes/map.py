from classes.connection import Connection
from classes.hub import Hub
from dataclasses import dataclass
from typing import List, Dict, Tuple
from queue import PriorityQueue

@dataclass
class Map:
    hubs: Dict[str, Hub]
    connections: Dict[str, Connection]
    start: Hub
    end: Hub
    nb_drones: int
    
    def get_adjacency_list(self) -> Dict[str, List[Tuple[Hub, int]]]:
        adj = {v.name: [] for v in self.hubs.values()}
        for c in self.connections.values():
            if c.hub_a.zone_type == 'blocked' or c.hub_b.zone_type == 'blocked':
                continue
            weight_b = 2 if c.hub_b.zone_type == 'restricted' else (0 if c.hub_b.zone_type == 'priority' else 1)
            weight_a = 2 if c.hub_a.zone_type == 'restricted' else (0 if c.hub_a.zone_type == 'priority' else 1)
            adj[c.hub_a.name].append((c.hub_b, weight_b))
            adj[c.hub_b.name].append((c.hub_a, weight_a))
        return adj
