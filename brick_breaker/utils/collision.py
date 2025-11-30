from entities.ball import Ball
from entities.player import Player

def handle_collision(ball: Ball, player: Player, brick):
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
