import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Load background image
background_image = pygame.image.load("bg.jpg")  # Ensure you have an image file named bg.jpg
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# Player setup
player_size = 80  # Increase the player size
player_image = pygame.image.load("spaceship1.png")  # Ensure you have an image file named spaceship1.png
player_image = pygame.transform.scale(player_image, (player_size, player_size))  # Scale the player image
player_pos = [screen_width // 2, screen_height - 2 * player_size]
player_speed = 10

# Bullet setup
bullet_size = 20
bullet_speed = 15
bullets = []

# Enemy setup
enemy_size = 50
enemy_image = pygame.image.load("e.png")  # Ensure you have an image file named e.png
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))
enemy_speed = 10
enemies = []

# Game settings
clock = pygame.time.Clock()
game_over = False
score = 0
font = pygame.font.SysFont("monospace", 35)

# Function to drop enemies
def drop_enemies(enemies):
    delay = random.random()
    if len(enemies) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width - enemy_size)
        y_pos = 0
        enemies.append([x_pos, y_pos])

# Function to draw enemies
def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

# Function to update enemy positions
def update_enemy_positions(enemies):
    global game_over, score
    for idx, enemy in enumerate(enemies):
        if enemy[1] >= 0 and enemy[1] < screen_height:
            enemy[1] += enemy_speed
        else:
            enemies.pop(idx)
            score += 1

# Function to detect collisions
def detect_collisions(player_pos, enemies):
    for enemy in enemies:
        if (enemy[1] >= player_pos[1] and enemy[1] < player_pos[1] + player_size) or (enemy[1] + enemy_size >= player_pos[1] and enemy[1] + enemy_size < player_pos[1] + player_size):
            if (enemy[0] >= player_pos[0] and enemy[0] < player_pos[0] + player_size) or (enemy[0] + enemy_size >= player_pos[0] and enemy[0] + enemy_size < player_pos[0] + player_size):
                return True
    return False

# Function to draw bullets
def draw_bullets(bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, blue, (bullet[0], bullet[1], bullet_size, bullet_size))

# Function to update bullet positions
def update_bullet_positions(bullets):
    for idx, bullet in enumerate(bullets):
        if bullet[1] > 0:
            bullet[1] -= bullet_speed
        else:
            bullets.pop(idx)

# Function to detect bullet collisions with enemies
def detect_bullet_collisions(bullets, enemies):
    for bullet in bullets:
        for enemy in enemies:
            if (enemy[1] <= bullet[1] < enemy[1] + enemy_size) and (enemy[0] <= bullet[0] < enemy[0] + enemy_size):
                bullets.remove(bullet)
                enemies.remove(enemy)
                return True
    return False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_pos[0] - player_speed >= 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] + player_speed <= screen_width - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE]:
        bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1] - bullet_size]
        bullets.append(bullet_pos)

    screen.blit(background_image, (0, 0))  # Draw background

    drop_enemies(enemies)
    update_enemy_positions(enemies)
    draw_enemies(enemies)

    if detect_collisions(player_pos, enemies):
        game_over = True

    update_bullet_positions(bullets)
    draw_bullets(bullets)

    detect_bullet_collisions(bullets, enemies)

    screen.blit(player_image, (player_pos[0], player_pos[1]))

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
