from dataclasses import dataclass
from src.ecs.component import Component

@dataclass
class Velocity(Component):
    vx: float
    vy: float
