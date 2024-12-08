# Description: Contains the classes for the game elements (Tower, Enemy, Projectile)
import pygame
from colors import *
import math

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x              # X-coordinate
        self.y = y              # Y-coordinate
        self.range = 200        # Range in pixels (current)
        self.cooldown = 150     # Cooldown in milliseconds
        self.last_shot = 0      # Time of the last shot
        self.health = 100       # Health points (current)
        self.max_health = 100   # Store the maximum health

    def shoot(self, enemies, projectiles,attackSpeedFactor):
        # Shoot if cooldown has elapsed
        if pygame.time.get_ticks() - self.last_shot > self.cooldown/attackSpeedFactor:

            # Find the nearest enemy
            for enemy in enemies:
                distance = math.hypot(enemy.x - self.x, enemy.y - self.y)

                # Shoot if the enemy is within range
                if distance < self.range:
                    projectiles.append(Projectile(self.x, self.y, enemy))
                    self.last_shot = pygame.time.get_ticks()
                    break

    def draw(self, screen):
        # Draw the tower
        pygame.draw.circle(screen, BLACK, (self.x, self.y), 20)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.range, 1)

        # Draw the health bar
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        # Calculate health bar dimensions
        bar_width = 40
        bar_height = 5
        health_ratio = self.health / self.max_health
        health_bar_width = bar_width * health_ratio

        # Draw the health bar background
        pygame.draw.rect(screen, BLACK, (self.x - bar_width // 2, self.y + 30, bar_width, bar_height))

        # Draw the health bar foreground
        pygame.draw.rect(screen, RED, (self.x - bar_width // 2, self.y + 30, health_bar_width, bar_height))

    def updateRange(self, range):
        self.range = range

    def updateHealth(self, health):
        self.health = health

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