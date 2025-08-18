from dataclasses import dataclass
from src.ecs.component import Component

@dataclass
class Position(Component):
    x: float
    y: float
