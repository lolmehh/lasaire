import pygame
import tkinter as tk

# Colors
WHITE = (255, 255, 255)


class Button:
    def __init__(
        self,
        x, y, width, height,
        text,
        callback,
        text_color=(255, 255, 255),
        color=(0, 0, 0),
        hover_color=(50, 50, 50)
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        # Hover color
        bg_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)

        # Font created here (pygame.init() will be called in main.py)
        font = pygame.font.SysFont("georgia", 32)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                # No try/except here so errors are visible while debugging
                self.callback()


def get_screen_resolution():
    """Try to get the OS screen size, fall back to 1280x720."""
    try:
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception as e:
        print(f"Error retrieving screen resolution: {e}")
        return 1280, 720
