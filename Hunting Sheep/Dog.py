from Agent import *


# Class to represent the player
class Dog(Agent):

    # Constructor
    def __init__(self, position, speed, angularSpeed, surface):
        super().__init__(position, speed, angularSpeed, surface)

    # Update the dog's path and velocity
    def update(self, graph, sheep):

        # If back path exists
        if len(graph.backPath) > 0:

            # If on the first node in back path
            if graph.getNodeFromPoint(self.position) == graph.backPath[0]:

                # If not at the end of the path
                if len(graph.backPath) > 1:

                    # Set velocity to point toward next path node
                    self.velocity = (graph.backPath[1].center - self.position).normalize()

                # Pop node off
                graph.backPath.pop(0)

            # If not on the first node
            else:

                # Set velocity to point toward first node
                self.velocity = (graph.backPath[0].center - self.position).normalize()

        # Find a new path
        else:
            graph.findPath(self.position, sheep.position)

        # Move
        super().update()