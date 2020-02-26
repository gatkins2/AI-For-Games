"""
Galen Atkinson
GDD 3400
HW - Sheep Herding
"""

import pygame, random
from Vector import Vector
from Dog import Dog
from Sheep import Sheep
from Constants import *

# Initiate program
pygame.init()
screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
done = False

clock = pygame.time.Clock()     # Game clock

# Dog data
pos = Vector(DOG_START_X, DOG_START_Y)
dogSurface = pygame.image.load('collie.png')
dog = Dog(pos, DOG_WIDTH, DOG_HEIGHT, DOG_MOVE_SPEED, dogSurface)

# Sheep data
sheeps = []
sheepSurface = pygame.image.load('sheep.png')
for i in range(10):
    pos = Vector(random.randint(0, WORLD_WIDTH - SHEEP_WIDTH), random.randint(0, WORLD_HEIGHT - SHEEP_HEIGHT))
    sheep = Sheep(pos, SHEEP_WIDTH, SHEEP_HEIGHT, SHEEP_MOVE_SPEED, sheepSurface)
    sheeps.append(sheep)

# Run in a loop
while not done:

    # Check for game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Update agents
    dog.update()
    for sheep in sheeps:
        sheep.update(dog)
    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw agents
    dog.draw(screen)
    for sheep in sheeps:
        sheep.draw(screen, dog)

    # Flip buffer
    pygame.display.flip()

    # Tick clock at 60FPS
    clock.tick(FRAME_RATE)
