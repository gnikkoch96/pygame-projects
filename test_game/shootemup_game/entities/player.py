import pygame

class Player: 
    def __init__(self, x: int, y: int, speed: int = 5):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 50
        self.height = 50
        self.color = pygame.Color("#ffffff")
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_input(self, keys):
        print(keys)
    
    def update(self):
        pass

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)