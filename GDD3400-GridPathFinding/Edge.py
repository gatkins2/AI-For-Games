class Edge(object):
	"""Generic Edge to be used with the generic Graph"""

	# Initialize the edge with its nodes and weight
	def __init__(self, n1, n2, weight):
		self.n1 = n1
		self.n2 = n2
		self.weight = weight
		return

	# Get the weight of the edge
	def getWeight(self):
		return self.weight
