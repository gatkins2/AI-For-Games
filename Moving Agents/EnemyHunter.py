from Enemy import *


class EnemyHunter(Enemy):

    # Calculate hunter velocity form player's anticipated position
    def calculateVelocity(self, player):
        if self.active:
            distToPlayer = (player.center - self.center).length()
            if self.following:
                timeToReach = distToPlayer / self.speed
                playerPosAtTime = player.center + player.velocity.scale(player.speed * timeToReach)
                self.target = playerPosAtTime.tuple()
                self.velocity = (playerPosAtTime - self.center).normalize()
            else:
                timeToReach = distToPlayer / player.speed
                playerPosAtTime = player.center + player.velocity.scale(player.speed * timeToReach)
                self.velocity = -(playerPosAtTime - self.center).normalize()
        else:
            self.velocity = Vector.zero()