from typing import List
from entities.brick import Brick
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# return the brick list and their positions on the screen
def generate_bricks(num_bricks: int):
    # control max limit on number of bricks to fit on screen
    if num_bricks >= 128: num_bricks = 128

    bricks: List[Brick] = []

    for brick in range(num_bricks):
        brick = Brick(0, 0, )


    
