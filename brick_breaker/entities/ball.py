import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH

class Ball:
    def __init__(self, x: int, y: int, size: int = 10, speed_x: int = 2, speed_y: int = 2):
        self.x = x
        self.y = y
        self.size = size # diameter
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = pygame.Color("#ffffff")

    def update(self):
        # bounce x-axis
        if self.x + self.size  >= SCREEN_WIDTH or self.x - self.size < 0:
            self.speed_x *= -1 

        # bounce y-axis
        if self.y + self.size >= SCREEN_HEIGHT or self.y - self.size < 0:
            self.speed_y *= -1 
    
        self.x += self.speed_x
        self.y += self.speed_y

    def render(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)