from Agent import *


# Class to represent an enemy
class Enemy(Agent):

    # Update the enemy
    def update(self, player):

        # Calculate the distance to the player
        distToPlayer = player.center - self.center

        # Set velocity towards player if in attack range
        if distToPlayer.length() < ENEMY_ATTACK_RANGE:
            self.velocity = distToPlayer.normalize()
        else:
            self.velocity = Vector.zero()

        # Move
        super().update()