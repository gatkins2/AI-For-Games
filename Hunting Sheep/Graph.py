import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum


class SearchType(Enum):
	DJIKSTRA = 1
	A_STAR = 2
	BEST_FIRST = 3
	BREADTH_FIRST = 4


class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []  # Set of nodes
		self.obstacles = []  # Set of obstacles - used for collision detection
		self.searchType = SearchType.A_STAR  # Set initial search type to A*
		self.backPath = []  # Initialize empty back path
		self.toVisit = []  # Queue of nodes to visit

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i),
							Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
				row.append(node)
			self.nodes.append(row)

		## Connect to Neighbors
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				# Add the top row of neighbors
				if i - 1 >= 0:
					# Add the upper left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j - 1]]
					# Add the upper center
					self.nodes[i][j].neighbors += [self.nodes[i - 1][j]]
					# Add the upper right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j + 1]]

				# Add the center row of neighbors
				# Add the left center
				if j - 1 >= 0:
					self.nodes[i][j].neighbors += [self.nodes[i][j - 1]]
				# Add the right center
				if j + 1 < self.gridWidth:
					self.nodes[i][j].neighbors += [self.nodes[i][j + 1]]

				# Add the bottom row of neighbors
				if i + 1 < self.gridHeight:
					# Add the lower left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j - 1]]
					# Add the lower center
					self.nodes[i][j].neighbors += [self.nodes[i + 1][j]]
					# Add the lower right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j + 1]]

	def getNodeFromPoint(self, point):
		""" Get the node in the graph that corresponds to a point in the world """
		return self.nodes[int(point.y / Constants.GRID_SIZE)][int(point.x / Constants.GRID_SIZE)]

	def placeObstacle(self, point, color):
		""" Place an obstacle on the graph """
		node = self.getNodeFromPoint(point)

		# If the node is not already an obstacle, make it one
		if node.isWalkable:
			# Indicate that this node cannot be traversed
			node.isWalkable = False

			# Set a specific color for this obstacle
			node.color = color
			for neighbor in node.neighbors:
				neighbor.neighbors.remove(node)
			node.neighbors = []
			self.obstacles += [node]

	def reset(self):
		""" Reset all the nodes for another search """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].reset()
		self.backPath = []
		self.toVisit = []

	def findPath(self, startPoint, endPoint):

		self.reset()

		# Set start and end nodes
		start = self.getNodeFromPoint(startPoint)
		end = self.getNodeFromPoint(endPoint)

		# Add start node to toVisit and set to visited
		self.toVisit.append(start)
		start.isVisited = True
		start.isStart = True

		# Set start cost to 0
		start.cost = 0
		start.costFromStart = 0

		# Estimate cost to end from start (best and A*)
		start.costToEnd = (end.center - start.center).length()

		# Run search
		if self.searchType == SearchType.A_STAR:
			self.findPath_AStar(end)
		elif self.searchType == SearchType.BEST_FIRST:
			self.findPath_BestFirst(end)
		elif self.searchType == SearchType.DJIKSTRA:
			self.findPath_Djikstra(end)
		else:  # search type == BREADTH_FIRST
			self.findPath_Breadth(end)

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not None:
			node.isPath = True
			path = [node] + path
			node = node.backNode

		# If there are nodes in the path, reset the colors of start/end
		if len(path) > 0:
			path[0].isPath = False
			path[0].isStart = True
			path[-1].isPath = False
			path[-1].isEnd = True
		return path

	def findPath_Breadth(self, end):
		""" Breadth Search """

		# If toVisit queue is not empty
		while len(self.toVisit) > 0:

			# Look at first node in the queue
			testNode = self.toVisit.pop(0)
			testNode.isExplored = True

			# Add neighbor nodes to to visit queue and set backpaths
			for node in testNode.neighbors:

				# If neighbor node has not been visited or is not in queue
				if not node.isVisited and node not in self.toVisit:

					# Set back node and add to queue
					node.backNode = testNode
					self.toVisit.append(node)
					node.isVisited = True

				# If neighbor is the end node
				elif node == end:

					node.isEnd = True
					# Set back node and build the backpath
					node.backNode = testNode
					self.backPath = self.buildPath(node)
					return

	def findPath_Djikstra(self, end):
		""" Djikstra's Search """

		# If toVisit queue is not empty
		while len(self.toVisit) > 0:

			# Look at first node in the queue
			testNode = self.toVisit.pop(0)
			testNode.isExplored = True

			# If node is the end node
			if testNode == end:
				testNode.isEnd = True

				# Build back path
				self.backPath = self.buildPath(testNode)

				return

			else:

				# For each neighbor node
				for node in testNode.neighbors:

					# If neighbor not visited
					if not node.isVisited:
						# Set visited
						node.isVisited = True

						# Update cost
						node.costFromStart = testNode.costFromStart + (node.center - testNode.center).length()

						# Set parent pointer
						node.backNode = testNode

						# Add to queue
						self.toVisit.append(node)

					# If neighbor visited
					else:
						# If new cost is less than old distance
						newCost = testNode.costFromStart + (node.center - testNode.center).length()
						if newCost < node.costFromStart:
							# Update cost and back node
							node.costFromStart = newCost
							node.backNode = testNode

				# Sort the queue
				self.toVisit.sort(key=lambda node: node.costFromStart)

	def findPath_AStar(self, end):
		""" A Star Search """
		print("A_STAR")
		self.reset()

		# TODO: Add your A-star code here!

		return []

	def findPath_BestFirst(self, end):
		""" Best First Search """

		# If toVisit queue is not empty
		while len(self.toVisit) > 0:

			# Look at first node in the queue
			testNode = self.toVisit.pop(0)
			testNode.isExplored = True

			# Add neighbor nodes to to visit queue and set backpaths
			for node in testNode.neighbors:

				# If neighbor node has not been visited or is not in queue
				if not node.isVisited and node not in self.toVisit:

					# Set back node and add to queue
					node.backNode = testNode
					self.toVisit.append(node)
					node.isVisited = True

					# Set cost
					node.costToEnd = (end.center - node.center).length()

					# Sort queue
					self.toVisit.sort(key= lambda node:node.costToEnd)

				# If neighbor is the end node
				elif node == end:

					node.isEnd = True
					# Set back node and build the backpath
					node.backNode = testNode
					self.backPath = self.buildPath(node)
					return

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)
