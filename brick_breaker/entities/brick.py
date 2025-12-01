import pygame

class Brick:
    def __init__(self, x: int, y: int, color: str, width: int = 50, height: int = 20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hitbox = pygame.Rect(x, y, width, height) 

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, pygame.Color(self.color), self.hitbox))