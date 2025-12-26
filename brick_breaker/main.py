import pygame
from utils.collision import handle_collision
from utils.dialogs import show_dialog
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
    if not game_state.running: return

    left_mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_mouse_clicked = True

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    # mouse_pressed = pygame.mouse.get_pressed() # this is for listening for mouse hold
    game_state.player.handle_input(keys, mouse_pos, left_mouse_clicked)

    if DEBUG_MODE:
        game_state.ball.handle_input()

def update():
    handle_collision(game_state)
    game_state.player.update()

    for brick in game_state.bricks:
        brick.update()

    if not game_state.player.ball_attached:
        game_state.ball.update()

    for text_anim in game_state.text_animations[:]:
        text_anim['timer'] -= 1
        text_anim['alpha'] = max(0, int(255 * (text_anim['timer'] / 180)))
        text_anim['y'] -= 1 

        if text_anim['timer'] <= 0:
            game_state.text_animations.remove(text_anim)

def render_hud():
    score_label = hud_font.render(f"Score: {game_state.score}", True, pygame.Color("#ffffff"))
    screen.blit(score_label, (10, 10))

    lives_label = hud_font.render(f"Lives: {game_state.player.lives}", True, pygame.Color("#ffffff"))
    screen.blit(lives_label, (SCREEN_WIDTH - 140, 10))

def render():
    screen.fill(pygame.Color(BACKGROUND_COLOR))

    for brick in game_state.bricks:
        brick.render(screen)

    game_state.player.render(screen)
    game_state.ball.render(screen)
    render_hud()

    for anim in game_state.text_animations:
        text_surf = button_font.render(anim['text'], True, pygame.Color(anim['text_color']))
        text_surf.set_alpha(anim['alpha'])
        screen.blit(text_surf, (anim['x'], anim['y']))

    pygame.display.flip()

    if game_state.player.lives <= 0:
        show_dialog(screen, game_state, dialog_font, button_font, True)
        
    if len(game_state.bricks) <= 12:
        show_dialog(screen, game_state, dialog_font, button_font, False, True)

while game_state.running:
    check_input()
    update()
    render()
    clock.tick(FPS)