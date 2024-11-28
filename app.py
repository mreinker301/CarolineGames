#Test python script for Caroline dev
#Linking to github

import pygame
import random
import math

# Initialize Pygame
pygame.init()

print("Starting game...")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 150
        self.cooldown = 30
        self.last_shot = 0

    def shoot(self, enemies, projectiles):
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:
            for enemy in enemies:
                if self.in_range(enemy):
                    projectiles.append(Projectile(self.x, self.y, enemy))
                    self.last_shot = pygame.time.get_ticks()
                    break

    def in_range(self, enemy):
        distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
        return distance <= self.range

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 20)
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.range, 1)

# Enemy class
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.health = 100

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, 20, 20))

# Projectile class
class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5

    def move(self):
        angle = math.atan2(self.target.y - self.y, self.target.x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)

# Main game loop
def main():
    clock = pygame.time.Clock()
    tower = Tower(WIDTH // 2, HEIGHT // 2)
    enemies = []
    projectiles = []
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Spawn enemies
        if random.randint(1, 60) == 1:
            enemies.append(Enemy(random.randint(0, WIDTH), 0))

        # Move enemies
        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

        # Shoot projectiles
        tower.shoot(enemies, projectiles)

        # Move projectiles
        for projectile in projectiles:
            projectile.move()
            projectile.draw(screen)

        # Draw tower
        tower.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
