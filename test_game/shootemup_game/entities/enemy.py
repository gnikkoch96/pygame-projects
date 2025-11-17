import pygame
from typing import List, Union
from entities.bullet import BulletOwner, BulletDirection
from entities.pools.bullet_pool import BulletPool
from config import SCREEN_HEIGHT
from entities.player import Player

class Enemy:
    # class constants
    RED_COLOR = "#db3e3e"
    GREEN_COLOR = "#3edb6d"

    def __init__(self, x: int, y: int, hp: int, bullet_pool: BulletPool, speed: int = 2, shot_cooldown: int = 1000):
        self.x = x
        self.y = y
        self.hp = hp
        self.speed = speed
        self.width = 50
        self.height = 50
        self.current_target_index = 0 
        self.last_shot_time = 0
        self.shot_cooldown = shot_cooldown
        self.is_alive: bool = True
        self.bullet_pool = bullet_pool

        # color changes based on hp value
        if hp > 1:
            self.color = Enemy.GREEN_COLOR
        else:
            self.color = Enemy.RED_COLOR

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_cooldown:
            self.bullet_pool.get_bullet(self.x, self.y, 2, BulletDirection.DOWN, BulletOwner.ENEMY)
            self.last_shot_time = current_time
    
    def update(self, player: Player):
        # fly to the center of the screen in the beginning 
        if self.y <= SCREEN_HEIGHT // 3:
            self.y += self.speed
        else:
            # update center to fly towards player
            if self.x < player.x:
                self.x += self.speed
            elif self.x > player.x:
                self.x -= self.speed
            
            self.shoot()

    def render(self, screen: pygame.Surface):
        # left wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x, self.y),
                                (self.x - 15, self.y - self.height // 2),
                                (self.x, self.y - self.height // 2)
                            ],
                            width=2)
        # right wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x + self.width, self.y),
                                (self.x + self.width + 15, self.y - self.height // 2),
                                (self.x + self.width, self.y - self.height // 2)
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

        
        