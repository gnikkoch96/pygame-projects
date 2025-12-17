import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from utils.game_state import GameState

def show_dialog(screen: pygame.Surface, game_state: GameState, font: pygame.font, button_font: pygame.font, is_game_over: bool = False, is_next_level: bool = False):
    global game_finished, running

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

    
    score_message = f"Your Final Score: {game_state.score}"
    text = font.render(score_message, True, pygame.Color("#D7A6A6"))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    # buttons
    button_width, button_height = 100, 50

    
    if is_next_level:
        next_level_x = dialog_x + (dialog_width - button_width) // 2 - 75
        next_level_y = dialog_y + dialog_height - button_height - 20
        pygame.draw.rect(screen, pygame.Color("#4CAF50"), (next_level_x, next_level_y, button_width, button_height))
        pygame.draw.rect(screen, pygame.Color("#000000"), (next_level_x, next_level_y, button_width, button_height), 1)


        button_text = button_font.render("Next Level", True, pygame.Color('#ffffff'))
        button_text_rect = button_text.get_rect(center=(retry_button_x + button_width // 2, retry_button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)

    elif is_game_over:
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
                    game_finished = False
                    waiting = False # close dialog
            
                # clicked on exit button
                elif mouse_x >= exit_button_x and mouse_x <= (exit_button_x + button_width) and mouse_y >= exit_button_y and mouse_y <= (exit_button_y + button_height):
                    waiting = False
                    running = False