import pygame
import random
from typing import List, Dict, Optional, Tuple, Union

pygame.init()

# screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
BACKGROUND_COLOR: str = '#ffffff'
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Collect the Money')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()
FPS: int = 60 # 60 fps target 

# bucket
BUCKET_HEIGHT: int = 50
BUCKET_WIDTH: int = 100
BUCKET_COLOR: str = "#735b5b"
bucket_y: int = SCREEN_HEIGHT - BUCKET_HEIGHT
bucket_x: int  = SCREEN_WIDTH // 2 - BUCKET_WIDTH //2
bucket: List[Union[int, str]] = [bucket_x, bucket_y, BUCKET_WIDTH, BUCKET_HEIGHT, BUCKET_COLOR]

# money
MONEY_SIZE: List[int] = [50, 15]
MONEY_COLOR: str = "#21CE3B"
MONEY_FALL_SPEED: int = 3
MONEY_LIST: List[List[Union[int, str]]] = []
MONEY_SPAWN_RATE: int = 120

# rock
ROCK_SIZE: List[int] = [30, 30]
ROCK_COLOR: str = "#90614c"
ROCK_FALL_SPEED: int = 10
ROCK_SPAWN_RATE: int = 300
ROCK_LIST: List[List[Union[int, str]]] = []

# game logic
TIME_LIMIT: int = 30000
running: bool = True
game_running: bool = True
frame_count = 0
score: int = 0
start_time: int = 0
remaining_time: int = 0

# ui objs
font: pygame.font.SysFont = pygame.font.SysFont(None, 48)

# list of {'text': str, 'x': int, 'y': int, 'alpha': int, 'timer': int}
text_animations: List[Dict[str, Union[str, int]]] = [] 

def update():
    global frame_count, score, game_running

    # spawn new money
    frame_count += 1
    if frame_count % MONEY_SPAWN_RATE == 0:
        rand_x = random.randint(0, SCREEN_WIDTH - MONEY_SIZE[0])
        MONEY_LIST.append([rand_x, 0, MONEY_SIZE[0], MONEY_SIZE[1], MONEY_COLOR])

    # spawn rock
    if frame_count % ROCK_SPAWN_RATE == 0:
        rand_x = random.randint(0, SCREEN_WIDTH - MONEY_SIZE[0])
        ROCK_LIST.append([rand_x, 0, ROCK_SIZE[0], ROCK_SIZE[1], ROCK_COLOR])

    # update money position and check for collisions
    bucket_rect = pygame.Rect(bucket[0], bucket[1], bucket[2], bucket[3])
    
    for money in MONEY_LIST[:]: # slice to allow removal of items
        money[1] += MONEY_FALL_SPEED

        money_rect = pygame.Rect(money[0], money[1], money[2], money[3])
        if bucket_rect.colliderect(money_rect):
            # update score
            earned = random.randint(10, 50)
            score += earned

            # add animation earned
            text_animations.append({
                'text': f"+{earned}",
                'x': money[0],
                'y': money[1],
                'alpha': 255,
                'text_color': MONEY_COLOR,
                'timer': 180 # 3 seconds at 60FPS
            })

            MONEY_LIST.remove(money)
        elif money[1] > SCREEN_HEIGHT:
            MONEY_LIST.remove(money)

    # update rock position and check for collisions
    for rock in ROCK_LIST[:]:
        rock[1] += ROCK_FALL_SPEED

        rock_rect = pygame.Rect(rock[0], rock[1], rock[2], rock[3])
        if bucket_rect.colliderect(rock_rect) and score > 0:
            # play lost animation
            text_animations.append({
                'text': f"-{score}",
                'x': font.size('Money:')[0],
                'y': 30,
                'alpha': 255,
                'text_color': ROCK_COLOR,
                'timer': 180
            })  
        
            # reset score
            score = 0

            ROCK_LIST.remove(rock)
        elif rock[1] > SCREEN_HEIGHT:
            ROCK_LIST.remove(rock)

    # update animations
    for anim in text_animations[:]:
        anim['timer'] -= 1
        anim['alpha'] = max(0, int(255 * (anim['timer'] / 180)))
        anim['y'] -= 1 

        if anim['timer'] <= 0:
            text_animations.remove(anim)

    # update time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    remaining_time = max(0, TIME_LIMIT - elapsed_time)

    if remaining_time <= 0:
        game_running = False

    

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
    for money in MONEY_LIST:
        pygame.draw.rect(screen, pygame.Color(money[4]), money[:4])

    # render rocks
    for rock in ROCK_LIST:
        pygame.draw.rect(screen, pygame.Color(rock[4]), rock[:4])

    # render bucket
    pygame.draw.rect(screen, pygame.Color(bucket[4]), bucket[:4])

    # render animations
    for anim in text_animations:
        text_surf = font.render(anim['text'], True, pygame.Color(anim['text_color']))
        text_surf.set_alpha(anim['alpha'])
        screen.blit(text_surf, (anim['x'], anim['y']))

    text = font.render(f"Money: ${score}", True, pygame.Color("#000000"))
    screen.blit(text, (0, 0))

    pygame.display.flip()

while running: 
    update()
    check_input()
    render()
    clock.tick(FPS)