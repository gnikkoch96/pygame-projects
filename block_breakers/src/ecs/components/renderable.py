from dataclasses import dataclass
from src.ecs.component import Component
import pygame

@dataclass
class Renderable(Component):
    width: int
    height: int
    color: tuple

    def rect(self, position):
        return pygame.Rect(int(position.x), int(position.y), self.width, self.height)
