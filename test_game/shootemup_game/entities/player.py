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
        self.width = 25
        self.height = 25
        self.color = pygame.Color("#ffffff")
        self.last_shot_time = 0
        self.shot_cooldown = 200
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = pygame.Rect(self.rect.x - 15, self.rect.y + 10, self.rect.width, self.rect.height)

    def handle_input(self, keys):
        current_time = pygame.time.get_ticks()

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x - 27 >= 0:
            self.x -= self.speed

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.width + 27 <= SCREEN_WIDTH:
            self.x += self.speed

        if keys[pygame.K_SPACE] and current_time - self.last_shot_time > self.shot_cooldown:
            self.bullet_pool.get_bullet(self.x + self.width // 2 - 5, self.y, 15, 1)
            self.last_shot_time = current_time

    def update(self):
        # Update rect to match expanded bounding box
        self.rect.topleft = (self.x, self.y)
        self.hitbox.topleft = (self.rect.x - 15, self.rect.y + 10)

    def render(self, screen: pygame.Surface):
        # canon
        pygame.draw.rect(screen, pygame.Color(self.color), (self.x + self.width // 2 - 4, self.y - 10, 10, 10))
        
        # body
        pygame.draw.rect(screen, pygame.Color(self.color), self.rect)
        
        # left wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x, self.y),
                                (self.x - 15, self.y + self.height // 2 + 25),
                                (self.x, self.y + self.height)
                            ],
                            width=2)
        # right wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x + self.width, self.y),
                                (self.x + self.width + 15, self.y + self.height // 2+ 25),
                                (self.x + self.width, self.y + self.height)
                            ],
                            width=2)

        # pygame.draw.polygon(screen, 
        #     self.color,
        #     [
        #         (self.x, self.y),
        #         (self.x + self.width, self.y),
        #         (self.x + self.width // 2, self.y - 25)
        #     ],
        #     width=2)



