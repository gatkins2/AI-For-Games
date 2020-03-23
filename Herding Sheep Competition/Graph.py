import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []			# Set of nodes
		self.obstacles = []		# Set of obstacles - used for collision detection
		self.toVisit = []		# To visit queue

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i), Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
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
		point.x = max(0, min(point.x, Constants.WORLD_WIDTH - 1))
		point.y = max(0, min(point.y, Constants.WORLD_HEIGHT - 1))

		# Return the node that corresponds to this point
		return self.nodes[int(point.y/Constants.GRID_SIZE)][int(point.x/Constants.GRID_SIZE)]

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
		self.toVisit = []

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not 0:
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

	def findPath_Breadth(self, start, end):
		""" Breadth Search """
		self.reset()

		# TODO: Put your code here

		return []

	def findPath_Dijkstra(self, start, end):
		""" Dijkstra's Search """
		self.reset()

		# TODO: Put your code here

		return []

	def findPath_AStar(self, startPoint, endPoint):
		""" A Star Search """
		self.reset()

		# Set start and end nodes
		start = self.getNodeFromPoint(startPoint)
		end = self.getNodeFromPoint(endPoint)

		# Add start node to toVisit and set to visited
		self.toVisit.append(start)
		start.isVisited = True
		start.isStart = True

		# Set start cost to 0
		start.costFromStart = 0

		# Estimate cost to end from start
		start.costToEnd = (end.center - start.center).length()
		start.cost = start.costFromStart + start.costToEnd

		# If toVisit queue is not empty
		while len(self.toVisit) > 0:

			# Look at first node in the queue
			testNode = self.toVisit.pop(0)
			testNode.isExplored = True

			# If node is the end node
			if testNode == end:
				testNode.isEnd = True

				# Build back path
				return self.buildPath(testNode)

			else:

				# For each neighbor node
				for node in testNode.neighbors:

					# If neighbor not visited
					if not node.isVisited:
						# Set visited
						node.isVisited = True

						# Update cost
						node.costFromStart = testNode.costFromStart + (node.center - testNode.center).length()
						node.costToEnd = (end.center - node.center).length()
						node.cost = node.costFromStart + node.costToEnd

						# Set parent pointer
						node.backNode = testNode

						# Add to queue
						self.toVisit.append(node)

					# If neighbor visited
					else:
						# If new cost is less than old distance
						newCostFromStart = testNode.costFromStart + (node.center - testNode.center).length()
						newCost = newCostFromStart + node.costToEnd
						if newCost < node.cost:
							# Update cost and back node
							node.costFromStart = newCostFromStart
							node.cost = newCost
							node.backNode = testNode

				# Sort the queue
				self.toVisit.sort(key=lambda node: node.cost)

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		#print("BEST_FIRST")

		# TODO: Put your code here

		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)