import pygame
import sys

from graphs import Button
from gui import SettingsMenu

from grid import Grid
from camera import Camera
from player import Player
from inventory_ui import InventoryUI


# WORLD / CAMERA SETTINGS

TILE_SIZE = 40
GRID_COLOR = (60, 60, 60)

WORLD_WIDTH = 4000
WORLD_HEIGHT = 4000
BACKGROUND_COLOR = (30, 30, 40)

def start_game(screen):
    """Main game loop. main.py calls: start_game(screen)"""
    clock = pygame.time.Clock()

    grid = Grid()
    camera = Camera(screen, WORLD_WIDTH, WORLD_HEIGHT)

    # Start player in the center of the world
    player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, speed=300)

    # Give some starting items so you can see the inventory working
    player.add_item("rusty_sword", 2)
    player.add_item("small_hp_potion", 200)
    player.add_item("slime_goo", 5)

    # --- GUI / settings ---
    screen_w, screen_h = screen.get_size()
    button_size = 50

    # Top-right settings button
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

    settings = {
        "show_grid": True,
    }

    paused = False

    # Inventory UI (new)
    inventory_ui = InventoryUI()

    def on_settings_close():
        nonlocal paused
        # Only unpause if the inventory is not open
        if not inventory_ui.open:
            paused = False

    def go_back_to_main_menu():
        nonlocal paused, running
        paused = False
        inventory_ui.close()
        running = False   # exit game loop, main.py shows the menu again

    settings_menu = SettingsMenu(
        screen,
        settings=settings,
        on_close=on_settings_close,
        on_return_to_menu=go_back_to_main_menu,
    )

    def open_settings():
        nonlocal paused
        paused = True
        inventory_ui.close()
        settings_menu.open()

    settings_button.callback = open_settings

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if settings_menu.visible:
                settings_menu.handle_event(event)
            else:
                # --- Keyboard ---
                if event.type == pygame.KEYDOWN:
                    # ESC: return to main menu
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    # I: open/close inventory
                    elif event.key == pygame.K_i:
                        inventory_ui.toggle()
                        paused = inventory_ui.open or settings_menu.visible

                    # Inventory key controls
                    if inventory_ui.open:
                        inventory_ui.handle_key(event.key, player)

                # Mouse inside inventory
                if inventory_ui.open:
                    inventory_ui.handle_mouse(event, player)

                # Settings button still active when menus closed
                settings_button.handle_event(event)

        if not paused:
            keys = pygame.key.get_pressed()
            player.handle_input(keys, dt)
            # Your Player.clamp_to_world() still uses WORLD_WIDTH/HEIGHT
            player.clamp_to_world(WORLD_WIDTH,WORLD_HEIGHT)
            camera.update(player.x, player.y)

        # --- DRAW WORLD ---
        screen.fill(BACKGROUND_COLOR)

        if settings.get("show_grid", True):
            grid.draw(screen, camera)

        player.draw(screen, camera)
        settings_button.draw(screen)
        settings_menu.draw()

        # --- INVENTORY OVERLAY ---
        inventory_ui.draw(screen, player)

        pygame.display.flip()

    return

def load_game():
    # placeholder so the "Load Game" button keeps working
    print("Load game not implemented yet.")
