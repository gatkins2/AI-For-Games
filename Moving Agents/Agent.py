import pygame
from Vector import Vector
from Constants import *


class Agent:

    # Constructor
    def __init__(self, position, size, speed, color):
        self.position = position
        self.size = size
        self.speed = speed
        self.velocity = Vector.zero()
        self.center = Vector(position.x + (size / 2), position.y + (size / 2))
        self.color = color

    # Print
    def __str__(self):
        printStr = str(type(self)) + " size = " + str(self.size) + "\n"
        printStr += str(type(self)) + " position = " + str(self.position) + "\n"
        printStr += str(type(self)) + " velocity = " + str(self.velocity) + "\n"
        printStr += str(type(self)) + " center = " + str(self.center) + "\n"
        return printStr

    # Draws the agent to the screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position.x, self.position.y, self.size, self.size))
        endX = self.center.x + (self.velocity.normalize().x * self.size)
        endY = self.center.y + (self.velocity.normalize().y * self.size)
        pygame.draw.line(screen, BLUE, self.center.tuple(), (endX, endY), 3)

    # Update the agent
    def update(self):
        # Update position from velocity
        self.position = self.position + self.velocity.normalize().scale(self.speed)

        # Update center
        self.center = Vector(self.position.x + (self.size / 2), self.position.y + (self.size / 2))