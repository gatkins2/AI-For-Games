from Agent import *


# Class to represent an enemy
class Enemy(Agent):

    # Initiate enemy to be following and inactive
    def __init__(self, position, size, speed, color):
        super().__init__(position, size, speed, color)
        self.vectToPlayer = 0
        self.following = True
        self.active = False
        self.canCollide = True
        self.collideTimer = 0
        self.flashTimer = 0

    # Update the enemy
    def update(self, player):

        # Check collide timer
        if self.collideTimer > 0:
            self.collideTimer -= 1
            if self.flashTimer <= 0:
                self.flashTimer = ENEMY_FLASH_TIMEOUT
            else:
                self.flashTimer -= 1
        else:
            self.canCollide = True

        # Switch following / fleeing on collision with player
        if self.canCollide:
            if self.collision(player):
                self.canCollide = False
                self.collideTimer = ENEMY_COLLIDE_TIMEOUT
                self.following = not self.following

        # Calculate the distance to the player
        self.vectToPlayer = player.center - self.center

        # Set activity
        if self.vectToPlayer.length() < ENEMY_ATTACK_RANGE:
            self.active = True
        else:
            self.active = False

        # Set velocity
        self.calculateVelocity()
        self.velocity = self.velocity.normalize()

        # Move
        super().update()

    # Calculate enemy velocity
    def calculateVelocity(self):
        if self.active:
            if self.following:
                self.velocity = self.vectToPlayer.normalize()
            else:
                self.velocity = -self.vectToPlayer.normalize()
        else:
            self.velocity = Vector.zero()

    # Draw enemy target line
    def draw(self, screen, player):

        # Flash white if can't collide
        if not self.canCollide and self.flashTimer <= ENEMY_FLASH_TIMEOUT / 2:
            self.color = WHITE
        else:
            self.color = ENEMY_COLOR

        # If following the player, draw attack line
        if self.following and self.active:
            self.drawAttackLine(screen, player)

        # Call parent draw
        super().draw(screen)

    # Draw the line where the enemy is attacking
    def drawAttackLine(self, screen, player):
        pygame.draw.line(screen, RED, self.center.tuple(), player.center.tuple(), 3)