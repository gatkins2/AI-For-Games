import pygame
import random
import cmath

from Vector import *
from GridNode import *
from GridEdge import *
from Graph import *


# Functions
def Distance(n1, n2):
    return (n1.position - n2.position).length()


# Draw the graph by rendering the nodes and edges
def DrawGraph(screen, nodes):
    for nodeRow in nodes:
        for node in nodeRow:
            node.draw(screen)
            for edge in node.neighborEdges:
                edge.draw(screen)
    return


# Constants
screenWidth = 800
screenHeight = 600
gridCellSize = 25
numberRows = int(screenWidth / gridCellSize)
numberCols = int(screenHeight / gridCellSize)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CORNFLOWER_BLUE = (100, 149, 237)
CYAN = (0, 255, 255)

# Init the game
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False
angle = 1
clock = pygame.time.Clock()

# Create the list of gridCells (nodes)
nodes = []
breadthGraph = Graph()
for i in range(0, numberRows):
    nodeRow = []
    for j in range(0, numberCols):
        node = GridNode(CYAN, BLACK, Vector(i * gridCellSize, j * gridCellSize), gridCellSize, i, j)
        nodeRow.append(node)
        breadthGraph.addNode(node)
    nodes.append(nodeRow)

# Create the edges between neighbors
for i in range(0, numberRows):
    for j in range(0, numberCols):
        for m in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                if m >= 0 and n >= 0 and m < numberRows and n < numberCols \
                        and (i != m or j != n):
                    edge = GridEdge(nodes[i][j], nodes[m][n],
                                    Distance(nodes[i][j], nodes[m][n]), RED, WHITE)
                    nodes[i][j].addNeighborEdge(edge)

# Assume the system starts in non-searching mode
isSearching = False

# Game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the background
    screen.fill(CORNFLOWER_BLUE)

    # Get the keyboard to initiate a breadth-first search
    if isSearching == False and pygame.key.get_pressed()[pygame.K_b] != 0:
        for nodeRow in nodes:
            for node in nodeRow:
                node.reset()

        # Select 2 random points as start and goal
        start = nodes[random.randint(0, numberRows - 1)][random.randint(0, numberCols - 1)]
        end = nodes[random.randint(0, numberRows - 1)][random.randint(0, numberCols - 1)]
        while start is end:
            end = nodes[random.randint(0, numberRows - 1)][random.randint(0, numberCols - 1)]

        # Initialize the search
        breadthGraph.setupSearch(start, end, SearchType.BREADTH)
        isSearching = True

        # Set colors for start and goal nodes
        start.color = GREEN
        end.color = RED
    else:
        # If we have not yet found a path, take another step
        if len(breadthGraph.path) == 0:
            breadthGraph.update()
        # If we have found a path, render it as black
        else:
            for node in breadthGraph.path:
                node.color = BLACK
                isSearching = False

    DrawGraph(screen, nodes)

    pygame.display.flip()
    clock.tick(60)
