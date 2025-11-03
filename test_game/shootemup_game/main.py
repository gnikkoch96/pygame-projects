import pygame
import random
from typing import List, Dict, Optional, Tuple, Union
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shoot em\' Up Game')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True


