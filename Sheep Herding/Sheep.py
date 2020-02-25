from Agent import *


# Class to represent a sheep
class Sheep(Agent):

    # Initiate sheep to be following and inactive
    def __init__(self, position, size, speed, color):
        super().__init__(position, size, speed, color)
        self.vectToPlayer = Vector.zero()
        self.target = (0, 0)
        self.active = False

    # Update the sheep
    def update(self, player):

        # Calculate the distance to the player
        self.vectToPlayer = player.center - self.center

        # Set activity
        if self.vectToPlayer.length() < ENEMY_ATTACK_RANGE:
            self.active = True
        else:
            self.active = False

        # Set velocity
        self.calculateVelocity(player)
        self.velocity = self.velocity.normalize()

        # Move
        super().update()

    # Calculate sheep velocity
    def calculateVelocity(self, player):
        self.target = player.center.tuple()
        if self.active:
            self.velocity = -self.vectToPlayer.normalize()
        else:
            self.velocity = Vector.zero()

    # Draw sheep
    def draw(self, screen, player):

        # If following the player, draw attack line
        if self.active:
            pygame.draw.line(screen, RED, self.center.tuple(), self.target, 3)

        # Call parent draw
        super().draw(screen)
