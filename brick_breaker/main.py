import pygame
from entities.ball import Ball
from entities.player import Player
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOR, FPS


pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True

# game objs
ball: Ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player: Player = Player(SCREEN_WIDTH //2, SCREEN_HEIGHT - 25)

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update():
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