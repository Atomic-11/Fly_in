from classes.connection import Connection
from classes.hub import Hub
from dataclasses import dataclass, field
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
    
    def dijkstra(self, start: Hub, end: Hub, excluded: set[str]) -> List[str]:
        adj = self.get_adjacency_list()
        path = []
        came_from = {}
        dist = {v: float('inf') for v in adj}
        pq = PriorityQueue()
        dist[start.name] = 0
        came_from[start.name] = None
        pq.put((0, start.name))
        while not pq.empty():
            cost, hub = pq.get()
            if cost > dist[hub]:
                continue
            for next_hub, w in adj[hub]:
                if next_hub.name in excluded:
                    continue
                if dist[next_hub.name] > cost + w:
                    came_from[next_hub.name] = hub
                    dist[next_hub.name] = cost + w
                    pq.put((dist[next_hub.name], next_hub.name))
        v = end.name
        if dist[end.name] == float('inf'):
            return []
        while v is not None:
            path.append(v)
            v = came_from.get(v)
        path.reverse()
        return path

    def find_paths(self, start: Hub, end: Hub) -> List[List[str]]:
        possible_paths = []
        excluded = set()
        while True:
            path = self.dijkstra(start, end, excluded)
            if not path or path in possible_paths:
                break
            possible_paths.append(path)
            excluded.update(
                hub for hub in path[1:-1]
                if self.hubs[hub].max_drones == 1
            )
        return possible_paths