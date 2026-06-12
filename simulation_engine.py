from classes.map import Map
from classes.drone import Drone
from classes.hub import Hub
from classes.connection import Connection
from typing import List, Optional, Dict
from ui.visualizer import Visualizer


class Engine:

    
    def simulate(self, drones: List[Drone], mp: Map):
        
        while not all(d.arrived for d in drones):
            planned_moves = self.resolve_turn(drones, mp)
            
                
                
    def resolve_turn(self, drones: List[Drone], mp: Map):
        planned_arrivals: Dict[str, int] = {h.name: 0 for h in mp.hubs}
        planned_departures: Dict[str, int] = {h.name: 0 for h in mp.hubs}
        for i, d in enumerate(drones):
            hub = d.path[d.path_index + 1]
            if d.arrived:
                continue
            if d.in_transit:
                planned_arrivals[hub] += 1
                mp.connections[d.cur_hub.name, hub].in_transit.remove(d)
                d.in_transit = False
                d.direction = None
            available_space = planned_arrivals[hub] + len(mp.hubs[hub].current_drones - planned_departures[hub]
            if available_space < mp.hubs[hub].max_drones:
                if mp.hubs[hub].zone_type == 'restricted':
                    if mp.connections[d.cur_hub.name, hub].max_link_capacity > planned_arrivals[hub]:
                        mp.connections[d.cur_hub.name, hub].in_transit.append(d)
                        d.in_transit = True
                        d.direction = mp.hubs[hub]
                    else:
                        continue
                d.path_index += 1
                planned_arrivals[hub] += 1
                planned_departures[d.cur_hub.name] += 1
                d.cur_hub = mp.hubs[hub]
            else:
                continue
            if hub == mp.end:
                d.arrived = True
                
        return planned_arrivals