from classes.map import Map
from classes.drone import Drone
from classes.hub import Hub
from classes.connection import Connection
from typing import List, Dict, Tuple
from ui.visualizer import Visualizer
from configs.parser import Parser, ParserError
from simulation.schedular import Schedular

class Engine:
    cur_turn: int = 0
    future_arv: Dict[Tuple[str, int], int] = {}

    def simulate(self, map: Map, drones: List[Drone]) -> List[Dict[int, str]]:
        state: List[Dict[int, str]] = []
        for d in drones:
            map.start.current_drones.append(d)
        state.append({d.did: d.cur_hub.name for d in drones})
        while not all(d.arrived for d in drones):
            self.cur_turn += 1
            moves = self.resolve_turn(map, drones)
            turn_state: Dict[int, str] = {}
            for d in drones:
                if d.in_transit:
                    turn_state[d.did] = (
                        f"{d.cur_hub.name}-{d.destination.name}"
                    )
                else:
                    turn_state[d.did] = d.cur_hub.name
            state.append(turn_state)
            line = " ".join(moves)
            if line:
                print(line)
        return state

    def get_connection(
        self,
        map: Map,
        a: str,
        b: str,
    ) -> Connection:
        return (
            map.connections.get(f"{a}-{b}")
            or map.connections.get(f"{b}-{a}")
        )

    def resolve_turn(
        self,
        map: Map,
        drones: List[Drone],
    ) -> List[str]:

        moves: List[str] = []

        planned_arv: Dict[str, int] = {
            h: 0 for h in map.hubs.keys()
        }
        planned_dep: Dict[str, int] = {
            h: 0 for h in map.hubs.keys()
        }

        just_arrived = set()
        pending: List[Tuple[Drone, Hub]] = []

        for d in drones:
            if d.arrived or not d.in_transit:
                continue
            if self.future_arv.get(
                (d.destination.name, self.cur_turn), 0
            ) > 0:
                con = self.get_connection(
                    map,
                    d.destination.name,
                    d.cur_hub.name,
                )
                self.future_arv[
                    (d.destination.name, self.cur_turn)
                ] -= 1
                d.in_transit = False
                d.cur_hub = d.destination
                d.cur_hub.current_drones.append(d)
                d.destination = None
                d.path_index += 1
                con.in_transit.remove(d)
                moves.append(f"D{d.did}-{d.cur_hub.name}")
                just_arrived.add(d.did)
            if d.cur_hub.name == map.end.name:
                d.arrived = True

        for d in drones:
            if d.arrived or d.in_transit:
                continue
            if d.did in just_arrived:
                continue
            if self.cur_turn < d.start_turn:
                continue
            hub = d.path[d.path_index + 1]
            occupied = (
                len(map.hubs[hub].current_drones)
                + planned_arv[hub]
                - planned_dep[hub]
            )
            if occupied < map.hubs[hub].max_drones:
                if map.hubs[hub].zone_type == "restricted":
                    future_turn = self.cur_turn + 1
                    con = self.get_connection(map, d.cur_hub.name, hub)
                    if (self.future_arv.get((hub, future_turn), 0) < map.hubs[hub].max_drones
                        and len(con.in_transit) < con.max_link_capacity
                    ):
                        self.future_arv[(hub, future_turn)] = (
                            self.future_arv.get((hub, future_turn), 0) + 1
                        )
                        d.cur_hub.current_drones.remove(d)
                        d.in_transit = True
                        d.destination = map.hubs[hub]
                        con.in_transit.append(d)
                        moves.append(
                            f"D{d.did}-{d.cur_hub.name}-{hub}"
                        )
                else:
                    pending.append((d, map.hubs[hub]))
                    planned_arv[hub] += 1
                    planned_dep[d.cur_hub.name] += 1
                    moves.append(f"D{d.did}-{hub}")

        for d, dest in pending:
            d.cur_hub.current_drones.remove(d)
            d.cur_hub = dest
            d.cur_hub.current_drones.append(d)
            d.path_index += 1
            if d.cur_hub.name == map.end.name:
                d.arrived = True
        return moves

p = Parser("map.txt")
try:
    d = p.parse()
    e = Engine()
    s = Schedular()
    v = Visualizer(d)
    paths = d.find_paths(d.start, d.end)
    if not paths:
        print("Error: no path found between start and end")
        exit(1)
    Drones = s.create_drones(d, d.find_paths(d.start, d.end))
    state = e.simulate(d, Drones)
    v.run(state)
except ParserError as e:
    print(e)