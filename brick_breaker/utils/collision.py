from utils.game_state import GameState
import random

def handle_collision(game_state: GameState):
    # ball -> paddle collision
    if game_state.ball.hitbox.colliderect(game_state.player.hitbox):
        # determine which part of the player the ball collided with
        if game_state.ball.hitbox.x - game_state.ball.radius  < game_state.player.hitbox.x + game_state.player.hitbox.width // 3:
            # left
            game_state.ball.speed_x = -abs(game_state.ball.speed_x)
        elif game_state.ball.hitbox.x + game_state.ball.radius > game_state.player.hitbox.x + (2 * game_state.player.hitbox.width // 3):
            # right
            game_state.ball.speed_x = abs(game_state.ball.speed_x)

        # reverse ball direction 
        game_state.ball.speed_y *= -1

    # ball -> brick collision
    for brick in game_state.bricks:
        if game_state.ball.hitbox.colliderect(brick.hitbox):
            # reverse ball
            game_state.ball.speed_y *= -1

            # randomize left or right direction
            game_state.ball.speed_x = random.choice([2, -2])

            # decrease brick hp
            brick.hp -= 1
            if brick.hp <= 0:
                # remove from bricks
                game_state.bricks.remove(brick)

            # update score
            game_state.score += 100


            

            
