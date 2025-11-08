import pygame
from config import SCREEN_WIDTH
from entities.bullet import Bullet
from entities.pools.bullet_pool import BulletPool
from typing import List

class Player: 
    def __init__(self, x: int, y: int, bullet_pool: BulletPool, speed: int = 5):
        self.x = x
        self.y = y
        self.bullet_pool = bullet_pool
        self.speed = speed
        self.width = 50
        self.height = 50
        self.color = pygame.Color("#ffffff")
        self.last_shot_time = 0
        self.shot_cooldown = 200

    def handle_input(self, keys):
        current_time = pygame.time.get_ticks()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x - 27 >= 0:
            self.x -= self.speed

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.width + 27 <= SCREEN_WIDTH:
            self.x += self.speed

        if keys[pygame.K_SPACE] and current_time - self.last_shot_time > self.shot_cooldown:
            self.bullet_pool.get_bullet(self.x + self.width // 2 - 2, self.y - 25, 15, 1)
            self.last_shot_time = current_time

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pygame.draw.polygon(screen, 
            self.color,
            [
                (self.x, self.y),
                (self.x + self.width, self.y),
                (self.x + self.width // 2, self.y - 25)
            ],
            width=2)



