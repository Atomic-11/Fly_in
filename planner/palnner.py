from typing import List, Dict, Tuple
from classes.map import Map
from classes.drone import Drone
from classes.reservation import Reservation
from path_finder.path import PathFinder
from planner.state_builder import build_state


class Planner:
    def __init__(self, map: Map) -> None:
        self.map = map
        self.reservation = Reservation()
        self.pathfinder = PathFinder(map)
        self.timed_paths: Dict[int, List[Tuple[str, int]]] = {}

    def create_drones(self) -> List[Drone]:
        drones = []
        for i in range(self.map.nb_drones):
            drones.append(
                Drone(
                    did=i + 1,
                    start_turn=0,
                    path=[],
                    cur_hub=self.map.start,
                    path_index=0,
                    arrived=False,
                    in_transit=False,
                    destination=None,
                )
            )
        return drones

    def reserve_path(self, timed_path: List[Tuple[str, int]]) -> None:
        for (h1, t1), (h2, t2) in zip(timed_path, timed_path[1:]):
            if h1 == h2:
                # wait-hop
                if h2 not in (self.map.start.name, self.map.end.name):
                    self.reservation.reserve_hub(h2, t2)
                continue

            # move-hop: reserve link for all transit turns
            conn = self.pathfinder.get_connection(h1, h2)
            link_key = f"{conn.hub_a.name}-{conn.hub_b.name}"
            for t in range(t1, t2):
                self.reservation.reserve_link(link_key, t)

            # reserve arrival hub (unless start/end)
            if h2 not in (self.map.start.name, self.map.end.name):
                self.reservation.reserve_hub(h2, t2)

    def plan(self) -> List[Dict[int, str]]:
        drones = self.create_drones()
        for d in drones:
            timed_path = self.pathfinder.dijkstra_time_aware(
                start=d.cur_hub,
                end=self.map.end,
                start_turn=d.start_turn,
                reservation=self.reservation,
            )
            self.timed_paths[d.did] = timed_path
            self.reserve_path(timed_path)
            d.path = [h for h, _ in timed_path]

        return build_state(self.timed_paths, self.map.end.name)