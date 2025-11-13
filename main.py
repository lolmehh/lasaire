import sys
import pygame
from graphs import Button, get_screen_resolution
#from functions import start_game, load_game  # your real gameplay logic here

def quit_game():
    print("Exiting game...")
    pygame.quit()
    sys.exit()

def fade_out(screen, color=(0, 0, 0), speed=5):
    """Simple fade-out transition effect."""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill(color)
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
    if not screen_width or not screen_height:
        screen_width, screen_height = 1280, 720

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Colors and fonts
    BACKGROUND = (25, 25, 35)
    TITLE_COLOR = (255, 255, 255)
    FONT = pygame.font.SysFont("georgia", 60)
    BUTTON_FONT = pygame.font.SysFont("georgia", 32)

    # Title
    title_surface = FONT.render("LASAIRE", True, TITLE_COLOR)
    title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))

    # --- Button Callbacks ---
    def on_start():
        fade_out(screen, color=(0, 0, 0), speed=8)
        start_game()  # your main gameplay function

    def on_load():
        fade_out(screen, color=(0, 0, 0), speed=8)
        load_game()

    def on_quit():
        quit_game()

    # --- Create Buttons ---
    button_width = 250
    button_height = 70
    button_spacing = 90
    start_y = screen_height // 2 - 80

    buttons = [
        Button(screen_width // 2 - button_width // 2, start_y, button_width, button_height,
               "Start Game", on_start, text_color=(255, 255, 255),
               color=(0, 0, 0), hover_color=(50, 50, 50)),

        Button(screen_width // 2 - button_width // 2, start_y + button_spacing, button_width, button_height,
               "Load Game", on_load, text_color=(255, 255, 255),
               color=(0, 0, 0), hover_color=(50, 50, 50)),

        Button(screen_width // 2 - button_width // 2, start_y + button_spacing * 2, button_width, button_height,
               "Quit", on_quit, text_color=(255, 255, 255),
               color=(0, 0, 0), hover_color=(50, 50, 50)),
    ]

    # --- Main Loop ---
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
