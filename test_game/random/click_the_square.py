import pygame
from typing import List, Dict, Optional, Tuple, Union
import random

pygame.init()

# screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
TIME_LIMIT = 30000 # milliseconds (30 seconds)
BACKGROUND_COLOR: str = "#ffffff"
screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Click the Square!")

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()
FPS: int = 60

# we do this so that we can change when to run or not
running: bool = True
game_finished: bool = False
font: pygame.font.SysFont = pygame.font.SysFont(None, 48)
button_font: pygame.font.SysFont = pygame.font.SysFont(None, 24)
score: int = 0
start_time: int = 0
remaining_time: int = 0

# rectangle properties
good_color: str = "#359c50" # can click
bad_color: str = "#872222" # lose points for clicking

square_generation_delay: int = 1500 # milliseconds 
last_generation_time: int = 0 # tracks when the last square was generated
current_square: Optional[Tuple[int, int, int, int, str]] = None


def check_input():
    global running, current_square, score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_square:
                x, y, w, h, color = current_square
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                    if color == good_color:
                        score += 1
                    else:
                        score -= 1
                    # regenerate a new square
                    current_square = None

def update():
    global current_square, last_generation_time, start_time, running, score, remaining_time, game_finished
    
    if game_finished:
        # display dialog
        show_game_over_dialog()
        # running = False 
        return

    current_time = pygame.time.get_ticks()
    
    # Square generation logic
    if current_square is None or (current_time - last_generation_time) >= square_generation_delay:
        square_size: int = random.randint(50, 250)
        random_x: int = random.randint(0, SCREEN_WIDTH - square_size)
        random_y: int = random.randint(0, SCREEN_HEIGHT - square_size)
        random_num: int = random.randint(1, 10)
        square_color: str = good_color
        if random_num % 4 == 0: square_color = bad_color
        current_square = (random_x, random_y, square_size, square_size, square_color)
        last_generation_time = current_time
    
    # Timer logic (if added)
    elapsed_time = current_time - start_time
    remaining_time = max(0, TIME_LIMIT - elapsed_time)
    if remaining_time <= 0:
        game_finished = True

def show_game_over_dialog():
    global score, start_time, remaining_time, game_finished, current_square, last_generation_time, running
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
                    current_square = None
                    last_generation_time = 0
                    waiting = False # close dialog
            
                # clicked on exit button
                elif mouse_x >= exit_button_x and mouse_x <= (exit_button_x + button_width) and mouse_y >= exit_button_y and mouse_y <= (exit_button_y + button_height):
                    waiting = False
                    running = False

                    


def render():
    global screen, current_square, score, remaining_time
    
    screen.fill(pygame.Color(BACKGROUND_COLOR))
    
    if current_square:
        x, y, w, h, color = current_square
        pygame.draw.rect(screen, pygame.Color(color), (x, y, w, h))
    
    # render score text
    text = font.render(f"Score: {score}", True, pygame.Color("#000000"))
    screen.blit(text, (0, 0))
    
    # Render timer if added
    timer_text = font.render(f"Time: {remaining_time // 1000}s", True, pygame.Color("#000000"))
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 0))
    
    pygame.display.flip()


while running:
    update()  # Call logic first
    check_input()
    render()  # Then render
    clock.tick(FPS)
