import pygame
import logging
from src.ecs.entity import Entity
from src.ecs.components.position import Position
from src.ecs.components.velocity import Velocity
from src.ecs.components.renderable import Renderable
from src.ecs.components.paddle import Paddle
from src.ecs.components.ball import Ball
from src.ecs.components.brick import Brick
from src.ecs.systems.input_system import InputSystem
from src.ecs.systems.movement_system import MovementSystem
from src.ecs.systems.collision_system import CollisionSystem
from src.ecs.systems.render_system import RenderSystem
from src.ecs.systems.cleanup_system import CleanupSystem
from src.game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Game factory helpers
def create_paddle(x, y):
    e = Entity()
    e.add_component(Position(x, y))
    e.add_component(Renderable(100, 20, (180, 180, 50)))
    e.add_component(Paddle())
    return e

def create_ball(x, y):
    e = Entity()
    e.add_component(Position(x, y))
    e.add_component(Velocity(200, -200))
    e.add_component(Ball(radius=8, speed=280))
    return e

def create_brick(x, y, w=64, h=24, hp=1, color=(100, 160, 220)):
    e = Entity()
    e.add_component(Position(x, y))
    e.add_component(Renderable(w, h, color))
    e.add_component(Brick(hit_points=hp, score=100))
    return e

def build_level(rows=5, cols=10, top=100, h_gap=4, v_gap=4, brick_w=64, brick_h=24):
    """Build a centered grid of bricks."""
    total_width = cols * brick_w + (cols - 1) * h_gap
    offset_x = (SCREEN_WIDTH - total_width) / 2
    offset_y = top
    bricks = []
    for r in range(rows):
        for c in range(cols):
            x = offset_x + c * (brick_w + h_gap)
            y = offset_y + r * (brick_h + v_gap)
            bricks.append(create_brick(
                x, y, brick_w, brick_h,
                hp=1 + r // 2,
                color=(100 + r * 20, 120 + c * 5, 180)
            ))
    return bricks

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Block Breaker - ECS")
    clock = pygame.time.Clock()
    running = True

    # Entities
    entities = []
    paddle = create_paddle(SCREEN_WIDTH/2 - 50, SCREEN_HEIGHT - 40)
    ball = create_ball(SCREEN_WIDTH/2 - 8, SCREEN_HEIGHT/2)
    entities.extend([paddle, ball])
    entities.extend(build_level())

    # Systems
    input_system = InputSystem(SCREEN_WIDTH)
    movement_system = MovementSystem()
    collision_system = CollisionSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    render_system = RenderSystem(screen)
    cleanup_system = CleanupSystem()

    font = pygame.font.SysFont(None, 24)
    score = 0

    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        input_system.update(entities, dt)
        movement_system.update(entities, dt)
        collision_system.update(entities, dt)
        cleanup_system.update(entities, dt)

        # recompute score (simple: (initial bricks - remaining)*100)
        remaining_bricks = sum(1 for e in entities if e.get_component(Brick))
        total_bricks = 5 * 10  # keep in sync with build_level defaults
        score = (total_bricks - remaining_bricks) * 100

        render_system.update(entities, dt)
        txt = font.render(f"Score: {score}", True, (250,250,250))
        screen.blit(txt, (10, 10))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
