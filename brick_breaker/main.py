import pygame
from utils.collision import handle_collision
from entities.ball import Ball
from entities.player import Player
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOR, FPS, DEBUG_MODE


pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True

# game objs
ball: Ball = Ball(0, 0)
player: Player = Player(SCREEN_WIDTH //2, SCREEN_HEIGHT - 25, ball)

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
    handle_collision(ball, player, None)
    player.update()

    if not player.ball_attached:
        ball.update()

def render():
    screen.fill(pygame.Color(BACKGROUND_COLOR))
    player.render(screen)
    ball.render(screen)
    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)