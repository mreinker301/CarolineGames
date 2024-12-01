# Description: Contains the classes for the game elements (Tower, Enemy, Projectile)
import pygame
from colors import *
import math

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x              # X-coordinate
        self.y = y              # Y-coordinate
        self.range = 200        # Range in pixels
        self.cooldown = 100     # Cooldown in milliseconds
        self.last_shot = 0      # Time of the last shot
        self.health = 100       # Health points

    def shoot(self, enemies, projectiles, attackSpeedMult):
        # Shoot if cooldown has elapsed
        if pygame.time.get_ticks() - self.last_shot > self.cooldown/attackSpeedMult:

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
        self.edge = 20

    def move(self,speedFactor):
        # Calculate direction vector
        direction_x = self.tower_x - self.x
        direction_y = self.tower_y - self.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        # Normalize direction vector
        direction_x /= distance
        direction_y /= distance

        # Update position
        self.x += direction_x * self.speed * speedFactor
        self.y += direction_y * self.speed * speedFactor

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x - self.edge/2, self.y - self.edge/2, self.edge, self.edge))

# Projectile class
class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 5

    def move(self, speedFactor):

        direction_x = self.target.x - self.x
        direction_y = self.target.y - self.y
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        direction_x /= distance
        direction_y /= distance

        self.x += direction_x * self.speed * speedFactor
        self.y += direction_y * self.speed * speedFactor

    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), 5)