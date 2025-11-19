import pygame
import random
from typing import List
from entities.enemy import Enemy
from config import SCREEN_WIDTH
from entities.pools.bullet_pool import BulletPool
from entities.player import Player

class EnemyPool: 
    def __init__(self, bullet_pool: BulletPool, max_enemies: int = 2):
        self.pool = [Enemy(0, 0, 0, bullet_pool) for _ in range(max_enemies)]
        self.active_enemies: List[Enemy] = []
        self.last_enemy_spawn: int = 0
        self.spawn_rate: int = 1000
        self.max_spawn = 1
        self.max_enemy_hp = 1

    def handle_enemy_generation(self):
        if len(self.active_enemies) >= self.max_spawn: return

        current_time = pygame.time.get_ticks()
        if current_time - self.last_enemy_spawn > self.spawn_rate:
            rand_x = random.randint(0, SCREEN_WIDTH) # we should also subtract by meteor size if possible for the max range
            
            self.get_enemy(rand_x, 0, 2)

    def get_enemy(self, x: int, y: int, hp: int, speed: int = 2, shot_cooldown: int = 1000):
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

    def update_all(self, player: Player):
        for enemy in self.active_enemies:
            enemy.update(player)

            if not enemy.is_alive:
                # only start to spawn after the enemy has died
                self.last_enemy_spawn = pygame.time.get_ticks()
                self.active_enemies.remove(enemy)
                self.pool.append(enemy)
                enemy.is_alive = True # prevent from automatically being removed the moment they spawn
        
    def render_all(self, screen: pygame.Surface):
        for enemy in self.active_enemies:
            enemy.render(screen)
