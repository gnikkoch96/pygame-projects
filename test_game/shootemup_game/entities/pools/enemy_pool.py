import pygame
import random
from typing import List
from entities.enemy import Enemy
from config import SCREEN_WIDTH

class EnemyPool: 
    def __init__(self, max_enemies: int = 2):
        self.pool = [Enemy(0, 0, 0) for _ in range(max_enemies)]
        self.active_enemies: List[Enemy] = []

    def handle_enemy_generation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_meteor_spawn > self.spawn_rate:
            rand_x = random.randint(0, SCREEN_WIDTH) # we should also subtract by meteor size if possible for the max range
            
            rand_size = random.randint(self.meteor_min_size, self.meteor_max_size)
            rand_speed = random.randint(self.meteor_min_speed, self.meteor_max_speed)
            self.get_meteor(rand_x, 0, rand_size, rand_speed)
            self.last_meteor_spawn = current_time

    def get_enemy(self, x: int, y: int, hp: int, speed: int, shot_cooldown: int = 1000):
        if self.pool:
            enemy = self.pool.pop()
            enemy.x = x
            enemy.y = y
            enemy.hp = hp
            enemy.speed = speed
            enemy.shot_cooldown = shot_cooldown
        else:
            enemy = Enemy(x, y, hp, speed, shot_cooldown)
        
        self.active_enemies.append(enemy)
        return enemy

    def update_all(self):
        for enemy in self.active_enemies:
            enemy.update()

            if enemy.hp == 0: 
                enemy.is_alive = False

            if not enemy.is_alive:
                self.active_enemies.remove(enemy)
                self.pool.append(enemy)
        
    def render_all(self):
        for enemy in self.active_enemies:
            enemy.render()
