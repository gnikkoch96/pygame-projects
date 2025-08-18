import pygame
from src.ecs.system import System
from src.ecs.components.position import Position
from src.ecs.components.renderable import Renderable
from src.ecs.components.ball import Ball

class RenderSystem(System):
    def __init__(self, screen):
        self.screen = screen

    def update(self, entities, dt):
        self.screen.fill((20, 20, 30))
        for e in entities:
            pos = e.get_component(Position)
            render = e.get_component(Renderable)
            ball = e.get_component(Ball)
            if pos and render:
                pygame.draw.rect(self.screen, render.color, render.rect(pos))
            elif pos and ball:
                pygame.draw.circle(self.screen, (200,200,255), (int(pos.x+ball.radius), int(pos.y+ball.radius)), ball.radius)
