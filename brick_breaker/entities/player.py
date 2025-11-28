import pygame
from typing import Sequence
from config import SCREEN_WIDTH, DEBUG_MODE

class Player:
    def __init__(self, x: int, y: int, width: int = 100, height: int = 10, speed: int = 5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = pygame.Color("#ffffff")
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_input(self, keys: Sequence[bool]):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x >= 0:
            self.x -= self.speed

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.width <= SCREEN_WIDTH:
            self.x += self.speed

        # let go of ball and/or speed up ball 
        if keys[pygame.K_SPACE]:
            pass

    
    def update(self):
        self.hitbox.topleft  = (self.x, self.y)

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.hitbox)

        if DEBUG_MODE: 
            pygame.draw.rect(screen, pygame.Color("#f90000"), self.hitbox, 1)        