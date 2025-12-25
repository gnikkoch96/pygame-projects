from __future__ import annotations
import pygame
from entities.ball import Ball
from typing import Sequence, TYPE_CHECKING
from config import SCREEN_WIDTH, SCREEN_HEIGHT, DEBUG_MODE
from utils.dialogs import show_dialog

if TYPE_CHECKING:
    from utils.game_state import GameState

class Player:
    def __init__(self, x: int, y: int, ball: Ball, width: int = 100, height: int = 10, speed: int = 5, lives: int = 3):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = pygame.Color("#ffffff")
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.ball = ball
        self.ball_attached = True
        self.lives = lives

    def handle_input(self, keys: Sequence[bool], mouse_pos: Sequence[bool], left_mouse_clicked: bool):
        # mouse controls
        # self.x = mouse_pos[0] - self.width//2
        # self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        
        # if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x >= 0:
        #     self.x -= self.speed

        # if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x + self.width <= SCREEN_WIDTH:
        #     self.x += self.speed

        # let go of ball and/or speed up ball 
        if keys[pygame.K_SPACE] or left_mouse_clicked:
            # release the ball
            if self.ball_attached:
                self.ball_attached = False

                # add ball speed
                self.ball.speed_y = 10
            # else speed up the ball (while space is being hold)

    
    def reset_ball(self):
        self.ball.x = self.x + self.width // 2
        self.ball.y = self.y - self.ball.radius - 3
        self.ball.speed_x = 0
        self.ball.speed_y = 0

    def update(self):
        self.hitbox.topleft  = (self.x, self.y)

        if self.ball and self.ball_attached:
            self.reset_ball()

        if self.ball.y + self.ball.radius >= SCREEN_HEIGHT:
            if self.lives > 0:
                # reset ball pos
                self.ball_attached = True

                # lose a life
                self.lives -= 1


    def render(self, screen: pygame.Surface, game_state: GameState, font: pygame.font, button_font: pygame.font):
        pygame.draw.rect(screen, self.color, self.hitbox)

        if DEBUG_MODE: 
            pygame.draw.rect(screen, pygame.Color("#f90000"), self.hitbox, 1)     

        if self.lives <= 0:
            show_dialog(screen, game_state, font, button_font, True)   