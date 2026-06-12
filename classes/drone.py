from dataclasses import dataclass
from typing import List, Optional
from classes.hub import Hub
from classes.map import Map

@dataclass
class Drone:
    did: int
    start_turn: int
    path: List[str]
    cur_hub: Hub
    path_index: int
    arrived: bool
    in_transit: bool
    direction: Optional[Hub]
