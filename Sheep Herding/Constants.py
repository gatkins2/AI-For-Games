# Game config
FRAME_RATE = 60
WORLD_WIDTH = 1024
WORLD_HEIGHT = 768
BACKGROUND_COLOR = (100, 149, 237)

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Dog data
DOG_MOVE_SPEED = 5.5
DOG_WIDTH = 16
DOG_HEIGHT = 32

# Sheep data
SHEEP_ATTACK_RANGE = 200
SHEEP_START_X = 100
SHEEP_START_Y = 100
SHEEP_MOVE_SPEED = 5
SHEEP_WIDTH = 16
SHEEP_HEIGHT = 32
SHEEP_NEIGHBOR_RADIUS = 50
SHEEP_BOUNDARY_RADIUS = 50

# UI Toggles
VELOCITY_LINES = True
BOUNDING_BOXES = True
ATTACK_LINES = True
BOUNDARY_FORCE_LINES = True
NEIGHBOR_LINES = True
LINE_WIDTH = 2

# Force Toggles
DOG_FORCES = False
ALIGNMENT_FORCES = False
SEPARATION_FORCES = False
COHESION_FORCES = False
BOUNDARY_FORCES = False

# Force Weights
DOG_WEIGHT = 0.2
ALIGNMENT_WEIGHT = 0.3
SEPARATION_WEIGHT = 0.325
COHESION_WEIGHT = 0.3
BOUNDARY_WEIGHT = 0.2