import pygame

from pygame import Rect
from Vector import *
from Node import *

class GridNode(Node):
	"""Node in a grid"""

	# Initialize the nodes colors, position, size, and identifiers
	def __init__(self, color, borderColor, position, size, row, col):
		super().__init__()
		self.color = color
		self.originalColor = color
		self.borderColor = borderColor
		self.position = position
		self.size = size
		self.center = Vector(self.position.x + size * 0.5, self.position.y + size * 0.5)
		self.row = row
		self.col = col
		return

	# Reset the node colors to their original colors
	def reset(self):
		self.color = self.originalColor
		return

	# Set the visited status of the node and change its color
	def setVisited(self, isVisited):
		super().setVisited(isVisited)
		if isVisited:
			self.color = (0, 0, 255)
		else:
			self.color = (0, 255, 255)
		return

	# Get the visited status
	def getVisited(self):
		return super().getVisited()

	# Print the node's data for debugging
	def print(self):
		print("Node: [" + str(self.row) + "][" + str(self.col) + "]")
		super().print()
		return

	# Draw the node and its rectangular boundary
	def draw(self, screen):
		# draw the filled rectangle
		pygame.draw.rect(screen, self.color, Rect(self.position.x, self.position.y, 
												  self.size, self.size))
		# draw the boarder for the rectangle
		pygame.draw.rect(screen, self.borderColor, Rect(self.position.x, self.position.y, 
												        self.size, self.size), 1)
		return