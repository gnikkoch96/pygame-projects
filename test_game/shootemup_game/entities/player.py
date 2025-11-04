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