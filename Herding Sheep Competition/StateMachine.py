from Constants import *
from pygame import *
from random import *
from Vector import *
from Agent import *
from Sheep import *
from Dog import *
from Graph import *
from Node import *
from GameState import *


class StateMachine:
	""" Machine that manages the set of states and their transitions """

	def __init__(self, startState):
		""" Initialize the state machine and its start state"""
		self.__currentState = startState
		self.__currentState.enter(GameState())

	def getCurrentState(self):
		""" Get the current state """
		return self.__currentState

	def update(self, gameState):
		""" Run the update on the current state and determine if we should transition """
		nextState = self.__currentState.update(gameState)

		# If the nextState that is returned by current state's update is not the same
		# state, then transition to that new state
		if nextState is not None and type(nextState) != type(self.__currentState):
			self.transitionTo(nextState, gameState)

	def transitionTo(self, nextState, gameState):
		""" Transition to the next state """
		self.__currentState.exit(gameState)
		self.__currentState = nextState
		self.__currentState.enter(gameState)

	def draw(self, screen):
		""" Draw any debugging information associated with the states """
		self.__currentState.draw(screen)


class State:
	def enter(self, gameState):
		""" Enter this state, perform any setup required """
		print("Entering " + self.__class__.__name__)

	def exit(self, gameState):
		""" Exit this state, perform any shutdown or cleanup required """
		print("Exiting " + self.__class__.__name__)

	def update(self, gameState):
		""" Update this state, before leaving update, return the next state """
		print("Updating " + self.__class__.__name__)

	def draw(self, screen):
		""" Draw any debugging info required by this state """
		pass


class FindSheep(State):
	""" Pick the closest sheep to target """

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()

		# Pick the closest sheep
		herd = gameState.getHerd()
		herd.sort(key=lambda sheep: (sheep.center - dog.center).length())
		i = 0
		closestSheep = herd[i]
		while not gameState.getGraph().getNodeFromPoint(closestSheep.center).isWalkable:
			i += 1
			closestSheep = herd[i]
		dog.setTargetSheep(closestSheep)

		return CheckSheepZone()


class CheckSheepZone(State):
	""" Check which zone the sheep is in and set a path accordingly"""

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		sheep = dog.getTargetSheep()
		targetPoint = Vector(0, 0)
		entranceCenter = Vector(gameState.getPenBounds()[0].centerx, gameState.getPenBounds()[0].centery)
		worldBoundsRect = pygame.Rect(0, 0, gameState.getWorldBounds().x, gameState.getWorldBounds().y)

		# If sheep is above entrance
		if sheep.center.y < entranceCenter.y:
			# Move sheep toward entrance
			targetPoint = sheep.center + (sheep.center - entranceCenter).normalize().scale(
				SHEEP_MIN_FLEE_DIST + GRID_SIZE)

		# If sheep is below and to the side of the entrance
		elif sheep.center.y >= entranceCenter.y - (4 * GRID_SIZE) and \
				not gameState.getPenBounds()[0].collidepoint(sheep.center.x, entranceCenter.y):
			# Move sheep up
			targetPoint = sheep.center + Vector(0, 1).scale(SHEEP_MIN_FLEE_DIST + GRID_SIZE)

		# If sheep is directly below entrance
		else:
			# If sheep is below and to the right
			if sheep.center.x > gameState.getPenBounds()[0].centerx:
				# Move sheep right
				targetPoint = sheep.center + Vector(-1, 0).scale(SHEEP_MIN_FLEE_DIST + GRID_SIZE)

			# If sheep is below and to the left
			else:
				# Move sheep left
				targetPoint = sheep.center + Vector(1, 0).scale(SHEEP_MIN_FLEE_DIST + GRID_SIZE)

		# Clamp target point in bounds and avoid obstacles
		targetToSheepDirection = (sheep.center - targetPoint).normalize()
		while not worldBoundsRect.collidepoint(targetPoint.x, targetPoint.y) or \
				not gameState.getGraph().getNodeFromPoint(targetPoint).isWalkable:
			targetPoint += targetToSheepDirection.scale(GRID_SIZE)

		# If dog to sheep vector is close to target to sheep vector
		dogToSheepDirection = (sheep.center - dog.center).normalize()
		if math.degrees(math.acos(targetToSheepDirection.dot(dogToSheepDirection) / (targetToSheepDirection.length() * dogToSheepDirection.length()))) <= 20:
			# Begin chasing sheep
			return ChaseSheep()

		# Set dog path
		# If target and dog are not in sheep radius
		if (targetPoint - sheep.center).length() > SHEEP_MIN_FLEE_DIST and (
				dog.center - sheep.center).length() > SHEEP_MIN_FLEE_DIST:
			# Find a path around the sheep's radius
			dog.calculatePathToNewTarget(targetPoint, sheep)
		else:
			# Find a normal path
			dog.calculatePathToNewTarget(targetPoint)
		dog.sheepLastLocation = sheep.center

		# Start moving to target point
		return MoveToSheepRadius()


class MoveToSheepRadius(State):
	""" Move the dog to the target on the sheep's radius """

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		sheep = dog.getTargetSheep()

		# If sheep has moved
		if dog.sheepLastLocation != sheep.center:
			# Restart path
			return CheckSheepZone()

		# If dog has reached the sheep's radius
		elif not dog.isFollowingPath:
			# Begin chasing sheep
			return ChaseSheep()

		# Continue in state
		return self


class ChaseSheep(State):
	""" Move the dog towards the sheep """

	def enter(self, gameState):
		dog = gameState.getDog()
		dog.calculatePathToNewTarget(dog.getTargetSheep().center)

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		sheep = dog.getTargetSheep()

		# If sheep is successfully herded
		if sheep not in gameState.getHerd():
			# Target next sheep
			return FindSheep()

		# If dog is done pathing
		if not dog.isFollowingPath:
			# Check sheep zone
			return CheckSheepZone()

		# Continue in state
		return self
