import pygame

from Node import *
from Edge import *
from Vector import *
from enum import Enum

# Define the possible search types that are supported by this graph
class SearchType(Enum):
	BREADTH = 1
	DJIKSTRA = 2
	A_STAR = 3
	BEST = 4

class Graph(object):
	"""Generic Graph class that can be used with any type of Nodes and Edges"""

	# Initialize the graph as empty and default search of breadth-first
	def __init__(self):
		self.nodes = []
		self.path = []
		self.toVisit = []
		self.searchType = SearchType.BREADTH
		return

	# Add a node to the graph (neighbors are accessed through the nodes)
	def addNode(self, node):
		self.nodes.append(node)
		return

	# Initialize the search - this resets the graph
	def setupSearch(self, start, end, searchType):
		self.start = start
		self.end = end
		self.searchType = searchType

		# Reset the graph for the search
		self.path = []
		self.toVisit = []
		for node in self.nodes:
			node.setVisited(False)

		# Identify the starting node as visited and add
		# to the toVisit queue
		self.start.setVisited(True)
		self.toVisit.append(self.start)

		return

	# Perform a Breadth-first search, one step at a time
	def RunBreadthFirstStep(self):

		# If toVisit queue is not empty
		if len(self.toVisit) > 0:

			# Look at first node in the queue
			testNode = self.toVisit.pop(0)
			testNode.setVisited(True)
			print("Testing " + str(testNode.row) + "," + str(testNode.col))

			# Add neighbor nodes to to visit queue and set backpaths
			for edge in testNode.neighborEdges:
				neighborNode = edge.n2

				# If neightbor is the end node
				if neighborNode == self.end:

					# Backtrack through backpath until the start,
					# adding each node along the way to the path
					self.path.insert(0, neighborNode)
					while testNode != 0:
						self.path.insert(0, testNode)
						testNode = testNode.backpath
				elif neighborNode.getVisited() == False  and neighborNode not in self.toVisit:
					neighborNode.backpath = testNode
					self.toVisit.append(neighborNode)

		return

	# Perform a Djikstra's search, one step at a time
	def RunDjikstraStep(self):
		# TODO
		return

	# Perform a Best-first search, one step at a time
	def RunBestFirstStep(self):
		# TODO
		return

	# Perform an A-star search, one step at a time
	def RunA_StarStep(self):
		# TODO
		return

	# Call the next step for the current search type
	def update(self):
		if self.searchType == SearchType.BREADTH:
			self.RunBreadthFirstStep()
		elif self.searchType == SearchType.DJIKSTRA:
			self.RunDjikstraStep()
		elif self.searchType == SearchType.BEST:
			self.RunBestFirstStep()
		else: #self.searchType == SearchType.DJIKSTRA:
			self.RunA_StarStep()
		return