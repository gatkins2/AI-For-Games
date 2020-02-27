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
        self.target = player.center.tuple()

        # Calculate current neighbors
        self.neighbors = self.calculateNeighbors(herd)

        # Set velocity
        self.calculateVelocity(player)

        # Move
        super().update()

    # Draw sheep
    def draw(self, screen, player):

        # If near the player, draw attack line
        if Constants.ATTACK_LINES and self.vectToPlayer.length() <= Constants.SHEEP_ATTACK_RANGE:
            pygame.draw.line(screen, Constants.RED, self.center.tuple(), self.target, Constants.LINE_WIDTH)

        # Draw lines to neighbors
        if Constants.NEIGHBOR_LINES:
            for sheep in self.neighbors:
                pygame.draw.line(screen, Constants.BLUE, self.center.tuple(), sheep.center.tuple(), Constants.LINE_WIDTH)

        # Call parent draw
        super().draw(screen)

    # Calculate sheep velocity
    def calculateVelocity(self, player):

        # Get forces
        alignment = cohesion = separation = boundaries = dog = Vector.zero()
        if Constants.ALIGNMENT_FORCES: alignment = self.getAlignmentForce()
        if Constants.COHESION_FORCES: cohesion = self.getCohesionForce()
        if Constants.SEPARATION_FORCES: separation = self.getSeparationForce()
        if Constants.BOUNDARY_FORCES: boundaries = self.getBoundaryForce()
        if Constants.DOG_FORCES: dog = self.getDogForce(player)

        forces = alignment.scale(Constants.ALIGNMENT_WEIGHT) \
                 + cohesion.scale(Constants.COHESION_WEIGHT) \
                 + separation.scale(Constants.SEPARATION_WEIGHT) \
                 + boundaries.scale(Constants.BOUNDARY_WEIGHT) \
                 + dog.scale(Constants.DOG_WEIGHT)

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

    # Calculate sheep's cohesion force
    def getCohesionForce(self):

        # If no neighbors
        if len(self.neighbors) <= 0:
            return self.velocity.normalize()

        # Add neighbor positions
        centerOfMass= self.velocity
        for sheep in self.neighbors:
            centerOfMass += sheep.position

        # Divide by number of neighbors
        centerOfMass.x /= len(self.neighbors)
        centerOfMass.y /= len(self.neighbors)

        # Find direction vector toward center of mass
        velocity = centerOfMass - self.position

        return velocity.normalize()

    # Calculate sheep's separation force
    def getSeparationForce(self):

        # If no neighbors
        if len(self.neighbors) <= 0:
            return self.velocity.normalize()

        # Add difference between neighbor positions
        velocity = self.velocity
        for sheep in self.neighbors:
            velocity += sheep.position - self.position

        # Divide by number of neighbors
        velocity.x /= len(self.neighbors)
        velocity.y /= len(self.neighbors)

        # Negate vector
        velocity = -velocity.normalize()

        return velocity

    # Calculate sheep's boundary force
    def getBoundaryForce(self):

        velocity = Vector.zero()

        # Top/bottom boundary
        if self.center.y - Constants.SHEEP_BOUNDARY_RADIUS <= 0:
            velocity.y = 1
        elif self.center.y + Constants.SHEEP_BOUNDARY_RADIUS >= Constants.WORLD_HEIGHT:
            velocity.y = -1

        # Left/right boundary
        if self.center.x - Constants.SHEEP_BOUNDARY_RADIUS <= 0:
            velocity.x = 1
        elif self.center.x + Constants.SHEEP_BOUNDARY_RADIUS >= Constants.WORLD_WIDTH:
            velocity.x = -1

        return velocity.normalize()

    # Calculate sheep's dog force
    def getDogForce(self, player):
        pass