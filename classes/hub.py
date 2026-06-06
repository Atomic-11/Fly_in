from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from classes.connection import Connection

if TYPE_CHECKING:
    from classes.connection import Connection


@dataclass
class Hub:
    name: str
    x: int
    y: int
    zone_type: str
    color: str
    max_drones: int
    is_start: bool
    is_end: bool
    connections: list["Connection"] = field(default_factory=list)
    current_drones: list = field(default_factory=list)