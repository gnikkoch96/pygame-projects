import pygame
import random
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

# money
MONEY_SIZE: List[int] = [50, 50]
MONEY_COLOR: str = "#21CE3B"
FALL_SPEED: int = 3
money_list: List[List[Union[int, str]]] = []
SPAWN_RATE: int = 120
frame_count = 0

def update():
    global frame_count

    # spawn new money
    frame_count += 1
    if frame_count % SPAWN_RATE == 0:
        rand_x = random.randint(0, SCREEN_WIDTH - MONEY_SIZE[0])
        money_list.append([rand_x, 0, MONEY_SIZE[0], MONEY_SIZE[1], MONEY_COLOR])

    # update money position and check for collisions
    bucket_rect = pygame.Rect(bucket[0], bucket[1], bucket[2], bucket[3])
    for money in money_list[:]: # slice to allow removal of items
        money[1] += FALL_SPEED

        money_rect = pygame.Rect(money[0], money[1], money[2], money[3])
        if bucket_rect.colliderect(money_rect):
            money_list.remove(money)
        elif money[1] > SCREEN_HEIGHT:
            money_list.remove(money)

    

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

    # render money
    for money in money_list:
        pygame.draw.rect(screen, pygame.Color(money[4]), money[:4])

    # render bucket
    pygame.draw.rect(screen, pygame.Color(bucket[4]), bucket[:4])

    pygame.display.flip()

while running: 
    update()
    check_input()
    render()
    clock.tick(FPS)