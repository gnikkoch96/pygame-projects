import pygame
from utils.collision import handle_collision
from utils.brick_generation import generate_bricks_by_row
from utils.game_state import GameState
from entities.ball import Ball
from entities.player import Player
from entities.brick import Brick
from typing import List
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOR, FPS, DEBUG_MODE

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True
game_state: GameState = GameState()

# ui objs
hud_font: pygame.font.SysFont = pygame.font.SysFont(None, 48)

# game objs
ball: Ball = Ball(0, 0)
player: Player = Player(SCREEN_WIDTH //2, SCREEN_HEIGHT - 25, ball)
bricks: List[Brick] = generate_bricks_by_row(3)

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    if DEBUG_MODE:
        ball.handle_input()

def update():
    handle_collision(game_state, ball, player, bricks)
    player.update()

    for brick in bricks:
        brick.update()

    if not player.ball_attached:
        ball.update()

def render_hud():
    score_label = hud_font.render(f"Score: {game_state.score}", True, pygame.Color("#ffffff"))
    screen.blit(score_label, (10, 10))

def render():
    screen.fill(pygame.Color(BACKGROUND_COLOR))

    for brick in bricks:
        brick.render(screen)

    player.render(screen)
    ball.render(screen)
    render_hud()

    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)