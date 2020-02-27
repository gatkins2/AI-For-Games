import pygame, random, math
from Vector import Vector
import Constants


# Class to represent any moving agents
class Agent:

    # Constructor
    def __init__(self, position, width, height, speed, surface):
        self.position = position
        self.width = width
        self.height = height
        self.speed = speed
        self.velocity = Vector(0, -1)
        self.lookDirection = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))
        self.startSurface = surface
        self.surface = surface
        self.rect = surface.get_bounding_rect()
        self.center = Vector(position.x + (surface.get_width() / 2), position.y + (surface.get_height() / 2))

    # Print
    def __str__(self):
        printStr = str(type(self)) + " width = " + str(self.width) + "\n"
        printStr = str(type(self)) + " height = " + str(self.height) + "\n"
        printStr += str(type(self)) + " position = " + str(self.position) + "\n"
        printStr += str(type(self)) + " velocity = " + str(self.velocity) + "\n"
        printStr += str(type(self)) + " center = " + str(self.center) + "\n"
        return printStr

    # Draws the agent to the screen
    def draw(self, screen):

        # Blit the agent
        screen.blit(self.surface, [self.position.x, self.position.y])

        # Draw bounding box
        if Constants.BOUNDING_BOXES:
            pygame.draw.rect(screen, Constants.BLACK, self.rect, 2)

        # Draw velocity line
        if Constants.SHEEP_VELOCITY_LINES:
            endX = self.center.x + (self.velocity.normalize().x * max(self.height, self.width))
            endY = self.center.y + (self.velocity.normalize().y * max(self.height, self.width))
            pygame.draw.line(screen, Constants.BLUE, self.center.tuple(), (endX, endY), 3)

    # Update the agent
    def update(self):

        # Update position from velocity
        self.position += self.velocity.scale(self.speed)

        # Clamp position
        self.clampPosition()

        # Update surface
        self.lookDirection = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))
        self.surface = pygame.transform.rotate(self.startSurface, self.lookDirection - 90)

        # Update rect
        self.rect = self.surface.get_bounding_rect().move(self.position.x, self.position.y)

        # Update center
        self.center = Vector(self.position.x + (self.surface.get_width() / 2),
                             self.position.y + (self.surface.get_height() / 2))

    # Clamp position in world bounds
    def clampPosition(self):

        # clamp X
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x + self.surface.get_width() > Constants.WORLD_WIDTH:
            self.position.x = Constants.WORLD_WIDTH - self.surface.get_width()

        # Clamp Y
        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y + self.surface.get_height() > Constants.WORLD_HEIGHT:
            self.position.y = Constants.WORLD_HEIGHT - self.surface.get_height()

    # Check collision with another agent
    def collision(self, other):

        if self.rect.colliderect(other.rect):
            return True
        else:
            return False
