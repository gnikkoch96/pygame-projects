import pygame
from entities.ball import Ball
from typing import Sequence
from config import SCREEN_WIDTH, DEBUG_MODE

class Player:
    def __init__(self, x: int, y: int, ball: Ball, width: int = 100, height: int = 10, speed: int = 5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = pygame.Color("#ffffff")
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ball = ball
        self.ball_attached = True

    def handle_input(self, keys: Sequence[bool]):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x >= 0:
            self.x -= self.speed

        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.width <= SCREEN_WIDTH:
            self.x += self.speed

        # let go of ball and/or speed up ball 
        if keys[pygame.K_SPACE]:
            # release the ball
            if self.ball_attached:
                self.ball_attached = False
                
            # else speed up the ball (while space is being hold)

    
    def update(self):
        self.hitbox.topleft  = (self.x, self.y)

        if self.ball and self.ball_attached:
            self.ball.x = self.x + self.width // 2
            self.ball.y = self.y - self.ball.radius

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.hitbox)

        if DEBUG_MODE: 
            pygame.draw.rect(screen, pygame.Color("#f90000"), self.hitbox, 1)        