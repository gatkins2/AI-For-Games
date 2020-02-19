from Agent import *


# Class to represent an enemy
class Enemy(Agent):

    # Initiate enemy to be following and inactive
    def __init__(self, position, size, speed, color):
        super().__init__(position, size, speed, color)
        self.following = True
        self.active = False

    # Update the enemy
    def update(self, player):

        # Switch following / fleeing on collision with player
        if self.collision(player):
            self.following = not self.following

        # Calculate the distance to the player
        distToPlayer = player.center - self.center

        # Set activity
        if distToPlayer.length() < ENEMY_ATTACK_RANGE:
            self.active = True
        else:
            self.active = False

        # Set velocity
        if self.active:
            if self.following:
                self.velocity = distToPlayer.normalize()
            else:
                self.velocity = -distToPlayer.normalize()
        else:
            self.velocity = Vector.zero()
        self.velocity = self.velocity.normalize()

        # Move
        super().update()

    # Draw enemy target line
    def draw(self, screen, player):

        # If following the player
        if self.following and self.active:
            pygame.draw.line(screen, RED, self.center.tuple(), player.center.tuple(), 3)

        # Call parent draw
        super().draw(screen)
