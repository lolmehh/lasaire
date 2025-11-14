import sys
import pygame
from graphs import Button, get_screen_resolution
from functions import start_game, load_game

def quit_game():
    print("Exiting game...")
    pygame.quit()
    sys.exit()


def fade_out(screen, color=(0, 0, 0), speed=5):
    """Simple fade-out transition effect."""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)

    # ensure alpha is reset
    for alpha in range(0, 255, speed):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)


def main():
    pygame.init()
    pygame.display.set_caption("Lasaire")

    # Get resolution or fallback
    screen_width, screen_height = get_screen_resolution()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # --- Splash Screen ---
    try:
        splash = pygame.image.load("../pngs/start.png").convert()
        splash = pygame.transform.scale(splash, (screen_width, screen_height))
        screen.blit(splash, (0, 0))
        pygame.display.flip()
        pygame.time.wait(2000)  # show for 2 seconds
        fade_out(screen, color=(0, 0, 0), speed=5)
    except Exception as e:
        print(f"Could not load splash image: {e}")

    # --- Menu UI setup ---
    BACKGROUND = (25, 25, 35)
    TITLE_COLOR = (255, 255, 255)
    title_font = pygame.font.SysFont("georgia", 60)

    title_surface = title_font.render("LASAIRE", True, TITLE_COLOR)
    title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))

    # Button callbacks
    def on_start():
        fade_out(screen, color=(0, 0, 0), speed=8)
        start_game(screen)      # from functions.py
        # When start_game returns, we come back to this menu loop.

    def on_load():
        fade_out(screen, color=(0, 0, 0), speed=8)
        load_game(screen)

    def on_quit():
        quit_game()

    # Create buttons
    button_width = 250
    button_height = 70
    button_spacing = 90
    start_y = screen_height // 2 - 80

    buttons = [
        Button(
            screen_width // 2 - button_width // 2,
            start_y,
            button_width,
            button_height,
            "Start Game",
            on_start,
            text_color=(255, 255, 255),
            color=(0, 0, 0),
            hover_color=(50, 50, 50),
        ),
        Button(
            screen_width // 2 - button_width // 2,
            start_y + button_spacing,
            button_width,
            button_height,
            "Load Game",
            on_load,
            text_color=(255, 255, 255),
            color=(0, 0, 0),
            hover_color=(50, 50, 50),
        ),
        Button(
            screen_width // 2 - button_width // 2,
            start_y + button_spacing * 2,
            button_width,
            button_height,
            "Quit",
            on_quit,
            text_color=(255, 255, 255),
            color=(0, 0, 0),
            hover_color=(50, 50, 50),
        ),
    ]

    # --- Main Menu Loop ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                button.handle_event(event)

        screen.fill(BACKGROUND)
        screen.blit(title_surface, title_rect)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
