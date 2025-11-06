import pygame

class Meteor:
    def __init__(self, x: int, y: int = 0, size: int = 25, speed: int = 2):
        self.x = x
        self.y = y
        self.width = size
        self.height = size
        self.color: str = "#6d5124"
        self.speed = speed
        self.angle = 0
        self.rotation_speed: int = 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, pygame.Color(self.color), (0, 0, self.width, self.height))

    def update(self):
        self.y += self.speed
        self.angle += self.rotation_speed
        self.rect.center = (self.x + self.width // 2, self.y + self.height // 2)


    def render(self, screen: pygame.Surface):
        rotated_surface = pygame.transform.rotate(self.surface, self.angle)
        rotated_rect = rotated_surface.get_rect(center=self.rect.center)
        screen.blit(rotated_surface, rotated_rect)