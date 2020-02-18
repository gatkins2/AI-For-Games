import pygame
from Vector import Vector


# Class to represent an enemy
class Player:

    # Constructor
    def __init__(self, position, velocity, size):
        self.position = position
        self.velocity = velocity
        self.size = size
        self.moveSpeed = 5

    # Draws the enemy to the screen
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.position.x, self.position.y, self.size, self.size))
        startX = self.position.x + (self.size / 2)
        startY = self.position.y + (self.size / 2)
        endX = startX + (self.velocity.normalize().x * self.size)
        endY = startY + (self.velocity.normalize().y * self.size)
        pygame.draw.line(screen, (255, 255, 255), (startX, startY), (endX, endY), 3)

    # Updates the enemy's position based on its velocity
    def update(self):

        # Get key input
        pressed = pygame.key.get_pressed()

        # Check for movement
        self.velocity = Vector(0, 0)
        if pressed[pygame.K_w]: self.velocity.y -= 1
        if pressed[pygame.K_s]: self.velocity.y += 1
        if pressed[pygame.K_a]: self.velocity.x -= 1
        if pressed[pygame.K_d]: self.velocity.x += 1

        # Update position from velocity
        self.position = self.position + self.velocity.normalize().scale(self.moveSpeed)