from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from classes.hub import Hub


@dataclass
class Connection:
    hub_a: Hub
    hub_b: Hub
    max_link_capacity: int
    in_transit: List = field(default_factory=list)
