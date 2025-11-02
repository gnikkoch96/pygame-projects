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
MONEY_LIST: List[List[Union[int, str]]] = []
MONEY_FALL_SPEED_MIN: int = 3
MONEY_FALL_SPEED_MAX: int = 6
MONEY_SPAWN_RATE_MIN: int = 30 # per 60 FPS
MONEY_SPAWN_RATE_MAX: int = 120

# rock
ROCK_SIZE: List[int] = [30, 30]
ROCK_COLOR: str = "#90614c"
ROCK_FALL_SPEED: int = 10
ROCK_SPAWN_RATE_MIN: int = 120
ROCK_SPAWN_RATE_MAX: int = 300
ROCK_LIST: List[List[Union[int, str]]] = []

# game logic
TIME_LIMIT: int = 30000
running: bool = True
frame_count = 0
score: int = 0
start_time: int = 0
remaining_time: int = TIME_LIMIT

# ui objs
font: pygame.font.SysFont = pygame.font.SysFont(None, 48)
button_font: pygame.font.SysFont = pygame.font.SysFont(None, 24)

# list of {'text': str, 'x': int, 'y': int, 'alpha': int, 'timer': int}
text_animations: List[Dict[str, Union[str, int]]] = [] 

def update():
    global frame_count, score, remaining_time, money_fall_speed, money_spawn_rate

    # update time
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    remaining_time = max(0, TIME_LIMIT - elapsed_time)

    # calculate progress (0 at start, 1 at end)
    progress = (TIME_LIMIT - remaining_time) / TIME_LIMIT if TIME_LIMIT > 0 else 1

    # interpolate fall speed and spawn rate (linear increase)
    current_money_fall_speed = int(MONEY_FALL_SPEED_MIN + progress * (MONEY_FALL_SPEED_MAX - MONEY_FALL_SPEED_MIN))

    current_money_spawn_rate = max(1, int(MONEY_SPAWN_RATE_MAX - progress * (MONEY_SPAWN_RATE_MAX - MONEY_SPAWN_RATE_MIN)))

    current_rock_spawn_rate = max(1, int(ROCK_SPAWN_RATE_MAX - progress * (ROCK_SPAWN_RATE_MAX - ROCK_SPAWN_RATE_MIN)))

    # spawn new money
    frame_count += 1
    if frame_count % current_money_spawn_rate == 0:
        rand_x = random.randint(0, SCREEN_WIDTH - MONEY_SIZE[0])
        MONEY_LIST.append([rand_x, 0, MONEY_SIZE[0], MONEY_SIZE[1], MONEY_COLOR])

    # spawn rock
    if frame_count % current_rock_spawn_rate == 0:
        rand_x = random.randint(0, SCREEN_WIDTH - MONEY_SIZE[0])
        ROCK_LIST.append([rand_x, 0, ROCK_SIZE[0], ROCK_SIZE[1], ROCK_COLOR])

    # update money position and check for collisions
    bucket_rect = pygame.Rect(bucket[0], bucket[1], bucket[2], bucket[3])
    
    for money in MONEY_LIST[:]: # slice to allow removal of items
        money[1] += current_money_fall_speed

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

    # hud
    money_label = font.render(f"Money: ${score}", True, pygame.Color("#000000"))
    screen.blit(money_label, (0, 0))

    timer_label = font.render(f"Time: {remaining_time // 1000}s", True, pygame.Color("#000000"))
    screen.blit(timer_label, (SCREEN_WIDTH - 160, 0))

    pygame.display.flip()

def show_game_over_dialog():
    global score, start_time, remaining_time, game_finished, last_generation_time, running
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # dialog box
    dialog_width, dialog_height = 400, 250
    dialog_x = (SCREEN_WIDTH - dialog_width) // 2
    dialog_y = (SCREEN_HEIGHT - dialog_height) // 2

    # main dialog box
    pygame.draw.rect(screen, pygame.Color("#ffffff"), (dialog_x, dialog_y, dialog_width, dialog_height))

    # border color
    pygame.draw.rect(screen, pygame.Color('#000000'), (dialog_x, dialog_y, dialog_width, dialog_height), 2)

    message = f"Your Final Score: {score}"
    text = font.render(message, True, pygame.Color("#000000"))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # buttons
    button_width, button_height = 100, 50

    # retry button
    retry_button_x = dialog_x + (dialog_width - button_width) // 2 - 75
    retry_button_y = dialog_y + dialog_height - button_height - 20
    pygame.draw.rect(screen, pygame.Color("#4CAF50"), (retry_button_x, retry_button_y, button_width, button_height))
    pygame.draw.rect(screen, pygame.Color("#000000"), (retry_button_x, retry_button_y, button_width, button_height), 1)

    # retry button text
    button_text = button_font.render("Restart", True, pygame.Color('#ffffff'))
    button_text_rect = button_text.get_rect(center=(retry_button_x + button_width // 2, retry_button_y + button_height // 2))
    screen.blit(button_text, button_text_rect)

    # exit button
    exit_button_x = dialog_x + (dialog_width - button_width) // 2 + 75
    exit_button_y = dialog_y + dialog_height - button_height - 20
    pygame.draw.rect(screen, pygame.Color("#AF594C"), (exit_button_x, exit_button_y, button_width, button_height))
    pygame.draw.rect(screen, pygame.Color("#000000"), (exit_button_x, exit_button_y, button_width, button_height), 1)

    # exit button text
    button_text = button_font.render("Exit", True, pygame.Color("#ffffff"))
    button_text_rect = button_text.get_rect(center=(exit_button_x + button_width // 2, exit_button_y + button_height // 2))
    screen.blit(button_text, button_text_rect)

    pygame.display.flip()

    waiting = True
    while waiting: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # clicked on retry button
                if mouse_x >= retry_button_x and mouse_x <= (retry_button_x + button_width) and mouse_y >= retry_button_y and mouse_y <= (retry_button_y + button_height):
                    score = 0
                    start_time = pygame.time.get_ticks()
                    remaining_time = TIME_LIMIT
                    game_finished = False
                    last_generation_time = 0
                    MONEY_LIST.clear()
                    ROCK_LIST.clear()
                    text_animations.clear()
                    waiting = False # close dialog
            
                # clicked on exit button
                elif mouse_x >= exit_button_x and mouse_x <= (exit_button_x + button_width) and mouse_y >= exit_button_y and mouse_y <= (exit_button_y + button_height):
                    waiting = False
                    running = False

while running: 
    if remaining_time > 0:
        update()
        check_input()
        render()
    else:
        show_game_over_dialog()

    clock.tick(FPS)


