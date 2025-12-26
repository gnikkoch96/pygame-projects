from entities.ball import Ball
from entities.brick import Brick
from entities.player import Player
from typing import List, Dict, Union
from config import SCREEN_HEIGHT, SCREEN_WIDTH
from utils.brick_generation import generate_bricks_by_row

class GameState:
    def __init__(self):
        self.score = 0
        self.running = True
        self.level = 1
        self.ball: Ball = Ball(0, 0)
        self.player: Player = Player(SCREEN_WIDTH //2, SCREEN_HEIGHT - 25, self.ball)
        self.bricks: List[Brick] = generate_bricks_by_row(self.level)
        self.text_animations: List[Dict[str, Union[str, int]]] = []

    def reset(self):
        self.score = 0
        self.running = True
        self.player.ball_attached = True
        self.player.reset_ball()
        self.player.lives = 3
        self.bricks: List[Brick] = generate_bricks_by_row(self.level)

    def next_level(self):
        self.level += 1
        self.reset()
