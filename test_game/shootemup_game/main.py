import pygame
import random
from typing import List, Dict, Optional, Tuple, Union
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS
from entities.player import Player

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shoot em\' Up Game')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True

# game objs
player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 100)

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update():
    player.update()

def render():
    screen.fill(BACKGROUND_COLOR)
    player.render(screen)
    
    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)
