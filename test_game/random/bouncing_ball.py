import pygame
from typing import List, Dict, Optional, Tuple, Union

pygame.init()

# screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball")

# fps limiter
clock = pygame.time.Clock()
FPS = 60

# we do this so that we can change when to run or not
running: bool = True

# ball properties 
ball_pos: List[float] = [0, 0] # x, y
ball_radius = 10
ball_color: str = '#4287f5'
move_speed: List[float] = [5.0, 0.0] # x vel, y vel
gravity: float = 0.5
bounce_damp: float = 0.9 

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update_physics():
    global ball_pos, move_speed

    # add gravity because 0,0 is at the top
    move_speed[1] += gravity

    # update poition
    ball_pos[0] += move_speed[0]
    ball_pos[1] += move_speed[1]
    
    # check for edges (and bounce if possible)

    # bounce on left/right edges
    if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= SCREEN_WIDTH:
        move_speed[0] = -move_speed[0] * bounce_damp
        ball_pos[0] = max(ball_radius, min(SCREEN_WIDTH - ball_radius, ball_pos[0]))


    # bounce on top/bottom edges
    if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= SCREEN_HEIGHT:
        move_speed[1] = -move_speed[1] * bounce_damp
        ball_pos[1] = max(ball_radius, min(SCREEN_HEIGHT - ball_radius, ball_pos[1]))

    # add dampening to the x speed
    if (ball_pos[1] + ball_radius) + gravity >= SCREEN_HEIGHT:
        move_speed[0] *= 0.98


def render():
    global screen
    screen.fill(pygame.Color("#ffffff"))
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.display.flip()

while running:
    check_input()
    update_physics()
    render()

    clock.tick(FPS)
