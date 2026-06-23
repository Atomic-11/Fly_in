from classes.map import Map
from classes.drone import Drone
from classes.hub import Hub
from classes.connection import Connection
from typing import List, Dict, Tuple
from ui.visualizer import Visualizer
from configs.parser import Parser, ParserError
from simulation.schedular import Schedular


class Engine:
    
    current_turn: int = 0
    future_arv: Dict[Tuple[str, int], int] = {}

    def simulate(self, mp: Map, drones: List[Drone]) -> List[Dict[int, str]]:
        state: List[Dict[int, str]] = []
        for drone in drones:
            mp.start.current_drones.append(drone)
        state.append({d.did: d.cur_hub.name for d in drones})
        while not all(d.arrived for d in drones):
            self.current_turn += 1
            movements = self.resolve_turn(drones, mp)
            turn_state = {}
            for d in drones:
                if d.in_transit:
                    turn_state[d.did] = f"{d.cur_hub.name}-{d.destination.name}"
                else:
                    turn_state[d.did] = d.cur_hub.name
            state.append(turn_state)
            line = " ".join(movements)
            if line:
                print(line)
        return state
            
    def get_connection(self, mp: Map, a: str, b: str) -> Connection:
        return (mp.connections.get(f"{a}-{b}") or
                mp.connections.get(f"{b}-{a}"))
    
    def resolve_turn(self, drones: List[Drone], mp: Map) -> List[str]:
        moves: List[str] = []
        planned_arrivals: Dict[str, int] = {h: 0 for h in mp.hubs.keys()}
        planned_departures: Dict[str, int] = {h: 0 for h in mp.hubs.keys()}
        just_arrived = set()
        pending = []

        for d in drones:
            if d.arrived or not d.in_transit:
                continue
            if self.future_arv.get((d.destination.name, self.current_turn), 0) > 0:
                con = self.get_connection(mp, d.cur_hub.name, d.destination.name)
                self.future_arv[(d.destination.name, self.current_turn)] -= 1
                d.cur_hub = d.destination
                d.cur_hub.current_drones.append(d)
                d.path_index += 1
                d.in_transit = False
                d.destination = None
                con.in_transit.remove(d)
                just_arrived.add(d.did)
                moves.append(f"D{d.did}-{d.cur_hub.name}")
                if d.cur_hub.name == mp.end.name:
                    d.arrived = True

        for d in drones:
            if d.arrived or d.in_transit:
                continue
            if d.did in just_arrived:
                continue
            if self.current_turn < d.start_turn:
                continue
            hub = d.path[d.path_index + 1]
            occupied = (
                len(mp.hubs[hub].current_drones)
                + planned_arrivals[hub]
                - planned_departures[hub]
            )
            if occupied < mp.hubs[hub].max_drones:
                if mp.hubs[hub].zone_type == 'restricted':
                    future_turn = self.current_turn + 1
                    con = self.get_connection(mp, d.cur_hub.name, hub)
                    if (
                        self.future_arv.get((hub, future_turn), 0) < mp.hubs[hub].max_drones
                        and len(con.in_transit) < con.max_link_capacity
                    ):
                        con.in_transit.append(d)
                        self.future_arv[(hub, future_turn)] = (
                            self.future_arv.get((hub, future_turn), 0) + 1
                        )
                        d.cur_hub.current_drones.remove(d)
                        d.in_transit = True
                        d.destination = mp.hubs[hub]
                        moves.append(f"D{d.did}-{d.cur_hub.name}-{hub}")
                else:
                    pending.append((d, mp.hubs[hub]))
                    planned_arrivals[hub] += 1
                    planned_departures[d.cur_hub.name] += 1
                    moves.append(f"D{d.did}-{hub}")

        for drone, destination in pending:
            drone.cur_hub.current_drones.remove(drone)
            drone.path_index += 1
            drone.cur_hub = destination
            destination.current_drones.append(drone)
            if destination.name == mp.end.name:
                drone.arrived = True
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