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
screen = pygame.display.set_mode(WORLD_WIDTH, WORLD_HEIGHT)
done = False

clock = pygame.time.Clock() # Game clock

# Player data
pos = Vector(300, 30)
vel = Vector(0, 0)
player = Player(pos, vel, 25)


# Run in a loop
while not done:

    # Check for game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update player
    player.update()

    # Draw player
    screen.fill(BACKGROUND_COLOR)
    player.draw(screen)

    # Flip buffer
    pygame.display.flip()

    # Tick clock at 60FPS
    clock.tick(60)