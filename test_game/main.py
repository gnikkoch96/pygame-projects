import pygame
from typing import List, Dict, Optional, Tuple, Union

pygame.init()

# screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
TIME_LIMIT: int = 30000
BACKGROUND_COLOR: str = '#ffffff'
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Collect the Money')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()
FPS: int = 60 # 60 fps target 

# game flags
running: bool = True

# ui objs
font: pygame.font.SysFont = pygame.font.SysFont(None, 48)

# bucket
BUCKET_HEIGHT: int = 50
BUCKET_WIDTH: int = 100
BUCKET_COLOR: str = "#735b5b"
bucket_y: int = SCREEN_HEIGHT - BUCKET_HEIGHT
bucket_x: int  = SCREEN_WIDTH // 2 - BUCKET_WIDTH //2
bucket: List[Union[int, str]] = [bucket_x, bucket_y, BUCKET_WIDTH, BUCKET_HEIGHT, BUCKET_COLOR]

def check_input():
    global running, bucket_x, bucket_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Note: pressing x sends a QUIT event
            running = False

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and bucket[0] > 0:
        bucket[0] -= 5
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and bucket[0] < SCREEN_WIDTH - BUCKET_WIDTH:
        bucket[0] += 5
    

def render():
    global screen
    screen.fill(pygame.Color(BACKGROUND_COLOR))

    # render bucket
    pygame.draw.rect(screen, pygame.Color(bucket[4]), bucket[:4])

    pygame.display.flip()

while running: 
    check_input()
    render()
    clock.tick(FPS)