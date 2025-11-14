import pygame
import sys
import math

from graphs import Button
from gui import SettingsMenu

from grid import Grid, Player    # or whatever modules you import

# WORLD / CAMERA SETTINGS

TILE_SIZE = 40
GRID_COLOR = (60, 60, 60)

# Size of your game world in pixels (not the same as screen size)
WORLD_WIDTH = 4000
WORLD_HEIGHT = 4000

BACKGROUND_COLOR = (20, 20, 20)


# CAMERA

class Camera:
    def __init__(self, screen, world_width, world_height):
        self.screen = screen
        self.world_width = world_width
        self.world_height = world_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target_x, target_y):
        """
        Center the camera on (target_x, target_y),
        and clamp so we don't go outside the world.
        """
        screen_w, screen_h = self.screen.get_size()

        # center on target
        self.offset_x = target_x - screen_w / 2
        self.offset_y = target_y - screen_h / 2

        # clamp to world bounds
        self.offset_x = max(0, min(self.offset_x, self.world_width - screen_w))
        self.offset_y = max(0, min(self.offset_y, self.world_height - screen_h))

    def world_to_screen(self, x, y):
        """
        Convert world coordinates (x, y) -> screen coordinates.
        Use this for any object you draw.
        """
        return x - self.offset_x, y - self.offset_y


# GRID (BACKGROUND)

class Grid:
    def __init__(self, tile_size=TILE_SIZE):
        self.tile_size = tile_size

    def draw(self, screen, camera: Camera):
        screen_w, screen_h = screen.get_size()

        # We only need to draw lines that fall inside the current view.
        # Compute which world lines are visible.
        start_x = int(camera.offset_x // self.tile_size) * self.tile_size
        end_x = int((camera.offset_x + screen_w) // self.tile_size + 1) * self.tile_size

        start_y = int(camera.offset_y // self.tile_size) * self.tile_size
        end_y = int((camera.offset_y + screen_h) // self.tile_size + 1) * self.tile_size

        # Vertical lines
        x = start_x
        while x <= end_x and x <= WORLD_WIDTH:
            sx, _ = camera.world_to_screen(x, 0)
            pygame.draw.line(screen, GRID_COLOR, (sx, 0), (sx, screen_h))
            x += self.tile_size

        # Horizontal lines
        y = start_y
        while y <= end_y and y <= WORLD_HEIGHT:
            _, sy = camera.world_to_screen(0, y)
            pygame.draw.line(screen, GRID_COLOR, (0, sy), (screen_w, sy))
            y += self.tile_size


# movement

class Player:
    def __init__(self, x, y, speed=300):
        # world coordinates (floats for smoothness)
        self.x = float(x)
        self.y = float(y)
        self.speed = speed  # pixels per second
        self.size = 30
        self.color = (255, 0, 0)

    def handle_input(self, keys, dt):
        dx = 0
        dy = 0

        # Hold keys for continuous movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        if dx != 0 or dy != 0:
            # Normalize so diagonals are not faster
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

            self.x += dx * self.speed * dt
            self.y += dy * self.speed * dt

    def clamp_to_world(self):
        half = self.size / 2
        self.x = max(half, min(WORLD_WIDTH - half, self.x))
        self.y = max(half, min(WORLD_HEIGHT - half, self.y))

    def draw(self, screen, camera: Camera):
        # Convert center from world -> screen
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (int(screen_x), int(screen_y))
        pygame.draw.rect(screen, self.color, rect)

def start_game(screen):
    """Main game loop. main.py calls: start_game(screen)"""
    clock = pygame.time.Clock()

    grid = Grid()
    camera = Camera(screen, WORLD_WIDTH, WORLD_HEIGHT)

    # Start player in the center of the world
    player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, speed=300)

    # --- GUI / settings ---
    screen_w, screen_h = screen.get_size()
    button_size = 50

    # Top-right settings button (⚙)
    settings_button = Button(
        screen_w - button_size - 10,
        10,
        button_size,
        button_size,
        "+",
        callback=None,  # we set this just below
        text_color=(255, 255, 255),
        color=(0, 0, 0),
        hover_color=(80, 80, 80),
    )

    # Simple settings dict – the menu can change these, the game reads them
    settings = {
        "show_grid": True,
    }

    paused = False

    def on_settings_close():
        nonlocal paused
        paused = False

    def go_back_to_main_menu():
        # Called when the user clicks "Return to main menu" in Settings
        nonlocal paused, running
        paused = False
        running = False   # this will exit the game loop, then main.py shows the menu again

    settings_menu = SettingsMenu(
        screen,
        settings=settings,
        on_close=on_settings_close,
        on_return_to_menu=go_back_to_main_menu,
    )


    def open_settings():
        nonlocal paused
        paused = True
        settings_menu.open()

    # Hook up button callback now that open_settings exists
    settings_button.callback = open_settings

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if settings_menu.visible:
                # While the menu is open, only it gets the events
                settings_menu.handle_event(event)
            else:
                # ESC: return to main menu (back to main.py)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

                # Settings button only active when menu is not open
                settings_button.handle_event(event)

        if not paused:
            # UPDATE gameplay
            keys = pygame.key.get_pressed()
            player.handle_input(keys, dt)
            player.clamp_to_world()

            # Camera focuses the player
            camera.update(player.x, player.y)

        # DRAW
        screen.fill(BACKGROUND_COLOR)

        if settings.get("show_grid", True):
            grid.draw(screen, camera)

        player.draw(screen, camera)
        settings_button.draw(screen)
        settings_menu.draw()

        pygame.display.flip()

    # When loop ends, we return to the menu in main.py
    return



def load_game():
    # placeholder so the "Load Game" button keeps working
    print("Load game not implemented yet.")
