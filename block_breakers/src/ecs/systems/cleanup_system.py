from src.ecs.system import System
from src.ecs.components.brick import Brick

class CleanupSystem(System):
    def update(self, entities, dt):
        # remove bricks with <=0 hp
        to_remove = []
        for e in entities:
            brick = e.get_component(Brick)
            if brick and brick.hit_points <= 0:
                to_remove.append(e)
        for e in to_remove:
            entities.remove(e)
