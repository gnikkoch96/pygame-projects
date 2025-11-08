import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BACKGROUND_COLOR, FPS
from entities.player import Player
from entities.enemy import Enemy
from entities.meteor import Meteor
from entities.pools.bullet_pool import BulletPool
from entities.pools.meteor_pool import MeteorPool

pygame.init()

screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shoot em\' Up Game')

# fps limiter
clock: pygame.time.Clock = pygame.time.Clock()

# game logic
running: bool = True

# game objs
bullet_pool: BulletPool = BulletPool()
player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 25, bullet_pool)
enemy = Enemy(100, 100, 1, [(0, 0), (SCREEN_HEIGHT + 100)])


meteor_pool: MeteorPool = MeteorPool()
last_meteor_spawn: int = 0
meteor_spawn_rate: int = 2000

def handle_meteor_generation():
    global last_meteor_spawn
    # print("Calling Meteors!")

    current_time = pygame.time.get_ticks()
    if current_time - last_meteor_spawn > meteor_spawn_rate:
        rand_x = random.randint(0, SCREEN_WIDTH) # we should also subtract by meteor size if possible for the max range
        rand_size = random.randint(10, 50)
        rand_speed = random.randint(1, 5)
        meteor_pool.get_meteor(rand_x, 0, rand_size, rand_speed)
        last_meteor_spawn = current_time

def check_input():
    global running

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_input(keys)

def update():
    # meteor generation
    handle_meteor_generation()

    player.update()
    meteor_pool.update_all()
    bullet_pool.update_all()

def render():
    screen.fill(BACKGROUND_COLOR)
    player.render(screen)
    meteor_pool.render_all(screen)
    bullet_pool.render_all(screen)

    pygame.display.flip()

while running:
    check_input()
    update()
    render()
    clock.tick(FPS)
