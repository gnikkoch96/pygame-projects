import pygame
from typing import List, Union
from entities.bullet import Bullet

class Enemy:
    def __init__(self, x: int, y: int, color: str, path: List[Union[int, int]], speed: int = 2, shot_cooldown: int = 1000):
        self.x = x
        self.y = y
        self.color = color
        self.path = path
        self.speed = speed
        self.bullets: List[Bullet] = []
        self.current_target_index = 0 
        self.last_shot_time
        self.shot_cooldown = shot_cooldown

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pass

        
        