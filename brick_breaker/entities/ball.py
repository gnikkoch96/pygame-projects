import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH

class Ball:
    def __init__(self, x: int, y: int, radius: int = 10, speed_x: int = 2, speed_y: int = 2):
        self.x = x
        self.y = y
        self.radius = radius 
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = pygame.Color("#ffffff")
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        # bounce x-axis
        if self.x + self.radius  >= SCREEN_WIDTH or self.x - self.radius < 0:
            self.speed_x *= -1 

        # bounce y-axis
        if self.y + self.radius >= SCREEN_HEIGHT or self.y - self.radius < 0:
            self.speed_y *= -1 
    
        self.x += self.speed_x
        self.y += self.speed_y

        self.hitbox.center = (self.x, self.y)

    def render(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # hitbox
        pygame.draw.rect(screen, pygame.Color("#f90000"), self.hitbox, 1)