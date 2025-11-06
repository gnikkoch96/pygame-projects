import pygame
from typing import List, Union
from entities.bullet import Bullet

class Enemy:
    # class constants
    RED_COLOR = "#db3e3e"
    GREEN_COLOR = "#3edb6d"

    def __init__(self, x: int, y: int, hp: int, path: List[Union[int, int]], speed: int = 2, shot_cooldown: int = 1000):
        self.x = x
        self.y = y
        self.hp = hp
        self.path = path
        self.speed = speed
        self.width = 50
        self.height = 50
        self.bullets: List[Bullet] = []
        self.current_target_index = 0 
        self.last_shot_time = 0
        self.shot_cooldown = shot_cooldown

        # color changes based on hp value
        if hp > 1:
            self.color = Enemy.GREEN_COLOR
        else:
            self.color = Enemy.RED_COLOR

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        # bullets
        for bullet in self.bullets:
            bullet.render(screen)


        # left wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x, self.y),
                                (self.x - 25, self.y - self.height),
                                (self.x, self.y - self.height)
                            ],
                            width=2)
        # right wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x + self.width, self.y),
                                (self.x + self.width + 25, self.y - self.height),
                                (self.x + self.width, self.y - self.height)
                            ],
                            width=2)

        # top body
        pygame.draw.polygon(screen, 
            self.color,
            [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width // 2, self.y - 25)
            ],
            width=2)
        
        # bottom body
        pygame.draw.polygon(screen, 
                    self.color,
                    [
                        (self.x, self.y),
                        (self.x + self.width, self.y),
                        (self.x + self.width // 2, self.y + 25)
                    ],
                    width=2)

        
        