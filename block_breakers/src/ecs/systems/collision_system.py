import pygame
from src.ecs.system import System
from src.ecs.components.position import Position
from src.ecs.components.velocity import Velocity
from src.ecs.components.renderable import Renderable
from src.ecs.components.ball import Ball
from src.ecs.components.paddle import Paddle
from src.ecs.components.brick import Brick

class CollisionSystem(System):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, entities, dt):
        ball_entities = [e for e in entities if e.get_component(Ball)]
        paddle_entities = [e for e in entities if e.get_component(Paddle)]
        brick_entities = [e for e in entities if e.get_component(Brick)]

        for ball_e in ball_entities:
            pos = ball_e.get_component(Position)
            vel = ball_e.get_component(Velocity)
            ball = ball_e.get_component(Ball)
            if not (pos and vel and ball):
                continue
            # Wall collisions
            if pos.x <= 0:
                pos.x = 0
                vel.vx *= -1
            if pos.x + ball.radius*2 >= self.screen_width:
                pos.x = self.screen_width - ball.radius*2
                vel.vx *= -1
            if pos.y <= 0:
                pos.y = 0
                vel.vy *= -1
            # Bottom -> reset (simple)
            if pos.y > self.screen_height:
                pos.x = self.screen_width/2 - ball.radius
                pos.y = self.screen_height/2
                vel.vx = 200
                vel.vy = -200

            ball_rect = pygame.Rect(int(pos.x), int(pos.y), ball.radius*2, ball.radius*2)

            # Paddle collision
            for paddle_e in paddle_entities:
                p_pos = paddle_e.get_component(Position)
                render = paddle_e.get_component(Renderable)
                if p_pos and render:
                    paddle_rect = render.rect(p_pos)
                    if ball_rect.colliderect(paddle_rect) and vel.vy > 0:
                        pos.y = paddle_rect.top - ball.radius*2
                        vel.vy *= -1
                        # tweak angle based on hit location
                        offset = (ball_rect.centerx - paddle_rect.centerx) / (paddle_rect.width/2)
                        vel.vx = offset * 300

            # Brick collisions
            for brick_e in brick_entities:
                b_pos = brick_e.get_component(Position)
                b_render = brick_e.get_component(Renderable)
                brick = brick_e.get_component(Brick)
                if b_pos and b_render and brick:
                    brick_rect = b_render.rect(b_pos)
                    if ball_rect.colliderect(brick_rect):
                        # simple reflection
                        # Determine side: choose axis with smallest overlap
                        overlap_left = ball_rect.right - brick_rect.left
                        overlap_right = brick_rect.right - ball_rect.left
                        overlap_top = ball_rect.bottom - brick_rect.top
                        overlap_bottom = brick_rect.bottom - ball_rect.top
                        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                        if min_overlap == overlap_left:
                            pos.x -= overlap_left
                            vel.vx *= -1
                        elif min_overlap == overlap_right:
                            pos.x += overlap_right
                            vel.vx *= -1
                        elif min_overlap == overlap_top:
                            pos.y -= overlap_top
                            vel.vy *= -1
                        else:
                            pos.y += overlap_bottom
                            vel.vy *= -1
                        brick.hit_points -= 1
