import pygame
from config import SCREEN_WIDTH
from entities.bullet import Bullet
from typing import List

class Player: 
    def __init__(self, x: int, y: int, speed: int = 5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.color = pygame.Color("#ffffff")
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullets: List[Bullet] = []

    def handle_input(self, keys):
        if keys[pygame.K_LEFT] and self.x - 27 >= 0:
            self.x -= self.speed

        if keys[pygame.K_RIGHT] and self.x + self.width + 2 <= SCREEN_WIDTH:
            self.x += self.speed

        if keys[pygame.K_SPACE]:
            self.bullets.append(Bullet(self.x + self.width // 2 - 2, self.y - 25, 2, 1))

        

    def update(self):
        for bullet in self.bullets:
            bullet.update()

        # print(f"Bullets before cleanup: {len(self.bullets)}")  # Debug: Count before

        # clean up dead bullets
        alive_bullets_left = []
        for bullet in self.bullets:
            if bullet.is_alive:
                alive_bullets_left.append(bullet)

        self.bullets = alive_bullets_left

        # print(f"Bullets after cleanup: {len(self.bullets)}")  # Debug: Count after

    def render(self, screen: pygame.Surface):
        # bullets
        for bullet in self.bullets:
            bullet.render(screen)


        # left wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x, self.y),
                                (self.x - 25, self.y + self.height),
                                (self.x, self.y + self.height)
                            ],
                            width=2)
        # right wing
        pygame.draw.polygon(screen, 
                            self.color,
                            [
                                (self.x + self.width, self.y),
                                (self.x + self.width + 25, self.y + self.height),
                                (self.x + self.width, self.y + self.height)
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



