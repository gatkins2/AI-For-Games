"""
Galen Atkinson
GDD 3400
HW - Sheep Herding
"""

import pygame, random
from Vector import Vector
from Dog import Dog
from Sheep import Sheep
import Constants

# Initiate program
pygame.init()
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
done = False

clock = pygame.time.Clock()     # Game clock

# Dog data
pos = pos = Vector(random.randint(0, Constants.WORLD_WIDTH - Constants.SHEEP_WIDTH), random.randint(0, Constants.WORLD_HEIGHT - Constants.SHEEP_HEIGHT))
dogSurface = pygame.image.load('collie.png')
dog = Dog(pos, Constants.DOG_MOVE_SPEED, dogSurface)

# Sheep data
sheeps = []
sheepSurface = pygame.image.load('sheep.png')
for i in range(100):
    pos = Vector(random.randint(0, Constants.WORLD_WIDTH - Constants.SHEEP_WIDTH), random.randint(0, Constants.WORLD_HEIGHT - Constants.SHEEP_HEIGHT))
    sheep = Sheep(pos, Constants.SHEEP_MOVE_SPEED, sheepSurface)
    sheeps.append(sheep)

# Run in a loop
while not done:

    # Check for game exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set toggles
        elif event.type == pygame.KEYDOWN:

            # UI toggles
            if event.key == pygame.K_1:
                Constants.VELOCITY_LINES = not Constants.VELOCITY_LINES
            elif event.key == pygame.K_2:
                Constants.ATTACK_LINES = not Constants.ATTACK_LINES
            elif event.key == pygame.K_3:
                Constants.BOUNDARY_FORCE_LINES = not Constants.BOUNDARY_FORCE_LINES
            elif event.key == pygame.K_4:
                Constants.NEIGHBOR_LINES = not Constants.NEIGHBOR_LINES
            elif event.key == pygame.K_5:
                Constants.BOUNDING_BOXES = not Constants.BOUNDING_BOXES

            # Force toggles
            elif event.key == pygame.K_6:
                Constants.DOG_FORCES = not Constants.DOG_FORCES
            elif event.key == pygame.K_7:
                Constants.ALIGNMENT_FORCES = not Constants.ALIGNMENT_FORCES
            elif event.key == pygame.K_8:
                Constants.SEPARATION_FORCES = not Constants.SEPARATION_FORCES
            elif event.key == pygame.K_9:
                Constants.COHESION_FORCES = not Constants.COHESION_FORCES
            elif event.key == pygame.K_0:
                Constants.BOUNDARY_FORCES = not Constants.BOUNDARY_FORCES

    # Update agents
    dog.update()
    for sheep in sheeps:
        sheep.update(dog, sheeps)
    # Draw background
    screen.fill(Constants.BACKGROUND_COLOR)

    # Draw agents
    dog.draw(screen)
    for sheep in sheeps:
        sheep.draw(screen, dog)

    # Flip buffer
    pygame.display.flip()

    # Tick clock at 60FPS
    clock.tick(Constants.FRAME_RATE)
