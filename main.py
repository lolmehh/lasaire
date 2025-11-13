import sys
import pygame
from graphs import Button, get_screen_resolution

# Placeholder imports — replace with your actual game functions
# from functions import start_game, load_game

def start_game():
    print("Starting new game...")  # placeholder
    pygame.time.wait(1000)

def load_game():
    print("Loading game...")  # placeholder
    pygame.time.wait(1000)

def quit_game():
    print("Exiting game...")
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    pygame.display.set_caption("Lasaire")

    # Get full screen resolution or fallback
    screen_width, screen_height = get_screen_resolution()
    if not screen_width or not screen_height:
        screen_width, screen_height = 1280, 720

    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Colors
    BACKGROUND = (25, 25, 35)
    TITLE_COLOR = (255, 255, 255)
    FONT = pygame.font.SysFont("georgia", 60)
    BUTTON_FONT = pygame.font.SysFont("georgia", 32)

    # Title
    title_surface = FONT.render("LASAIRE", True, TITLE_COLOR)
    title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))

    # Create buttons
    button_width = 250
    button_height = 70
    button_spacing = 90
    start_y = screen_height // 2 - 80

    buttons = [
        Button(screen_width // 2 - button_width // 2, start_y, button_width, button_height,
               "Start Game", start_game, text_color=(255, 0, 0),
               color=(0, 0, 0), hover_color=(50, 50, 50)),

        Button(screen_width // 2 - button_width // 2, start_y + button_spacing, button_width, button_height,
               "Load Game", load_game, text_color=(255, 0, 0),
               color=(0, 0, 0), hover_color=(50, 50, 50)),

        Button(screen_width // 2 - button_width // 2, start_y + button_spacing * 2, button_width, button_height,
               "Quit", quit_game, text_color=(255, 0, 0),
               color=(0, 0, 0), hover_color=(50, 50, 50)),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in buttons:
                button.handle_event(event)

        # Draw background and title
        screen.fill(BACKGROUND)
        screen.blit(title_surface, title_rect)

        # Draw all buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
