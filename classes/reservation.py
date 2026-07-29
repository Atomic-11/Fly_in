from dataclasses import dataclass, field
from typing import Dict, Tuple


@dataclass
class Reservation:
    hub_occupancy: Dict[Tuple[str, int], int] = field(default_factory=dict)
    link_occupancy: Dict[Tuple[str, int], int] = field(default_factory=dict)

    def hub_count(self, hub_name: str, turn: int) -> int:
        return self.hub_occupancy.get((hub_name, turn), 0)

    def link_count(self, link_key: str, turn: int) -> int:
        return self.link_occupancy.get((link_key, turn), 0)

    def reserve_hub(self, hub_name: str, turn: int) -> None:
        key = (hub_name, turn) 
        self.hub_occupancy[key] = self.hub_occupancy.get(key, 0) + 1

    def reserve_link(self, link_key: str, turn: int) -> None:
        key = (link_key, turn)
        self.link_occupancy[key] = self.link_occupancy.get(key, 0) + 1