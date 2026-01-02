from typing import List
from entities.brick import Brick
from config import SCREEN_WIDTH

# return the brick list and their positions on the screen
from math import ceil
from typing import List

def generate_bricks_by_row(max_rows: int, brick_width: int = 50, brick_height: int = 20) -> List["Brick"]:
    if max_rows >= 6:
        max_rows = 6

    bricks: List[Brick] = []
    brick_spacing = 10
    top_margin = 50

    bricks_per_row = SCREEN_WIDTH // (brick_width + brick_spacing)

    # --- bottom-up colors for your rules ---
    white_rows  = ceil(max_rows / 3)
    orange_rows = ceil((max_rows - 1) / 3)
    red_rows    = ceil((max_rows - 2) / 3)

    colors_bottom_up = (
        ["white"] * white_rows +
        ["orange"] * orange_rows +
        ["red"] * red_rows
    )

    # screen draws rows top->bottom, so flip to keep "white on bottom"
    colors_top_down = colors_bottom_up[::-1]

    # center horizontally
    total_w = bricks_per_row * (brick_width + brick_spacing) - brick_spacing
    start_x = (SCREEN_WIDTH - total_w) // 2

    # hp by color (adjust if yours differs)
    hp_map = {"white": 1, "orange": 2, "red": 3}

    for row in range(max_rows):
        color = colors_top_down[row]
        hp = hp_map[color]

        y = top_margin + row * (brick_height + brick_spacing)
        for col in range(bricks_per_row):
            x = start_x + col * (brick_width + brick_spacing)
            bricks.append(Brick(x, y, color, hp, brick_width, brick_height))

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