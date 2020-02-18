"""
Galen Atkinson
GDD 3400
HW - Intro to PyGame
"""

import pygame
from Vector import Vector
from Player import Player
from Constants import *

# Initiate program
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
done = False

clock = pygame.time.Clock() # Game clock

# Player data
pos = Vector(PLAYER_START_X, PLAYER_START_Y)
player = Player(pos, PLAYER_SIZE, PLAYER_MOVE_SPEED)


# Run in a loop
while not done:

    # Check for game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update agents
    player.update()

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw agents
    player.draw(screen)

    # Flip buffer
    pygame.display.flip()

    # Tick clock at 60FPS
    clock.tick(FRAME_RATE)