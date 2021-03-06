class Node(object):
	"""Node class works with the Graph class to create a generic node"""

	# Initialize the node with no neighbors
	def __init__(self):
		self.neighborEdges = []
		self.isVisited = False
		self.backpath = 0
		self.distance = 0
		return

	# Add a neighborEdge to the node
	def addNeighborEdge(self, edge):
		self.neighborEdges.append(edge)
		return		

	# Set the visited status
	def setVisited(self, isVisited):
		self.isVisited = isVisited
		return

	# Get the visited status
	def getVisited(self):
		return self.isVisited

	# Set the node's distance from the start
	def setDistance(self, distance):
		self.distance = distance

	# Get the node's distance from the start
	def getDistance(self):
		return self.distance

	# Print the node's data for debugging
	def print(self):
		print("isVisited: " + str(self.isVisited))
		print("edges: " + str(len(self.neighborEdges)))
		return
