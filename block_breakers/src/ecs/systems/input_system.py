import pygame
from src.ecs.system import System
from src.ecs.components.paddle import Paddle
from src.ecs.components.position import Position

class InputSystem(System):
    def __init__(self, screen_width):
        self.screen_width = screen_width

    def update(self, entities, dt):
        keys = pygame.key.get_pressed()
        for e in entities:
            paddle = e.get_component(Paddle)
            pos = e.get_component(Position)
            if paddle and pos:
                move = 0
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    move -= paddle.speed * dt
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    move += paddle.speed * dt
                pos.x += move
                # clamp
                if pos.x < 0:
                    pos.x = 0
                max_x = self.screen_width - 100
                if pos.x > max_x:
                    pos.x = max_x
