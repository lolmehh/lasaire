import pygame
from items import ItemStack, create_item

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
