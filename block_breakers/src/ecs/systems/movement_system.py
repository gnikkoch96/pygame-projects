from src.ecs.system import System
from src.ecs.components.position import Position
from src.ecs.components.velocity import Velocity

class MovementSystem(System):
    def update(self, entities, dt):
        for e in entities:
            pos = e.get_component(Position)
            vel = e.get_component(Velocity)
            if pos and vel:
                pos.x += vel.vx * dt
                pos.y += vel.vy * dt
