import pygame
import random
from typing import List, Dict, Union
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS, TIME_LIMIT
from entities.player import Player
from entities.enemy import Enemy
from entities.meteor import Meteor
from entities.pools.bullet_pool import BulletPool
from entities.pools.meteor_pool import MeteorPool
from entities.pools.enemy_pool import EnemyPool

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shoot em\' Up Game')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True
score: int = 0
start_time: int = 0
remainint_time: int = TIME_LIMIT

# ui objs
hud_font: pygame.font.SysFont = pygame.font.SysFont(None, 48)
button_font: pygame.font.SysFont = pygame.font.SysFont(None, 24)

# list of {'text': str, 'x': int, 'y': int, 'alpha': int, 'timer': int}
text_animations: List[Dict[str, Union[str, int]]] = [] 

# game objs
bullet_pool: BulletPool = BulletPool()
meteor_pool: MeteorPool = MeteorPool()
enemy_pool: EnemyPool = EnemyPool(bullet_pool)
player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 75, bullet_pool)

def update_time():
    global remaining_time, meteor_pool

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - start_time
    remaining_time = max(0, TIME_LIMIT - elapsed_time)

    # time based progression on the meteor_pool
    progress = (TIME_LIMIT - remaining_time) / TIME_LIMIT if TIME_LIMIT > 0 else 1

    # update meteor_pool based on time progression (spawn rate, size range, speed range)
    meteor_pool.spawn_rate = max(1, (1000 - progress * 500)) # decrease spawn rate by 500 by the end

    # in the end the range will be increased by 5 for min/max
    meteor_pool.meteor_min_speed = int(max(1,  1 + progress * 5))
    meteor_pool.meteor_max_speed = int(max(1,  3 + progress * 5))

    # in the end the range will be increased by 15 for min/max
    meteor_pool.meteor_min_size = int(max(1,  25 + progress * 25))
    meteor_pool.meteor_max_size = int(max(1,  50 + progress * 25))

    if remaining_time == 0:
        show_game_over_dialog()

def check_collisions():
    global score

    # player/meteor collisions
    for meteor in meteor_pool.active_meteors[:]:
        # player collides with meteor
        if player.hitbox.colliderect(meteor.rect):
            meteor.is_alive = False
            show_game_over_dialog()

    # bullet/meteor collision
    for bullet in bullet_pool.active_bullets[:]:
        for meteor in meteor_pool.active_meteors[:]:
            if bullet.rect.colliderect(meteor.rect):
                bullet.is_alive = False
                meteor.is_alive = False

                # update score
                score_earned = max(1, int(meteor_pool.meteor_max_size / meteor.width * 10))

                # add animation earned
                text_animations.append({
                    'text': f"+{score_earned}",
                    'x': meteor.x,
                    'y': meteor.y,
                    'alpha': 255,
                    'text_color': "#ffffff",
                    'timer': 180 # 3 seconds at 60FPS
                })

                score += score_earned


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
    text = hud_font.render(message, True, pygame.Color("#000000"))
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
                    bullet_pool.active_bullets.clear()
                    meteor_pool.active_meteors.clear()
                    start_time = pygame.time.get_ticks()
                    remaining_time = TIME_LIMIT
                    game_finished = False
                    last_generation_time = 0
                    waiting = False # close dialog
            
                # clicked on exit button
                elif mouse_x >= exit_button_x and mouse_x <= (exit_button_x + button_width) and mouse_y >= exit_button_y and mouse_y <= (exit_button_y + button_height):
                    waiting = False
                    running = False

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)

def update_text_animations():
    # update animations
    for anim in text_animations[:]:
        anim['timer'] -= 1
        anim['alpha'] = max(0, int(255 * (anim['timer'] / 180)))
        anim['y'] -= 1 

        if anim['timer'] <= 0:
            text_animations.remove(anim)

def update():
    update_time()
    player.update()

    meteor_pool.handle_meteor_generation()
    meteor_pool.update_all()

    enemy_pool.handle_enemy_generation()
    enemy_pool.update_all(player)    

    bullet_pool.update_all()
    check_collisions()
    update_text_animations()

def render_hud():
    score_label = hud_font.render(f"Score: {score}", True, pygame.Color('#ffffff'))
    screen.blit(score_label, (0, 0))

    timer_label = hud_font.render(f"Time: {remaining_time // 1000}s", True, pygame.Color("#ffffff"))
    screen.blit(timer_label, (SCREEN_WIDTH - 155, 0))

def render_text_animations():
    for anim in text_animations:
        text_surf = button_font.render(anim['text'], True, pygame.Color(anim['text_color']))
        text_surf.set_alpha(anim['alpha'])
        screen.blit(text_surf, (anim['x'], anim['y']))

def render():
    screen.fill(BACKGROUND_COLOR)
    player.render(screen)
    meteor_pool.render_all(screen)
    enemy_pool.render_all(screen)
    bullet_pool.render_all(screen)
    render_hud()
    render_text_animations()

    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)
