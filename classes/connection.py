from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from classes.hub import Hub


@dataclass
class Connection:
    hub_a: "Hub"
    hub_b: "Hub"
    max_link_capacity: int = 1

    in_transit: list = field(default_factory=list)