from Agent import *


# Class to represent a sheep
class Sheep(Agent):

    # Initiate sheep to be following and inactive
    def __init__(self, position, speed, surface):
        super().__init__(position, speed, surface)
        self.vectToPlayer = Vector.zero()
        self.target = (0, 0)
        self.neighbors = []

    # Update the sheep
    def update(self, player, herd):

        # Calculate the distance to the player
        self.vectToPlayer = player.center - self.center

        # Calculate current neighbors
        self.neighbors = self.calculateNeighbors(herd)

        # Set velocity
        self.calculateVelocity(player)

        # Move
        super().update()

    # Draw sheep
    def draw(self, screen, player):
        # If following the player, draw attack line
        if self.vectToPlayer.length() <= Constants.SHEEP_ATTACK_RANGE:
            pygame.draw.line(screen, Constants.RED, self.center.tuple(), self.target, 3)

        # Call parent draw
        super().draw(screen)

    # Calculate sheep velocity
    def calculateVelocity(self, player):

        # Get forces
        alignment = self.getAlignmentForce()

        forces = alignment.scale(Constants.CURRENT_ALIGNMENT_WEIGHT)

        if forces.length() != 0:
            self.velocity = forces.normalize()


    # Find sheep that are neighbors to this one
    def calculateNeighbors(self, herd):
        neighbors = []
        for sheep in herd:
            if sheep is not self and (sheep.center - self.center).length() < Constants.SHEEP_NEIGHBOR_RADIUS:
                neighbors.append(sheep)
        return neighbors

    # Celculate sheep's aligment force
    def getAlignmentForce(self):

        # If no neighbors
        if len(self.neighbors) <= 0:
            return self.velocity.normalize()

        # Add neighbor velocities
        velocity = self.velocity
        for sheep in self.neighbors:
            velocity += sheep.velocity

        # Divide by number of neighbors
        velocity.x /= len(self.neighbors)
        velocity.y /= len(self.neighbors)

        return velocity.normalize()