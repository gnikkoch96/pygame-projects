import pygame
from enum import Enum
from config import SCREEN_HEIGHT

class BulletOwner(Enum):
    PLAYER = "player"
    ENEMY = "enemy"

class Bullet:
    # direction (1 = up, 0 = down)
    def __init__(self, x: int, y: int, speed: int = 2, direction: int = 1, owner: BulletOwner = BulletOwner.PLAYER):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.owner = owner
        self.speed = speed
        self.color = pygame.Color("#ffffff")
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = direction
        self.is_alive = True

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, pygame.Color(self.color), self.rect)

    def update(self):
        if self.direction == 1:
            self.y -= self.speed
            self.rect.topleft = (self.x, self.y)

            if self.y <= 0:
                self.is_alive = False
        else: 
            self.y += self.speed
            self.rect.topleft = (self.x, self.y)

            if self.y >= SCREEN_HEIGHT:
                self.is_alive = False

