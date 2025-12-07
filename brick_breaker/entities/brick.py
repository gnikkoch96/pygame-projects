import pygame

class Brick:
    def __init__(self, x: int, y: int, color: str, hp: int = 1, width: int = 50, height: int = 20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hitbox = pygame.Rect(x, y, width, height) 
        self.hp = hp

    def update(self):
        if self.hp == 1:
            self.color = "#ffffff"
        elif self.hp == 2:
            self.color = "#ba9d4f"
        elif self.hp == 3: 
            self.color = "#e15353"

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, pygame.Color(self.color), self.hitbox)