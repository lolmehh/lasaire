import pygame

TILE_SIZE = 40      # pixels per tile
GRID_WIDTH = 30     # tiles horizontally
GRID_HEIGHT = 20    # tiles vertically
GRID_COLOR = (60, 60, 60)

class Grid:
    def __init__(self, tile_size=TILE_SIZE):
        self.tile_size = tile_size

    def draw(self, screen):
        width, height = screen.get_size()

        # Vertical lines
        for x in range(0, width, self.tile_size):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, height))

        # Horizontal lines
        for y in range(0, height, self.tile_size):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (width, y))


# OPTIONAL: simple test object
class Player:
    def __init__(self, grid_x=5, grid_y=5):
        self.x = grid_x
        self.y = grid_y
        self.color = (255, 0, 0)
        self.size = TILE_SIZE

    def draw(self, screen):
        rect = pygame.Rect(
            self.x * TILE_SIZE,
            self.y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )
        pygame.draw.rect(screen, self.color, rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy