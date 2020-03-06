from Agent import *


# Class to represent the player
class Dog(Agent):

    # Constructor
    def __init__(self, position, speed, angularSpeed, surface):
        self.traversing = False
        super().__init__(position, speed, angularSpeed, surface)

    # Update the dog's path and velocity
    def update(self, graph, sheep):

        # If traversing path
        if self.traversing:

            # Adjust velocity to point to next path node
            

        # Find a new path
        else:
            graph.reset()
            graph.findPath(self.position, sheep.position)

        # Move
        super().update()