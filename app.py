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
pygame.display.set_caption("Tower Defense Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game class
class Game:
    def __init__(self):
        self.tower = Tower(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.projectiles = []
        self.running = True
        self.cash = 0
        self.speed = 1
        self.damageMult = 1
        self.attackSpeedMult = 1
    def updateSpeed(self, speed):
        self.speed = speed
    def reset(self):
        self.enemies = []
        self.projectiles = []
        self.cash = 0
        self.speed = 1

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 18)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x              # X-coordinate
        self.y = y              # Y-coordinate
        self.range = 200        # Range in pixels
        self.cooldown = 100     # Cooldown in milliseconds
        self.last_shot = 0      # Time of the last shot

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
        pygame.draw.rect(screen, RED, (self.x, self.y, 20, 20))

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

# Function to display cash
def display_cash(screen, cash):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Cash: ${cash}", True, BLACK)
    screen.blit(text_surface, (WIDTH - 150, 10))

# Function to display current game speed
def display_speed(screen, speed):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Speed: {speed}", True, BLACK)
    screen.blit(text_surface, (WIDTH - 150, 50))

# Main game loop
def main():
    
    #initialize game
    clock = pygame.time.Clock()
    game = Game()
    running = True


    # Create the buttons
    quitButton = Button(10, 10, 100, 30, "Quit", RED, WHITE)
    restartButton = Button(10, 50, 100, 30, "Restart", BLUE, WHITE)
    speedUpButton = Button(10, 90, 100, 30, "Speed Up", GREEN, WHITE)
    speedDownButton = Button(10, 130, 100, 30, "Speed Down", GREEN, WHITE)
    damageButton = Button(200, 550, 100, 30, "Damage", BLACK, WHITE)
    attackSpeedButton = Button(500, 550, 100, 30, "Attack Speed", BLACK, WHITE)


    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or quitButton.is_clicked(event):
                running = False
            if restartButton.is_clicked(event):
                game.reset()
            if speedUpButton.is_clicked(event):
                game.speed += 0.1
            if speedDownButton.is_clicked(event):
                game.speed -= 0.1
            if damageButton.is_clicked(event):
                game.damageMult += 0.1
                game.cash -= 100 * game.damageMult
            if attackSpeedButton.is_clicked(event):
                game.attackSpeedMult += 0.1
                game.cash -= 100 * game.attackSpeedMult

        # Spawn enemies
        if random.randint(1, 60) == 1:
            game.enemies.append(Enemy(random.randint(0, WIDTH), 0, game.tower.x, game.tower.y))

        # Draw button
        quitButton.draw(screen)
        restartButton.draw(screen)
        speedUpButton.draw(screen)
        speedDownButton.draw(screen)
        damageButton.draw(screen)
        attackSpeedButton.draw(screen)

        # Move enemies
        for enemy in game.enemies:
            enemy.move(game.speed)
            enemy.draw(screen)

        # Shoot projectiles
        game.tower.shoot(game.enemies, game.projectiles, game.attackSpeedMult)

        # Move projectiles
        for projectile in game.projectiles:

            # Delete the projectile if the target is destroyed
            if projectile.target not in game.enemies:
                game.projectiles.remove(projectile)

            #Otherwise, move the projectile
            projectile.move(game.speed)
            projectile.draw(screen)

        # Check for collisions
        for projectile in game.projectiles[:]:
            for enemy in game.enemies[:]:
                distance = math.hypot(projectile.x - enemy.x, projectile.y - enemy.y)
                if distance < 10:  # Assuming 10 is the collision threshold
                    enemy.health -= 50*game.damageMult  # Reduce enemy health
                    game.projectiles.remove(projectile)  # Remove projectile
                    if enemy.health <= 0:
                        game.enemies.remove(enemy)  # Remove enemy if health is zero
                        game.cash += 10

        # Draw tower
        game.tower.draw(screen)

        # Display cash
        display_cash(screen, game.cash)

        # Display speed
        display_speed(screen, game.speed)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
