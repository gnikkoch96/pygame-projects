from typing import List
from entities.brick import Brick
from config import SCREEN_WIDTH

# return the brick list and their positions on the screen
def generate_bricks_by_row(max_rows: int, brick_width: int = 50, brick_height: int = 20) -> List[Brick]:
    # control max limit of rows of bricks to fit on screen
    if max_rows >= 6: max_rows = 6

    bricks: List[Brick] = []
    brick_spacing = 10
    top_margin = 50
    left_margin = 15

    bricks_per_row = SCREEN_WIDTH // (brick_width + brick_spacing)

    for row in range(max_rows):
        for col in range(bricks_per_row):            
            x = left_margin + col * (brick_width + brick_spacing)
            y = top_margin + (row * (brick_height + brick_spacing))

            if x + brick_width > SCREEN_WIDTH:
                continue # skip brick generation

            # create brick
            brick = Brick(x, y, '#ffffff', 3 - row % max_rows)
            bricks.append(brick)

    return bricks

def generate_bricks_by_brick(max_bricks: int, brick_width: int = 50, brick_height: int = 20) -> List[Brick]:
    # control max limit on number of bricks to fit on screen
    if max_bricks >= 60: max_bricks = 60

    bricks: List[Brick] = []
    brick_spacing = 10
    top_margin = 50
    left_margin = 15

    bricks_per_row = SCREEN_WIDTH // (brick_width + brick_spacing)

    for i in range(max_bricks):
        row = i // bricks_per_row
        col = i % bricks_per_row

        x = left_margin + col * (brick_width + brick_spacing)
        y = top_margin + (row * (brick_height + brick_spacing))

        if x + brick_width > SCREEN_WIDTH:
            continue # skip brick generation

        # create brick
        brick = Brick(x, y, '#ffffff')
        bricks.append(brick)

    return bricks