#Test python script for Caroline dev
#Linking to github

import pygame
import random
import math

# Initialize Pygame
pygame.init()

#Welcome the user to the game
print("Welcome to the Tower Defense Game!")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caroline's Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x              # X-coordinate
        self.y = y              # Y-coordinate
        self.range = 200        # Range in pixels
        self.cooldown = 150     # Cooldown in milliseconds
        self.last_shot = 0      # Time of the last shot

    def shoot(self, enemies, projectiles):
        # Shoot if cooldown has elapsed
        if pygame.time.get_ticks() - self.last_shot > self.cooldown:

            # Find the nearest enemy
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)

                # Shoot if the enemy is within range
                if distance < self.range:
                    projectiles.append(Projectile(self.x, self.y, enemy))
                    self.last_shot = pygame.time.get_ticks()
                    break

    def draw(self, screen):
        pygame.draw.circle(screen, GREEN, (self.x, self.y), 20)
        pygame.draw.circle(screen, GREEN, (self.x, self.y), self.range, 1)

# Enemy class
class Enemy:
    def __init__(self, x, y, tower_x, tower_y):
        self.x = x
        self.y = y
        self.tower_x = tower_x
        self.tower_y = tower_y
        self.speed = 2
        self.health = 100

    def move(self):
        # Calculate direction vector
        direction_x = self.tower_x - self.x
        direction_y = self.tower_y - self.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        # Normalize direction vector
        direction_x /= distance
        direction_y /= distance

        # Update position
        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

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

        direction_x = self.target.x - self.x
        direction_y = self.target.y - self.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        direction_x /= distance
        direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

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
            enemies.append(Enemy(random.randint(0, WIDTH), 0, tower.x, tower.y))

        # Move enemies
        for enemy in enemies:
            enemy.move()
            enemy.draw(screen)

        # Shoot projectiles
        tower.shoot(enemies, projectiles)

        # Move projectiles
        for projectile in projectiles:

            # Delete the projectile if the target is destroyed
            if projectile.target not in enemies:
                projectiles.remove(projectile)

            #Otherwise, move the projectile
            projectile.move()
            projectile.draw(screen)

        # Check for collisions
        for projectile in projectiles[:]:
            for enemy in enemies[:]:
                distance = math.hypot(projectile.x - enemy.x, projectile.y - enemy.y)
                if distance < 10:  # Assuming 10 is the collision threshold
                    enemy.health -= 50  # Reduce enemy health
                    projectiles.remove(projectile)  # Remove projectile
                    if enemy.health <= 0:
                        enemies.remove(enemy)  # Remove enemy if health is zero

        # Draw tower
        tower.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
