import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, FPS


pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sprite Rendering Test')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

def update():
    pass

def render():
    screen.fill(pygame.Color('#ffffff'))

    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)