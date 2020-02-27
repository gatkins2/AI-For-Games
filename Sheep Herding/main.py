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
pos = Vector(Constants.DOG_START_X, Constants.DOG_START_Y)
dogSurface = pygame.image.load('collie.png')
dog = Dog(pos, Constants.DOG_MOVE_SPEED, dogSurface)

# Sheep data
sheeps = []
sheepSurface = pygame.image.load('sheep.png')
for i in range(10):
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
                Constants.DOG_FORCE_LINES = not Constants.DOG_FORCE_LINES
            elif event.key == pygame.K_3:
                Constants.BOUNDARY_FORCE_LINES = not Constants.BOUNDARY_FORCE_LINES
            elif event.key == pygame.K_4:
                Constants.NEIGHBOR_FORCE_LINES = not Constants.NEIGHBOR_FORCE_LINES
            elif event.key == pygame.K_5:
                Constants.BOUNDING_BOXES = not Constants.BOUNDING_BOXES

            # Force toggles
            elif event.key == pygame.K_6:
                Constants.DOG_FORCES = not Constants.DOG_FORCES
                if Constants.DOG_FORCES:
                    Constants.CURRENT_DOG_WEIGHT = Constants.DEFAULT_DOG_WEIGHT
                else:
                    Constants.CURRENT_DOG_WEIGHT = 0
            elif event.key == pygame.K_7:
                Constants.ALIGNMENT_FORCES = not Constants.ALIGNMENT_FORCES
                if Constants.ALIGNMENT_FORCES:
                    Constants.CURRENT_ALIGNMENT_WEIGHT = Constants.DEFAULT_ALIGNMENT_WEIGHT
                else:
                    Constants.CURRENT_ALIGNMENT_WEIGHT = 0
            elif event.key == pygame.K_8:
                Constants.SEPARATION_FORCES = not Constants.SEPARATION_FORCES
                if Constants.SEPARATION_FORCES:
                    Constants.CURRENT_SEPARATION_WEIGHT = Constants.DEFAULT_SEPARATION_WEIGHT
                else:
                    Constants.CURRENT_SEPARATION_WEIGHT = 0
            elif event.key == pygame.K_9:
                Constants.COHESION_FORCES = not Constants.COHESION_FORCES
                if Constants.COHESION_FORCES:
                    Constants.CURRENT_COHESION_WEIGHT = Constants.DEFAULT_COHESION_WEIGHT
                else:
                    Constants.CURRENT_COHESION_WEIGHT = 0
            elif event.key == pygame.K_0:
                Constants.BOUNDARY_FORCES = not Constants.BOUNDARY_FORCES
                if Constants.BOUNDARY_FORCES:
                    Constants.CURRENT_BOUNDARY_WEIGHT = Constants.DEFAULT_BOUNDARY_WEIGHT
                else:
                    Constants.CURRENT_BOUNDARY_WEIGHT = 0


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
