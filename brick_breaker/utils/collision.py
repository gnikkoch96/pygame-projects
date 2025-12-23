from utils.game_state import GameState
import random
import math  # Add this import at the top if not present

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
            # Calculate current speed (magnitude) and angle
            speed = math.hypot(game_state.ball.speed_x, game_state.ball.speed_y)
            current_angle = math.atan2(game_state.ball.speed_y, game_state.ball.speed_x)
            
            # Reflect angle over horizontal (bounce off top)
            reflected_angle = -current_angle
            
            # Add small random variation to angle (e.g., ±30 degrees)
            angle_variation = random.uniform(-math.pi/6, math.pi/6)
            new_angle = reflected_angle + angle_variation
            
            # print(f"Old Angle: {math.degrees(current_angle):.2f}, Reflected Angle: {math.degrees(reflected_angle):.2f}, New Angle: {math.degrees(new_angle):.2f}")

            # Set new velocities based on speed and new angle
            game_state.ball.speed_x = speed * math.cos(new_angle)
            game_state.ball.speed_y = speed * math.sin(new_angle)
            
            # decrease brick hp
            brick.hp -= 1
            if brick.hp <= 0:
                # remove from bricks
                game_state.bricks.remove(brick)

            # update score
            game_state.score += 100

            # add animation earned
            game_state.text_animations.append({
                'text': f"+{100}",
                'x': brick.x,
                'y': brick.y,
                'alpha': 255,
                'text_color': "#ffffff",
                'timer': 180 # 3 seconds at 60FPS
            })





