#Test python script for Caroline dev
#Linking to github

import pygame
import random
import math
from colors import *
from gameElements import Tower, Enemy, Projectile

# Debug mode
DEBUG = True

# Initialize Pygame
pygame.init()

#Welcome the user to the game
print("Welcome to Caroline's Tower Defense Game!")

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caroline's Tower Defense Game")

# Game class
class Game:
    def __init__(self):
        self.tower = Tower(WIDTH // 2, HEIGHT // 2)
        self.enemies = []
        self.projectiles = []
        self.running = True
        self.cash = 0
        self.gameSpeed = 1
        self.damageMult = 1
        self.attackSpeedMult = 1
        self.mults = {"Damage": 1, "Attack Speed": 1, "Range": 1, "Health": 1}
    def updateSpeed(self, speed):
        self.gameSpeed = speed
    def reset(self):
        self.enemies = []
        self.projectiles = []
        self.cash = 0
        self.gameSpeed = 1
    def canUpgrade(self, key):
        return self.cash >= 100 * self.mults[key]
    def upgrade(self, key):
        self.cash -= 100 * self.mults[key]
        self.mults[key] += 0.1

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 14)

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

# Attribute class: Display the name of the attribute on the left and then make a button on the right which displays
# the current value of the attribute and the cost to upgrade it
class Attribute:
    def __init__(self, x, y, width, height, color, text_color, key, game):
        self.name_rect = pygame.Rect(x, y, width/2, height)
        self.value_rect = pygame.Rect(x + width/2, y, width/2, height/2)
        self.cost_rect = pygame.Rect(x + width/2, y + height/2, width/2, height/2)
        self.key = key
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 14)
        self.value = game.mults[key]
        self.cost = 100*self.value
        self.border_rect = pygame.Rect(x, y, width, height)  # Define the border rectangle

    def draw(self, screen):
        # Draw the border
        pygame.draw.rect(screen, self.text_color, self.border_rect, 2)  # Border with width 2

        # Draw the name of the attribute
        pygame.draw.rect(screen, self.color, self.name_rect)
        text_surface = self.font.render(self.key, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.name_rect.center)
        screen.blit(text_surface, text_rect)

        # Draw the value of the attribute
        pygame.draw.rect(screen, self.color, self.value_rect)
        text_surface = self.font.render(str(self.value), True, self.text_color)  # Ensure value is a string
        text_rect = text_surface.get_rect(center=self.value_rect.center)
        screen.blit(text_surface, text_rect)

        # Draw the cost of the attribute
        pygame.draw.rect(screen, self.color, self.cost_rect)
        text_surface = self.font.render("$"+str(self.cost), True, self.text_color)  # Ensure cost is a string
        text_rect = text_surface.get_rect(center=self.cost_rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.name_rect.collidepoint(event.pos) or self.value_rect.collidepoint(event.pos) or self.cost_rect.collidepoint(event.pos):
                return True

            

def display_game_state(screen, game):
    font = pygame.font.Font(None, 18)
    text_surface = font.render(f"Cash: ${round(game.cash)}", True, BLACK)
    screen.blit(text_surface, (WIDTH - 150, 10))
    text_surface = font.render(f"Speed: {game.gameSpeed}", True, BLACK)
    screen.blit(text_surface, (WIDTH - 150, 50))
    # text_surface = font.render(f"Damage Mult: {round(game.damageMult,1)}", True, BLACK)
    # screen.blit(text_surface, (WIDTH - 150, 90))
    # text_surface = font.render(f"Attack Speed Mult: {round(game.attackSpeedMult,1)}", True, BLACK)
    # screen.blit(text_surface, (WIDTH - 150, 130))

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
    damageButton = Button(200, 550, 100, 30, "Damage: $100", BLACK, WHITE)
    attackSpeedButton = Button(500, 550, 100, 30, "Attack Speed: $100", BLACK, WHITE)

    if DEBUG:
        test = Attribute(50, 550, 100, 30, WHITE, BLACK, "Damage", game)


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
                upgradeCost = 100 * game.damageMult
                if game.cash >= upgradeCost:
                    game.cash -= 100 * game.damageMult
                    game.damageMult += 0.1
                    damageButton.text = f"Damage: ${100 * game.damageMult}"
            if attackSpeedButton.is_clicked(event):
                upgradeCost = 100 * game.attackSpeedMult
                if game.cash >= upgradeCost:
                    game.cash -= 100 * game.attackSpeedMult
                    game.attackSpeedMult += 0.1
                    attackSpeedButton.text = f"Attack Speed: ${100 * game.attackSpeedMult}"
            if DEBUG:
                if test.is_clicked(event):
                    # Check to see if the player can upgrade the attribute
                    if game.canUpgrade(test.key):
                        game.upgrade(test.key)
                        test.value = game.mults[test.key]
                        test.cost = 100 * game.mults[test.key]

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

        if DEBUG:
            test.draw(screen)

        # Move enemies
        for enemy in game.enemies:
            enemy.move(game.gameSpeed)
            enemy.draw(screen)

        # Shoot projectiles
        game.tower.shoot(game.enemies, game.projectiles, game.attackSpeedMult)

        # Move projectiles
        for projectile in game.projectiles:

            # Delete the projectile if the target is destroyed
            if projectile.target not in game.enemies:
                game.projectiles.remove(projectile)

            #Otherwise, move the projectile
            projectile.move(game.gameSpeed)
            projectile.draw(screen)

        # Check for collisions between projectiles and enemies
        for projectile in game.projectiles[:]:
            for enemy in game.enemies[:]:
                distance = math.hypot(projectile.x - enemy.x, projectile.y - enemy.y)
                if distance < 10:  # Assuming 10 is the collision threshold
                    enemy.health -= 50*game.damageMult  # Reduce enemy health
                    game.projectiles.remove(projectile)  # Remove projectile
                    if enemy.health <= 0:
                        game.enemies.remove(enemy)  # Remove enemy if health is zero
                        game.cash += 10

        # Check for enermies reaching the tower
        for enemy in game.enemies[:]:
            distance = math.hypot(enemy.x - game.tower.x, enemy.y - game.tower.y)
            if distance < 10:
                game.tower.health -= 10
                if game.tower.health <= 0:
                    game.running = False

        # Draw tower
        game.tower.draw(screen)

        # Display game state
        display_game_state(screen, game)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
