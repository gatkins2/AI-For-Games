from Agent import *


# Class to represent the player
class Dog(Agent):

    # Updates the player's position based on its velocity
    def update(self):

        # Get key input
        pressed = pygame.key.get_pressed()

        # Check for movement
        if pressed[pygame.K_w]: self.velocity.y -= 1
        if pressed[pygame.K_s]: self.velocity.y += 1
        if pressed[pygame.K_a]: self.velocity.x -= 1
        if pressed[pygame.K_d]: self.velocity.x += 1
        self.velocity = self.velocity.normalize()

        # Move
        super().update()