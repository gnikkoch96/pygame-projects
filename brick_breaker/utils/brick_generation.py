from typing import List
from entities.brick import Brick
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# return the brick list and their positions on the screen
def generate_bricks(num_bricks: int, brick_width: int = 50, brick_height: int = 20) -> List[Brick]:
    # control max limit on number of bricks to fit on screen
    if num_bricks >= 128: num_bricks = 128

    bricks: List[Brick] = []
    brick_spacing = 10
    top_margin = 50

    bricks_per_row = SCREEN_WIDTH // (brick_width + brick_spacing)
        
    for i in range(num_bricks):
        row = i // bricks_per_row
        col = i % bricks_per_row

        x = col * (brick_width + brick_spacing)
        y = top_margin + (row * (brick_height + brick_spacing))

        if x + brick_width > SCREEN_WIDTH:
            continue # skip brick generation

        # create brick
        brick = Brick(x, y, '#ffffff')
        bricks.append(brick)
    return bricks