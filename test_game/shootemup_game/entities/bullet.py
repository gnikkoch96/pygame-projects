import pygame

class Bullet:
    def __init__(self, x: int, y: int, speed: int = 2):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.speed = speed
        self.color = pygame.Color("#ffffff")
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_alive = True

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, pygame.Color(self.color), self.rect)

    def update(self):
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)

        if self.y <= 0:
            self.is_alive = False

