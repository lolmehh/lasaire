import sys
import math
import pygame

# =========================
# GRID (still as background)
# =========================

TILE_SIZE = 40
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


# =========================
# PLAYER WITH SMOOTH MOVEMENT
# =========================

class Player:
    def __init__(self, x, y, speed=250):
        # position in pixels (floats for smooth movement)
        self.x = float(x)
        self.y = float(y)
        self.speed = speed  # pixels per second
        self.size = 30
        self.color = (255, 0, 0)

    def handle_input(self, keys, dt):
        dx = 0
        dy = 0

        # WASD + arrow keys
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        # normalize diagonal movement
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

    def clamp_to_screen(self, screen):
        width, height = screen.get_size()
        half = self.size / 2

        self.x = max(half, min(width - half, self.x))
        self.y = max(half, min(height - half, self.y))

    def draw(self, screen):
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (int(self.x), int(self.y))
        pygame.draw.rect(screen, self.color, rect)


# =========================
# GAME LOOP
# =========================

def start_game(screen):
    """
    Main game loop.
    Called from main.py as start_game(screen).
    """
    clock = pygame.time.Clock()
    grid = Grid()

    # start player in the middle of the screen
    width, height = screen.get_size()
    player = Player(width // 2, height // 2, speed=300)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ESC to return to main menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- CONTINUOUS MOVEMENT WHILE KEY IS HELD ---
        keys = pygame.key.get_pressed()
        player.handle_input(keys, dt)
        player.clamp_to_screen(screen)

        # --- DRAW ---
        screen.fill((20, 20, 20))
        grid.draw(screen)
        player.draw(screen)

        pygame.display.flip()

    # when loop ends, we return to the menu in main.py
    return


def load_game():
    # placeholder so the Load Game button keeps working
    print("Load game not implemented yet.")
