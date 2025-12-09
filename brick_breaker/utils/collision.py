from entities.ball import Ball
from entities.player import Player
from entities.brick import Brick
from typing import List
import random

def handle_collision(ball: Ball, player: Player, bricks: List[Brick]):
    # ball -> paddle collision
    if ball.hitbox.colliderect(player.hitbox):
        # determine which part of the player the ball collided with
        if ball.hitbox.x - ball.radius  < player.hitbox.x + player.hitbox.width // 3:
            # left
            ball.speed_x = -abs(ball.speed_x)
        elif ball.hitbox.x + ball.radius > player.hitbox.x + (2 * player.hitbox.width // 3):
            # right
            ball.speed_x = abs(ball.speed_x)

        # reverse ball direction 
        ball.speed_y *= -1

    # ball -> brick collision
    for brick in bricks:
        if ball.hitbox.colliderect(brick.hitbox):
            # reverse ball
            ball.speed_y *= -1

            # randomize left or right direction
            ball.speed_x = random.choice([2, -2])

            # decrease brick hp
            brick.hp -= 1
            if brick.hp <= 0:
                # remove from bricks
                bricks.remove(brick)

            

            
