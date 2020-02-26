import pygame

from Edge import *

class GridEdge(Edge):
	"""Edges for a grid-based world"""

	# Initialize the edges with their nodes, colors, and weight
	def __init__(self, n1, n2, weight, color, backColor):
		super().__init__(n1, n2, weight)
		self.color = color
		self.originalColor = color
		self.backColor = backColor
		return

	# Draw the edge to the screen
	def draw(self, screen):
		pygame.draw.line(screen, self.color, (self.n1.center.x, self.n1.center.y),
				(self.n2.center.x, self.n2.center.y), 1)
