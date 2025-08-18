from dataclasses import dataclass
from src.ecs.component import Component

@dataclass
class Ball(Component):
    radius: int
    speed: float
