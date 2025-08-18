from dataclasses import dataclass
from src.ecs.component import Component

@dataclass
class Paddle(Component):
    speed: float = 400.0
