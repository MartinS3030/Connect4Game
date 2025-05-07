# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Board settings
ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4

# Piece constants
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

# UI settings
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# Model settings
MODEL_FILE = 'connect4_model.keras'