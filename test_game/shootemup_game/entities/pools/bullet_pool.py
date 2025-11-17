import pygame
from typing import List
from entities.bullet import Bullet, BulletOwner, BulletDirection

class BulletPool: 
    def __init__(self, max_bullets: int = 100):
        self.pool = [Bullet(0, 0) for _ in range(max_bullets)]
        self.active_bullets: List[Bullet] = [] 
    
    def get_bullet(self, x: int, y: int, speed: int = 2, direction: BulletDirection = BulletDirection.UP) -> Bullet:
        if self.pool:
            # get existing bullet from pool (if possible)
            bullet = self.pool.pop()
            bullet.x = x
            bullet.y = y
            bullet.speed = speed
            bullet.direction = direction
            bullet.is_alive = True
        else:
            bullet = Bullet(x, y, speed, direction)
        
        self.active_bullets.append(bullet) 
        return bullet
    
    def update_all(self):
        for bullet in self.active_bullets[:]:
            bullet.update()

            # clean bullets by putting them back into the pool and removing them from the active bullets list
            if not bullet.is_alive:
                self.pool.append(bullet)
                self.active_bullets.remove(bullet)

    def render_all(self, screen: pygame.Surface):
        for bullet in self.active_bullets:
            bullet.render(screen)    