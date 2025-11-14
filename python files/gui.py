# gui.py
import pygame
from graphs import Button

PANEL_COLOR = (15, 15, 25)
PANEL_ALPHA = 220
TEXT_COLOR = (255, 255, 255)


class SettingsMenu:
    def __init__(self, screen, settings, on_close=None):
        """
        Simple settings overlay.

        screen: the main pygame display Surface
        settings: dict with settings values the game reads, e.g. {"show_grid": True}
        on_close: optional callback when the menu is closed (to unpause the game)
        """
        self.screen = screen
        self.settings = settings
        self.on_close = on_close
        self.visible = False

        self.screen_width, self.screen_height = self.screen.get_size()

        # Panel rectangle in the middle of the screen
        panel_width = 400
        panel_height = 260
        self.panel_rect = pygame.Rect(
            (self.screen_width - panel_width) // 2,
            (self.screen_height - panel_height) // 2,
            panel_width,
            panel_height,
        )

        self.font_title = pygame.font.SysFont("georgia", 32)
        self.font_text = pygame.font.SysFont("georgia", 24)

        self.buttons = []

        # --- Buttons inside settings panel ---

        btn_w = 260
        btn_h = 50
        start_y = self.panel_rect.y + 80
        spacing = 70

        def toggle_grid():
            self.settings["show_grid"] = not self.settings.get("show_grid", True)
            print("Show grid:", self.settings["show_grid"])

        def close_menu():
            self.visible = False
            if self.on_close:
                self.on_close()

        # Toggle grid button
        self.buttons.append(
            Button(
                self.panel_rect.x + (self.panel_rect.width - btn_w) // 2,
                start_y,
                btn_w,
                btn_h,
                "Toggle grid",
                toggle_grid,
                text_color=(255, 255, 255),
                color=(0, 0, 0),
                hover_color=(70, 70, 70),
            )
        )

        # Resume button
        self.buttons.append(
            Button(
                self.panel_rect.x + (self.panel_rect.width - btn_w) // 2,
                start_y + spacing,
                btn_w,
                btn_h,
                "Resume",
                close_menu,
                text_color=(255, 255, 255),
                color=(0, 0, 0),
                hover_color=(70, 70, 70),
            )
        )

    def open(self):
        self.visible = True

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # ESC also closes the menu
            self.visible = False
            if self.on_close:
                self.on_close()
            return

        for b in self.buttons:
            b.handle_event(event)

    def draw(self):
        if not self.visible:
            return

        # Dim the game behind with a translucent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # Settings panel
        panel_surface = pygame.Surface(self.panel_rect.size, pygame.SRCALPHA)
        panel_surface.fill((*PANEL_COLOR, PANEL_ALPHA))
        self.screen.blit(panel_surface, self.panel_rect.topleft)

        # Title text
        title_surf = self.font_title.render("Settings", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(self.panel_rect.centerx,
                                                 self.panel_rect.y + 40))
        self.screen.blit(title_surf, title_rect)

        # Draw buttons
        for b in self.buttons:
            b.draw(self.screen)
