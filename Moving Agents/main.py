"""
Galen Atkinson
GDD 3400
HW - Moving Agents
"""

import pygame, random
from Vector import Vector
from Player import Player
from Enemy import Enemy
from EnemyHunter import EnemyHunter
from Constants import *

# Initiate program
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
done = False

clock = pygame.time.Clock() # Game clock

# Player data
pos = Vector(PLAYER_START_X, PLAYER_START_Y)
player = Player(pos, PLAYER_SIZE, PLAYER_MOVE_SPEED, PLAYER_COLOR)

# Enemy data
enemies = []
for i in range(5):
    pos = Vector(random.randint(0, WORLD_WIDTH - ENEMY_SIZE), random.randint(0, WORLD_HEIGHT - ENEMY_SIZE))
    enemy = Enemy(pos, ENEMY_SIZE, ENEMY_MOVE_SPEED, ENEMY_COLOR)
    enemies.append(enemy)
for i in range(5):
    pos = Vector(random.randint(0, WORLD_WIDTH - ENEMY_SIZE), random.randint(0, WORLD_HEIGHT - ENEMY_SIZE))
    enemy = EnemyHunter(pos, ENEMY_SIZE, ENEMY_MOVE_SPEED, ENEMY_HUNTER_COLOR)
    enemies.append(enemy)

# Run in a loop
while not done:

    # Check for game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update agents
    player.update()
    for enemy in enemies:
        enemy.update(player)

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw agents
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen, player)

    # Flip buffer
    pygame.display.flip()

    # Tick clock at 60FPS
    clock.tick(FRAME_RATE)