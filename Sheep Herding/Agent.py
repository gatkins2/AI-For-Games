import pygame
from Vector import Vector
from Constants import *


# Class to represent any moving agents
class Agent:

    # Constructor
    def __init__(self, position, size, speed, surface):
        self.position = position
        self.size = size
        self.speed = speed
        self.velocity = Vector.zero()
        self.center = Vector(position.x + (size / 2), position.y + (size / 2))
        self.surface = surface
        self.rect = pygame.Rect(position.x, position.y, size, size)

    # Print
    def __str__(self):
        printStr = str(type(self)) + " size = " + str(self.size) + "\n"
        printStr += str(type(self)) + " position = " + str(self.position) + "\n"
        printStr += str(type(self)) + " velocity = " + str(self.velocity) + "\n"
        printStr += str(type(self)) + " center = " + str(self.center) + "\n"
        return printStr

    # Draws the agent to the screen
    def draw(self, screen):
        screen.blit(self.surface, [self.position.x, self.position.y])
        endX = self.center.x + (self.velocity.normalize().x * self.size)
        endY = self.center.y + (self.velocity.normalize().y * self.size)
        pygame.draw.line(screen, BLUE, self.center.tuple(), (endX, endY), 3)

    # Update the agent
    def update(self):

        # Update position from velocity
        self.position = self.position + self.velocity.scale(self.speed)

        # Clamp position
        self.clampPosition()

        # Update center
        self.center = Vector(self.position.x + (self.size / 2), self.position.y + (self.size / 2))

        # Update rect
        self.rect = pygame.Rect(self.position.x, self.position.y, self.size, self.size)

    # Clamp position in world bounds
    def clampPosition(self):

        # clamp X
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x + self.size > WORLD_WIDTH:
            self.position.x = WORLD_WIDTH - self.size

        # Clamp Y
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y + self.size > WORLD_HEIGHT:
            self.position.y = WORLD_HEIGHT - self.size

    # Check collision with another agent
    def collision(self, other):
        if self.rect.colliderect(other.rect):
            return True
        else:
            return False
