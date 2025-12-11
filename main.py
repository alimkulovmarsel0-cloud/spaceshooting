import pygame
import random
import math
import os

# --- 1. Initialization and Setup ---
pygame.init()

# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boss Battle Shooter - Shooting Boss")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (200, 50, 200)

# Game variables
running = True
clock = pygame.time.Clock()
FPS = 60
score = 0
BOSS_SCORE_TRIGGER = 15 
boss_active = False

# --- Set up Asset Paths ---
# IMPORTANT: Use your image paths here.
ASSET_DIR = 'assets'
try:
    PLAYER_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'player_ship.png')).convert_alpha()
    ENEMY_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'enemy_ship.png')).convert_alpha()
    BOSS_IMG = pygame.image.load(os.path.join(ASSET_DIR, 'boss_ship.png')).convert_alpha()
except pygame.error:
    print("WARNING: Could not load required image assets. Using fallback colored squares.")
    PLAYER_IMG = None
    ENEMY_IMG = None
    BOSS_IMG = None

# --- Helper Functions (Same as before) ---

def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health_bar(surf, x, y, health_percent, width, height, color_high, color_low):
    if health_percent < 0: health_percent = 0
    bar_fill = health_percent * width
    
    outline_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, bar_fill, height)
    
    pygame.draw.rect(surf, color_low, outline_rect) 
    pygame.draw.rect(surf, color_high, fill_rect) 
    pygame.draw.rect(surf, WHITE, outline_rect, 2) 

# --- 2. Sprite Classes ---

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, default_width=50, default_height=50, default_color=PURPLE):
        super().__init__()
        
        if image:
            self.image = image
        else:
            self.image = pygame.Surface([default_width, default_height])
            self.image.fill(default_color)
            
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 

# (Player and Enemy classes remain the same as the previous version)

class Player(GameSprite):
    def __init__(self):
        img = pygame.transform.scale(PLAYER_IMG, (60, 60)) if PLAYER_IMG else None
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT - 50
        super().__init__(img, x, y, 60, 60, GREEN)
        self.speed = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = PlayerBullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        all_player_bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self):
        img = pygame.transform.scale(ENEMY_IMG, (40, 40)) if ENEMY_IMG else None
        x = random.randrange(20, SCREEN_WIDTH - 20)
        y = random.randrange(-150, -50) 
        super().__init__(img, x, y, 40, 40, RED)
        self.speed = random.randrange(2, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.centerx = random.randrange(20, SCREEN_WIDTH - 20)
            self.rect.y = random.randrange(-150, -50)

class Boss(GameSprite):
    def __init__(self):
        img = pygame.transform.scale(BOSS_IMG, (150, 150)) if BOSS_IMG else None
        x = SCREEN_WIDTH // 2
        y = -150 
        super().__init__(img, x, y, 150, 150, PURPLE) 
        
        self.max_health = 50 
        self.health = self.max_health
        self.speed = 2
        self.move_counter = 0
        self.move_dir = 1 
        self.fire_rate = 30 # Fire every 30 frames
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        
        # 1. Slow Vertical Descent
        if self.rect.y < 50:
            self.rect.y += self.speed
            return

        # 2. Horizontal Movement Pattern
        self.rect.x += self.speed * self.move_dir
        self.move_counter += 1
        
        if self.move_counter > 100:
            self.move_dir *= -1
            self.move_counter = 0

        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.move_dir *= -1
        
        # 3. Boss Shooting Logic
        if current_time - self.last_shot > (1000 / FPS) * self.fire_rate:
             self.shoot()
             self.last_shot = current_time
        
    def shoot(self):
        # Fire 3 bullets from 3 points along the boss's bottom edge
        pos1 = (self.rect.left + 20, self.rect.bottom)
        pos2 = (self.rect.centerx, self.rect.bottom)
        pos3 = (self.rect.right - 20, self.rect.bottom)
        
        for x, y in [pos1, pos2, pos3]:
            bullet = BossBullet(x, y)
            all_sprites.add(bullet)
            all_boss_bullets.add(bullet)
        
    def draw_health(self):
        health_percent = self.health / self.max_health
        draw_health_bar(screen, 
                        (SCREEN_WIDTH // 2) - 150, 
                        10, 
                        health_percent, 
                        300, 
                        20, 
                        GREEN, 
                        RED)
            
class PlayerBullet(GameSprite):
    # This class replaces the old 'Bullet' class, now specifically for the player
    def __init__(self, x, y):
        bullet_surface = pygame.Surface([5, 15])
        bullet_surface.fill(WHITE)
        
        super().__init__(bullet_surface, x, y, 5, 15, WHITE)
        self.speed = 10
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class BossBullet(GameSprite):
    def __init__(self, x, y):
        # Boss bullets are red circles/squares and move down
        bullet_surface = pygame.Surface([8, 8])
        # Use colorkey to make it a circle if desired, but surface is easier for now
        bullet_surface.fill(RED) 
        
        super().__init__(bullet_surface, x, y, 8, 8, RED)
        self.speed = 5 # Slower than player bullets
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        # Move the bullet DOWN
        self.rect.y += self.speed
        # Remove the bullet if it goes off-screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# --- 3. Sprite Groups Setup ---

all_sprites = pygame.sprite.Group()
all_player_bullets = pygame.sprite.Group() # Player bullets
all_boss_bullets = pygame.sprite.Group()   # Boss bullets
all_enemies = pygame.sprite.Group()
boss_group = pygame.sprite.Group() 

# (The rest of the setup logic remains the same)

player = Player()
all_sprites.add(player)

def spawn_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    all_enemies.add(enemy)

def reset_enemies(num=5):
    for enemy in all_enemies:
        enemy.kill()
    for i in range(num):
        spawn_enemy()

reset_enemies()

# --- 4. Game Loop ---
while running:
    clock.tick(FPS)

    # 4b. Event Handling (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # --- GAME STATE CHECK ---
    if not boss_active and score >= BOSS_SCORE_TRIGGER:
        boss_active = True
        
        # Clear the screen of existing enemies
        for enemy in all_enemies:
            enemy.kill()
        
        # Spawn the Boss
        the_boss = Boss()
        all_sprites.add(the_boss)
        boss_group.add(the_boss)

    # 4c. Update (Movement and Game Logic)
    all_sprites.update()

    # 4d. Collision Detection

    # --- Collision 1: Player Bullets hit targets (enemies or boss) ---
    if not boss_active:
        # Player bullets hit normal enemies
        hits = pygame.sprite.groupcollide(all_player_bullets, all_enemies, True, True)
        for bullet, enemies_hit in hits.items():
            score += len(enemies_hit)
            for enemy in enemies_hit:
                spawn_enemy() 
    else:
        # Player bullets hit the boss
        boss_hits = pygame.sprite.groupcollide(all_player_bullets, boss_group, True, False)
        for bullet in boss_hits:
            the_boss.health -= 1
            if the_boss.health <= 0:
                print("BOSS DEFEATED! You win!")
                score += 10 
                the_boss.kill()
                boss_active = False
                reset_enemies() 
                # Clear all boss bullets when the boss is killed
                for bullet in all_boss_bullets:
                    bullet.kill()
                
    # --- Collision 2: Boss Bullets hit player (NEW) ---
    player_hit_by_boss_bullet = pygame.sprite.spritecollide(player, all_boss_bullets, True)
    if player_hit_by_boss_bullet:
        # If the player is hit by a boss bullet, it's Game Over
        print(f"Game Over! Final Score: {score}")
        running = False
        
    # --- Collision 3: Enemies/Boss (Body) hit player (Same as before) ---
    if boss_active:
        player_hits = pygame.sprite.spritecollide(player, boss_group, False)
    else:
        player_hits = pygame.sprite.spritecollide(player, all_enemies, True)
        
    if player_hits:
        print(f"Game Over! Final Score: {score}")
        running = False 

    # 4e. Drawing / Rendering
    screen.fill(BLACK) 

    all_sprites.draw(screen)
    
    draw_text(screen, f"Score: {score}", 36, 10, 10)
    
    if boss_active:
        the_boss.draw_health()

    pygame.display.flip()

# --- 5. Quit Pygame ---
pygame.quit()