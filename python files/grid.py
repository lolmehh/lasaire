import pygame

TILE_SIZE = 40      # pixels per tile
GRID_WIDTH = 30     # tiles horizontally
GRID_HEIGHT = 20    # tiles vertically
GRID_COLOR = (60, 60, 60)


class Grid:
    def __init__(self, tile_size=TILE_SIZE):
        self.tile_size = tile_size

    def draw(self, screen, camera):
        """
        Draw the grid in world space, taking the camera offset into account.
        This way, when the player moves (and the camera follows),
        the grid will scroll instead of staying glued to the screen.
        """
        screen_w, screen_h = screen.get_size()

        # How far we are scrolled in world coordinates
        offset_x = camera.offset_x
        offset_y = camera.offset_y

        # Start drawing lines a bit *before* the visible area, so we cover the whole screen.
        start_x = - (offset_x % self.tile_size)
        start_y = - (offset_y % self.tile_size)

        # Vertical lines
        x = start_x
        while x < screen_w:
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, screen_h))
            x += self.tile_size

        # Horizontal lines
        y = start_y
        while y < screen_h:
            pygame.draw.line(screen, GRID_COLOR, (0, y), (screen_w, y))
            y += self.tile_size
