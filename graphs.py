import pygame
import sys
import tkinter as tk

# Colors
WHITE = (255, 255, 255)

# Initialize font globally after pygame.init()
pygame.init()
FONT = pygame.font.SysFont(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, callback,
                 text_color=(255, 0, 0), color=(0, 0, 0), hover_color=(50, 50, 50)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color  # normal color (black)
        self.hover_color = hover_color  # hover color (dark gray)
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        # Change background color on hover
        bg_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)  # smooth corners

        # Render text centered
        text_surface = FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                try:
                    self.callback()
                except Exception as e:
                    print(f"Error in button callback: {e}")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                try:
                    self.callback()
                except Exception as e:
                    print(f"Error in button callback: {e}")

def on_button_click():
    pygame.quit()
    sys.exit()

def get_screen_resolution():
    try:
        root = tk.Tk()
        root.withdraw()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except Exception as e:
        print(f"Error retrieving screen resolution: {e}")
        return 800, 600  # fallback

def main():
    pygame.init()
    screen_width, screen_height = get_screen_resolution()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("lasaire")

    clock = pygame.time.Clock()
    background_color = (200, 200, 190)

    button = Button(
        screen_width - 60, 10, 50, 50, "X", on_button_click,
        text_color=(255, 0, 0),  # red text
        color=(0, 0, 0),  # black base
        hover_color=(80, 80, 80)  # dark gray when hovered
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button.handle_event(event)

        screen.fill(background_color)
        button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
