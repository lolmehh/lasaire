import pygame
import sys


def start_game(screen):
    """
    Simple placeholder gameplay screen.
    Uses the SAME window as the main menu.
    Press ESC to return to the menu.
    """

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("georgia", 40)

    text_surface = font.render("Game started! Press ESC to return.", True, (255, 255, 255))
    text_rect = text_surface.get_rect(
        center=(
            screen.get_width() // 2,
            screen.get_height() // 2
        )
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # go back to menu

        screen.fill((10, 10, 30))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    # just return to menu
    return


def load_game(screen):
    """
    Placeholder 'Load Game' screen.
    """
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("georgia", 40)

    text_surface = font.render("Load Game – not implemented yet. ESC to return.", True, (255, 255, 255))
    text_rect = text_surface.get_rect(
        center=(
            screen.get_width() // 2,
            screen.get_height() // 2
        )
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((30, 10, 10))
        screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)

    return
