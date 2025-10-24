import pygame
from typing import List, Dict, Optional, Tuple, Union

pygame.init()

# screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Square")

# we do this so that we can change when to run or not
running: bool = True

# square properties
square_vector: List[int]  = [100, 100] # [x, y]
square_size: int = 50
square_color: str = '#4287f5'
move_speed: int = 5

def check_input():
    global square_vector, running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                square_vector[0] -= move_speed
            if event.key == pygame.K_RIGHT:
                square_vector[0] += move_speed
            if event.key == pygame.K_DOWN:
                square_vector[1] += move_speed
            if event.key == pygame.K_UP:
                square_vector[1] -= move_speed

def render():
    global screen
    screen.fill(pygame.Color("#ffffff"))
    pygame.draw.rect(screen, square_color, (square_vector[0], square_vector[1], square_size, square_size))
    pygame.display.flip()

while running:
    check_input()
    render()