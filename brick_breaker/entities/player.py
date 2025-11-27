import pygame

class Player:
    def __init__(self, x: int, y: int, width: int = 100, height: int = 10, speed: int = 3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = pygame.Color("#ffffff")
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.hitbox)