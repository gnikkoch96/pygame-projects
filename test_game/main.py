import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Game settings
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 2
ENEMY_BULLET_SPEED = 4

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(CYAN)
        # Draw a simple ship shape
        pygame.draw.polygon(self.image, BLUE, [(25, 0), (50, 40), (25, 30), (0, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = PLAYER_SPEED
        self.health = 100
        self.shoot_cooldown = 0

    def update(self):
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top, -BULLET_SPEED)
            self.shoot_cooldown = 15
            return bullet
        return None

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type=0):
        super().__init__()
        self.enemy_type = enemy_type

        if enemy_type == 0:  # Basic enemy
            self.image = pygame.Surface((40, 30))
            self.image.fill(RED)
            self.health = 1
            self.score_value = 10
        elif enemy_type == 1:  # Stronger enemy
            self.image = pygame.Surface((50, 40))
            self.image.fill(YELLOW)
            self.health = 3
            self.score_value = 30
        else:  # Boss-like enemy
            self.image = pygame.Surface((70, 60))
            self.image.fill(GREEN)
            self.health = 5
            self.score_value = 50

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.shoot_cooldown = random.randint(30, 90)

    def update(self):
        self.rect.y += self.speed

        # Update shooting cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0 and random.random() < 0.02:
            bullet = Bullet(self.rect.centerx, self.rect.bottom, ENEMY_BULLET_SPEED)
            self.shoot_cooldown = random.randint(60, 120)
            return bullet
        return None

    def hit(self):
        self.health -= 1
        return self.health <= 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        if speed < 0:  # Player bullet
            self.image.fill(CYAN)
        else:  # Enemy bullet
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = random.randint(-5, 5)
        self.vel_y = random.randint(-5, 5)
        self.lifetime = 30

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()

    def reset_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score = 0
        self.wave = 1
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.game_over = False

    def spawn_enemy(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(-100, -40)

        # Determine enemy type based on wave
        rand = random.random()
        if self.wave >= 5 and rand < 0.1:
            enemy_type = 2  # Boss-like
        elif self.wave >= 3 and rand < 0.3:
            enemy_type = 1  # Stronger
        else:
            enemy_type = 0  # Basic

        enemy = Enemy(x, y, enemy_type)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def create_explosion(self, x, y, color, count=10):
        for _ in range(count):
            particle = Particle(x, y, color)
            self.all_sprites.add(particle)
            self.particles.add(particle)

    def run(self):
        running = True

        while running:
            self.clock.tick(FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.game_over:
                        bullet = self.player.shoot()
                        if bullet:
                            self.all_sprites.add(bullet)
                            self.player_bullets.add(bullet)
                    elif event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            if not self.game_over:
                # Update
                self.all_sprites.update()

                # Enemy spawning
                enemies_per_wave = 5 + self.wave * 2
                if self.enemies_spawned < enemies_per_wave:
                    self.spawn_timer += 1
                    if self.spawn_timer >= 60:  # Spawn every second
                        self.spawn_enemy()
                        self.enemies_spawned += 1
                        self.spawn_timer = 0
                elif len(self.enemies) == 0:
                    # Next wave
                    self.wave += 1
                    self.enemies_spawned = 0

                # Enemy shooting
                for enemy in self.enemies:
                    bullet = enemy.shoot()
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.enemy_bullets.add(bullet)

                    # Check if enemy reached bottom
                    if enemy.rect.top > SCREEN_HEIGHT:
                        enemy.kill()
                        self.player.health -= 10

                # Collision detection - Player bullets hit enemies
                for bullet in self.player_bullets:
                    hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
                    if hit_enemies:
                        bullet.kill()
                        for enemy in hit_enemies:
                            if enemy.hit():
                                self.score += enemy.score_value
                                self.create_explosion(enemy.rect.centerx, enemy.rect.centery,
                                                    YELLOW if enemy.enemy_type == 1 else RED, 15)
                                enemy.kill()
                            else:
                                self.create_explosion(enemy.rect.centerx, enemy.rect.centery,
                                                    WHITE, 5)

                # Collision detection - Enemy bullets hit player
                hit_bullets = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
                if hit_bullets:
                    self.player.health -= len(hit_bullets) * 10
                    self.create_explosion(self.player.rect.centerx, self.player.rect.centery,
                                        CYAN, 8)

                # Collision detection - Enemies hit player
                hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
                if hit_enemies:
                    self.player.health -= len(hit_enemies) * 20
                    for enemy in hit_enemies:
                        self.create_explosion(enemy.rect.centerx, enemy.rect.centery, RED, 15)

                # Check game over
                if self.player.health <= 0:
                    self.game_over = True
                    self.create_explosion(self.player.rect.centerx, self.player.rect.centery,
                                        CYAN, 30)

            # Draw
            self.screen.fill(BLACK)

            # Draw stars background
            for i in range(50):
                x = (i * 37) % SCREEN_WIDTH
                y = (i * 73 + pygame.time.get_ticks() // 20) % SCREEN_HEIGHT
                pygame.draw.circle(self.screen, WHITE, (x, y), 1)

            self.all_sprites.draw(self.screen)

            # Draw UI
            score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
            wave_text = self.small_font.render(f"Wave: {self.wave}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(wave_text, (10, 40))

            # Health bar
            health_width = 200
            health_height = 20
            health_x = SCREEN_WIDTH - health_width - 10
            health_y = 10
            pygame.draw.rect(self.screen, RED, (health_x, health_y, health_width, health_height))
            if self.player.health > 0:
                current_health_width = int((self.player.health / 100) * health_width)
                pygame.draw.rect(self.screen, GREEN, (health_x, health_y, current_health_width, health_height))
            pygame.draw.rect(self.screen, WHITE, (health_x, health_y, health_width, health_height), 2)

            health_text = self.small_font.render(f"Health: {max(0, self.player.health)}", True, WHITE)
            self.screen.blit(health_text, (health_x, health_y + 25))

            # Game over screen
            if self.game_over:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(128)
                overlay.fill(BLACK)
                self.screen.blit(overlay, (0, 0))

                game_over_text = self.font.render("GAME OVER", True, RED)
                final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
                wave_reached_text = self.small_font.render(f"Wave Reached: {self.wave}", True, WHITE)
                restart_text = self.small_font.render("Press R to Restart", True, GREEN)

                self.screen.blit(game_over_text,
                               (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
                self.screen.blit(final_score_text,
                               (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 270))
                self.screen.blit(wave_reached_text,
                               (SCREEN_WIDTH // 2 - wave_reached_text.get_width() // 2, 320))
                self.screen.blit(restart_text,
                               (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 370))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
