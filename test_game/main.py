import pygame
from typing import List, Dict, Optional, Tuple, Union
import random

pygame.init()

# screen settings
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
TIME_LIMIT = 5000 # milliseconds (30 seconds)
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
        print("Time's up! Final Score:", score)
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
    check_input()
    update()  # Call logic first
    render()  # Then render
    clock.tick(FPS)
