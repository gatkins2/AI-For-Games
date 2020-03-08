from Agent import *


# Class to represent a sheep
class Sheep(Agent):

    # Initiate sheep to be following and inactive
    def __init__(self, position, speed, angularSpeed, surface):
        super().__init__(position, speed, angularSpeed, surface)
        self.vectToPlayer = Vector.zero()
        self.neighbors = []
        self.nearestBoundary = None
        self.obstaclesInRange = []

    # Update the sheep
    def update(self, dog, herd, obstacles):

        # Calculate the distance to the dog
        self.vectToPlayer = dog.center - self.center
        self.target = dog.center.tuple()

        # Calculate current neighbors
        self.neighbors = self.calculateNeighbors(herd)

        # Set velocity
        self.calculateVelocity(dog, obstacles)

        # Move
        super().update()

    # Draw sheep
    def draw(self, screen, dog):

        # If near the dog, draw attack line
        if Constants.ATTACK_LINES and self.vectToPlayer.length() <= Constants.SHEEP_ATTACK_RANGE:
            pygame.draw.line(screen, Constants.RED, self.center.tuple(), self.target, Constants.LINE_WIDTH)

        # Draw lines to neighbors
        if Constants.SHEEP_NEIGHBOR_LINES:
            for sheep in self.neighbors:
                pygame.draw.line(screen, Constants.BLUE, self.center.tuple(), sheep.center.tuple(), Constants.LINE_WIDTH)

        # Draw line to nearest boundary
        if Constants.BOUNDARY_FORCE_LINES:
            if self.nearestBoundary is not None:
                pygame.draw.line(screen, Constants.MAGENTA, self.center.tuple(), self.nearestBoundary.tuple(), Constants.LINE_WIDTH)

        # Draw lines to obstacles
        if Constants.OBSTACLE_FORCES:
            for obstacle in self.obstaclesInRange:
                pygame.draw.line(screen, Constants.WHITE, self.center.tuple(), obstacle.center.tuple(), Constants.LINE_WIDTH)

        # Call parent draw
        super().draw(screen)

    # Calculate sheep velocity
    def calculateVelocity(self, dog, obstacles):

        # Get forces
        alignment = cohesion = separation = boundaries = dogForce = Vector.zero()
        if Constants.ALIGNMENT_FORCES: alignment = self.getAlignmentForce()
        if Constants.COHESION_FORCES: cohesion = self.getCohesionForce()
        if Constants.SEPARATION_FORCES: separation = self.getSeparationForce()
        if Constants.BOUNDARY_FORCES: boundaries = self.getBoundaryForce()
        else: self.nearestBoundary = None
        if Constants.DOG_FORCES: dogForce = self.getDogForce(dog)
        if Constants.OBSTACLE_FORCES: obstacles = self.getObstacleForce(obstacles)
        else: self.obstaclesInRange = []

        # Sum forces
        forces = alignment.scale(Constants.ALIGNMENT_WEIGHT) \
                 + cohesion.scale(Constants.COHESION_WEIGHT) \
                 + separation.scale(Constants.SEPARATION_WEIGHT) \
                 + boundaries.scale(Constants.BOUNDARY_WEIGHT) \
                 + dogForce.scale(Constants.DOG_WEIGHT) \
                 + obstacles.scale(Constants.OBSTACLE_WEIGHT)

        # Normalize and set velocity
        if forces.length() != 0:
            idealVelocity = forces.normalize()
            self.velocity = self.velocity.scale(1 - Constants.SHEEP_ANGULAR_SPEED) + idealVelocity.scale(
                Constants.SHEEP_ANGULAR_SPEED)

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
        nearestBoundVect = None

        # Top/bottom boundary
        if self.center.y - Constants.SHEEP_BOUNDARY_RADIUS <= 0:
            velocity.y = 1
            nearestBoundVect = Vector(0, -self.center.y)
        elif self.center.y + Constants.SHEEP_BOUNDARY_RADIUS >= Constants.WORLD_HEIGHT:
            velocity.y = -1
            nearestBoundVect = Vector(0, self.center.y)

        # Left/right boundary
        if self.center.x - Constants.SHEEP_BOUNDARY_RADIUS <= 0:
            velocity.x = 1
            nearestBoundVect = Vector(-self.center.x, 0)
        elif self.center.x + Constants.SHEEP_BOUNDARY_RADIUS >= Constants.WORLD_WIDTH:
            velocity.x = -1
            nearestBoundVect = Vector(self.center.x, 0)

        # Set nearest boundary point
        if nearestBoundVect is not None:
            self.nearestBoundary = self.center + nearestBoundVect
        else:
            self.nearestBoundary = None

        return velocity.normalize()

    # Calculate sheep's dog force
    def getDogForce(self, dog):

        velocity = Vector.zero()
        if (self.center - dog.center).length() <= Constants.SHEEP_ATTACK_RANGE:
            velocity = -self.vectToPlayer.normalize()

        return velocity

    # Calculate sheep's obstacle force
    def getObstacleForce(self, obstacles):

        velocity = Vector.zero()
        self.obstaclesInRange = []
        for obstacle in obstacles:

            # If obstacle in radius
            if (obstacle.center - self.center).length() < Constants.SHEEP_OBSTACLE_RADIUS:

                # Add to velocity calculation
                velocity += (self.center - obstacle.center)

                # Add to obstacles in range
                self.obstaclesInRange.append(obstacle)

        return velocity.normalize()
