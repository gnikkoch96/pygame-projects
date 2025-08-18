from dataclasses import dataclass
from src.ecs.component import Component

@dataclass
class Brick(Component):
    hit_points: int = 1
    score: int = 100
