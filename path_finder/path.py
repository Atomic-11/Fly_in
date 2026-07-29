from queue import PriorityQueue
from typing import List, Tuple, Dict, Optional

from classes.map import Map
from classes.hub import Hub
from classes.connection import Connection
from classes.reservation import Reservation


class PathFinder:
    def __init__(self, map: Map) -> None:
        self.map = map

    def get_connection(self, a: str, b: str) -> Connection:
        return (
            self.map.connections.get(f"{a}-{b}")
            or self.map.connections.get(f"{b}-{a}")
        )

    def dijkstra_time_aware(
        self,
        start: Hub,
        end: Hub,
        start_turn: int,
        reservation: Reservation,
    ) -> List[Tuple[str, int]]:
        adj = self.map.get_adjacency_list()

        dist: Dict[Tuple[str, int], Tuple[int, int]] = {
            (start.name, start_turn): (0, 0)
        }
        came_from: Dict[Tuple[str, int], Optional[Tuple[str, int]]] = {
            (start.name, start_turn): None
        }

        pq: PriorityQueue = PriorityQueue()
        pq.put((0, 0, start.name, start_turn))

        while not pq.empty():
            turns_so_far, tiebreak_so_far, hub_name, turn = pq.get()

            if (turns_so_far, tiebreak_so_far) > dist.get(
                (hub_name, turn), (float("inf"), float("inf"))
            ):
                continue
            if hub_name == end.name:
                return self._reconstruct(came_from, (hub_name, turn))

            # --- wait move: stay at hub_name for one more turn ---
            wait_state = (hub_name, turn + 1)
            wait_turns = turns_so_far + 1
            wait_tiebreak = tiebreak_so_far
            if reservation.hub_count(hub_name, turn + 1) < self.map.hubs[hub_name].max_drones:
                if (wait_turns, wait_tiebreak) < dist.get(
                    wait_state, (float("inf"), float("inf"))
                ):
                    dist[wait_state] = (wait_turns, wait_tiebreak)
                    came_from[wait_state] = (hub_name, turn)
                    pq.put((wait_turns, wait_tiebreak, hub_name, turn + 1))

            # --- move to neighbors ---
            for next_hub, _weight in adj[hub_name]:
                time_cost = 2 if next_hub.zone_type == "restricted" else 1  # real turn cost, never 0
                priority_bonus = 0 if next_hub.zone_type == "priority" else 1  # tie-break only

                arrival_turn = turn + time_cost
                conn = self.get_connection(hub_name, next_hub.name)

                # hub capacity check at arrival turn
                if reservation.hub_count(next_hub.name, arrival_turn) >= next_hub.max_drones:
                    continue

                # link capacity check for every turn the drone occupies the connection
                link_key = f"{conn.hub_a.name}-{conn.hub_b.name}"
                blocked = False
                for t in range(turn, arrival_turn):
                    if reservation.link_count(link_key, t) >= conn.max_link_capacity:
                        blocked = True
                        break
                if blocked:
                    continue

                new_turns = turns_so_far + time_cost
                new_tiebreak = tiebreak_so_far + priority_bonus
                state = (next_hub.name, arrival_turn)

                if (new_turns, new_tiebreak) < dist.get(state, (float("inf"), float("inf"))):
                    dist[state] = (new_turns, new_tiebreak)
                    came_from[state] = (hub_name, turn)
                    pq.put((new_turns, new_tiebreak, next_hub.name, arrival_turn))

        return []

    def _reconstruct(
        self,
        came_from: Dict[Tuple[str, int], Optional[Tuple[str, int]]],
        end_state: Tuple[str, int],
    ) -> List[Tuple[str, int]]:
        path: List[Tuple[str, int]] = []
        state: Optional[Tuple[str, int]] = end_state
        while state is not None:
            path.append(state)
            state = came_from[state]
        path.reverse()
        return path