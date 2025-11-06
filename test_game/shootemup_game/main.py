import pygame
import random
from typing import List, Dict, Optional, Tuple, Union
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS
from entities.player import Player
from entities.enemy import Enemy
from entities.meteor import Meteor

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shoot em\' Up Game')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True

# game objs
player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 100)
enemy = Enemy(100, 100, 1, [(0, 0), (SCREEN_HEIGHT + 100)])
meteor = Meteor(100, 100)

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)

def update():
    player.update()
    meteor.update()

def render():
    screen.fill(BACKGROUND_COLOR)
    player.render(screen)
    # enemy.render(screen)
    meteor.render(screen)

    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)
