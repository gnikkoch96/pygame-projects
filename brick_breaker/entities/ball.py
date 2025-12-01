import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, DEBUG_MODE

class Ball:
    def __init__(self, x: int, y: int, radius: int = 10, speed_x: int = 5, speed_y: int = 5):
        self.x = x
        self.y = y
        self.radius = radius 
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = pygame.Color("#ffffff")
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    # mainly used to test ball 
    def handle_input(self):
        self.x, self.y = pygame.mouse.get_pos()
        self.hitbox.center = (self.x, self.y)

    def update(self):
        if DEBUG_MODE: return

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

        if DEBUG_MODE: 
            pygame.draw.rect(screen, pygame.Color("#f90000"), self.hitbox, 1)   