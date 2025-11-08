import pygame
from typing import List
from entities.meteor import Meteor

class MeteorPool:
    def __init__(self, max_meteors: int = 10):
        self.pool = [Meteor(0, 0, 0, 0) for _ in range(max_meteors)]
        self.active_meteors: List[Meteor] = []
    
    def get_meteor(self, x: int, y: int, size: int = 25, speed: int = 2) -> Meteor:
        # we are updating the stats of an unused meteor in the pool
        if self.pool:
            meteor = self.pool.pop()
            meteor.x = x
            meteor.y = y
            meteor.width = size
            meteor.height = size
            meteor.speed = speed
            meteor.is_alive = True
            meteor.rect.x = x
            meteor.rect.y = y
            meteor.rect.width = size
            meteor.rect.height = size

            # we need to update the surface of the meteor as well to the new size (initiailly at size 0)
            meteor.surface = pygame.Surface((meteor.width, meteor.height), pygame.SRCALPHA)
            pygame.draw.rect(meteor.surface, pygame.Color(meteor.color), (0, 0, meteor.width, meteor.height))
        else:
            meteor = Meteor(x, y, size, speed)

        self.active_meteors.append(meteor)
        return meteor
    
    def update_all(self):
        for meteor in self.active_meteors:
            meteor.update()

            if not meteor.is_alive:
                self.pool.append(meteor)
                self.active_meteors.remove(meteor)
    
    def render_all(self, screen: pygame.Surface):
        for meteor in self.active_meteors:
            meteor.render(screen)
        
