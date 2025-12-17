import pygame
from utils.collision import handle_collision
from utils.game_state import GameState
from config import SCREEN_HEIGHT, SCREEN_WIDTH, BACKGROUND_COLOR, FPS, DEBUG_MODE

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Brick Breaker')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
game_state: GameState = GameState()

# ui objs
hud_font: pygame.font.SysFont = pygame.font.SysFont(None, 48)
dialog_font: pygame.font.SysFont = pygame.font.SysFont(None, 48)
button_font: pygame.font.SysFont = pygame.font.SysFont(None, 24)

def check_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    game_state.player.handle_input(keys, mouse_pos, mouse_pressed)

    if DEBUG_MODE:
        game_state.ball.handle_input()

def update():
    handle_collision(game_state)
    game_state.player.update()

    for brick in game_state.bricks:
        brick.update()

    if not game_state.player.ball_attached:
        game_state.ball.update()

def render_hud():
    score_label = hud_font.render(f"Score: {game_state.score}", True, pygame.Color("#ffffff"))
    screen.blit(score_label, (10, 10))

def render():
    screen.fill(pygame.Color(BACKGROUND_COLOR))

    for brick in game_state.bricks:
        brick.render(screen)

    game_state.player.render(screen, game_state, dialog_font, button_font)
    game_state.ball.render(screen)
    render_hud()

    pygame.display.flip()

while game_state.running:
    check_input()
    update()
    render()
    clock.tick(FPS)