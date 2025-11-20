import pygame
from items import ItemStack


class InventoryUI:
    def __init__(self):
        self.open = False
        self.category = "all"  # "all", "weapon", "consumable", "material", "other"
        self.selected_index = 0

        # Fonts for UI
        self.font = pygame.font.SysFont(None, 24)
        self.font_small = pygame.font.SysFont(None, 20)

        # list of (pygame.Rect, item_index) for mouse hit detection
        self.item_slots: list[tuple[pygame.Rect, int]] = []

    # ------------- state helpers -------------

    def toggle(self):
        self.open = not self.open

    def close(self):
        self.open = False

    # ------------- internal helpers -------------

    def _wrap_text(self, text: str, max_chars: int = 60):
        words = text.split()
        lines = []
        current = ""
        for w in words:
            if not current:
                current = w
            elif len(current) + 1 + len(w) <= max_chars:
                current += " " + w
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
        return lines

    def _matches_category(self, stack: ItemStack) -> bool:
        cat = (stack.item.category or "").lower()
        cat_id = self.category.lower()
        if cat_id == "all":
            return True
        if cat_id == "other":
            return cat not in ("weapon", "consumable", "material")
        return cat == cat_id

    def _get_filtered_stacks(self, player):
        return [s for s in player.inventory if self._matches_category(s)]

    # ------------- input handling -------------

    def handle_key(self, key, player):
        """Handle keyboard input when inventory is open."""
        if not self.open:
            return

        # Category hotkeys
        if key == pygame.K_1:
            self.category = "all"
            self.selected_index = 0
        elif key == pygame.K_2:
            self.category = "weapon"
            self.selected_index = 0
        elif key == pygame.K_3:
            self.category = "consumable"
            self.selected_index = 0
        elif key == pygame.K_4:
            self.category = "material"
            self.selected_index = 0
        elif key == pygame.K_5:
            self.category = "other"
            self.selected_index = 0

        filtered = self._get_filtered_stacks(player)
        if not filtered:
            self.selected_index = 0
            return

        cols = 6  # number of columns in the grid

        # Move selection
        if key == pygame.K_RIGHT and self.selected_index + 1 < len(filtered):
            self.selected_index += 1
        elif key == pygame.K_LEFT and self.selected_index - 1 >= 0:
            self.selected_index -= 1
        elif key == pygame.K_DOWN and self.selected_index + cols < len(filtered):
            self.selected_index += cols
        elif key == pygame.K_UP and self.selected_index - cols >= 0:
            self.selected_index -= cols

        # Use / equip selected
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            item = filtered[self.selected_index].item
            player.use_item(item)

    def handle_mouse(self, event, player):
        """Handle mouse clicks (select / use items)."""
        if not self.open:
            return
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        mx, my = event.pos

        # left click = select, right click = use/equip
        if event.button in (1, 3):
            for rect, idx in self.item_slots:
                if rect.collidepoint(mx, my):
                    self.selected_index = idx
                    filtered = self._get_filtered_stacks(player)
                    if event.button == 3 and 0 <= idx < len(filtered):
                        item = filtered[idx].item
                        player.use_item(item)
                    break

    # ------------- drawing -------------

    def draw(self, screen, player):
        """Draw the inventory overlay. No-op if not open."""
        if not self.open:
            self.item_slots = []
            return

        screen_w, screen_h = screen.get_size()
        filtered = self._get_filtered_stacks(player)
        if self.selected_index >= len(filtered):
            self.selected_index = max(0, len(filtered) - 1)

        # Darken whole screen
        dim_surface = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        dim_surface.fill((0, 0, 0, 120))
        screen.blit(dim_surface, (0, 0))

        # Big central panel (80% of screen)
        panel_width = int(screen_w * 0.8)
        panel_height = int(screen_h * 0.8)
        panel_x = (screen_w - panel_width) // 2
        panel_y = (screen_h - panel_height) // 2

        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((15, 15, 25, 230))
        screen.blit(panel_surface, (panel_x, panel_y))

        # Title
        title_text = "Inventory (I to close)"
        title_surf = self.font.render(title_text, True, (255, 255, 255))
        title_rect = title_surf.get_rect(midleft=(panel_x + 20, panel_y + 30))
        screen.blit(title_surf, title_rect)

        # Equipped weapon info (top-right)
        eq_text = f"Equipped weapon: {player.get_equipped_weapon_name()}"
        eq_surf = self.font_small.render(eq_text, True, (220, 220, 220))
        eq_rect = eq_surf.get_rect(midright=(panel_x + panel_width - 20, panel_y + 30))
        screen.blit(eq_surf, eq_rect)

        # Category bar
        category_labels = [
            ("all", "1: All"),
            ("weapon", "2: Weapons"),
            ("consumable", "3: Consumables"),
            ("material", "4: Materials"),
            ("other", "5: Other"),
        ]
        cat_x = panel_x + 20
        cat_y = panel_y + 70
        cat_spacing = 120

        for cat_id, cat_label in category_labels:
            is_active = (cat_id == self.category)
            color = (255, 255, 0) if is_active else (200, 200, 200)
            cat_surf = self.font_small.render(cat_label, True, color)
            screen.blit(cat_surf, (cat_x, cat_y))
            cat_x += cat_spacing

        pygame.draw.line(
            screen,
            (80, 80, 120),
            (panel_x + 15, cat_y + 24),
            (panel_x + panel_width - 15, cat_y + 24),
            2,
        )

        # Grid of item slots
        self.item_slots = []  # rebuild each frame

        slot_size = 64
        slot_pad = 10
        cols = 6
        desc_area_height = 120

        grid_x = panel_x + 30
        grid_y = cat_y + 40
        max_grid_bottom = panel_y + panel_height - desc_area_height - 10

        if not filtered:
            msg = "(no items in this category)"
            msg_surf = self.font.render(msg, True, (200, 200, 200))
            screen.blit(msg_surf, (grid_x, grid_y))
        else:
            for idx, stack in enumerate(filtered):
                row = idx // cols
                col = idx % cols

                x = grid_x + col * (slot_size + slot_pad)
                y = grid_y + row * (slot_size + slot_pad)

                rect = pygame.Rect(x, y, slot_size, slot_size)
                if rect.bottom > max_grid_bottom:
                    break

                self.item_slots.append((rect, idx))

                # Background
                pygame.draw.rect(screen, (30, 30, 45), rect)

                # Border color
                border_color = (120, 120, 160)
                if player.equipped_weapon is not None and stack.item is player.equipped_weapon:
                    border_color = (80, 200, 120)  # equipped
                if idx == self.selected_index:
                    border_color = (255, 255, 0)    # selected

                pygame.draw.rect(screen, border_color, rect, 2)

                # Item name (shortened) and quantity
                name = stack.item.name
                if len(name) > 8:
                    name = name[:7] + "…"

                name_surf = self.font_small.render(name, True, (230, 230, 230))
                name_rect = name_surf.get_rect(center=(rect.centerx, rect.y + 14))
                screen.blit(name_surf, name_rect)

                qty_text = f"x{stack.amount}"
                qty_surf = self.font_small.render(qty_text, True, (200, 200, 200))
                qty_rect = qty_surf.get_rect(bottomright=(rect.right - 4, rect.bottom - 4))
                screen.blit(qty_surf, qty_rect)

        # --- Description box at the bottom ---
        desc_x = panel_x + 20
        desc_y = panel_y + panel_height - desc_area_height
        desc_w = panel_width - 40
        desc_h = desc_area_height - 20

        desc_rect = pygame.Rect(desc_x, desc_y, desc_w, desc_h)
        pygame.draw.rect(screen, (25, 25, 40), desc_rect)
        pygame.draw.rect(screen, (80, 80, 120), desc_rect, 2)

        inner_x = desc_x + 10
        inner_y = desc_y + 10

        if filtered and 0 <= self.selected_index < len(filtered):
            stack = filtered[self.selected_index]
            item = stack.item

            title_line = item.name
            cat_line = (
                f"Category: {item.category} | Damage: {item.damage} "
                f"| Heal: {item.heal_amount} | Value: {item.value}"
            )
            if player.equipped_weapon is not None and item is player.equipped_weapon:
                cat_line += "  (Equipped)"

            desc_lines = self._wrap_text(item.description or "No description yet.", max_chars=70)

            y = inner_y
            title_surf = self.font.render(title_line, True, (255, 255, 255))
            screen.blit(title_surf, (inner_x, y))
            y += 26

            cat_surf = self.font_small.render(cat_line, True, (210, 210, 210))
            screen.blit(cat_surf, (inner_x, y))
            y += 24

            for line in desc_lines:
                if y > desc_y + desc_h - 30:
                    break
                line_surf = self.font_small.render(line, True, (200, 200, 200))
                screen.blit(line_surf, (inner_x, y))
                y += 20

        hint_text = "Right-click or Enter/Space to equip/use.  1–5 to change category."
        hint_surf = self.font_small.render(hint_text, True, (180, 180, 200))
        hint_rect = hint_surf.get_rect(
            bottomright=(desc_x + desc_w - 10, desc_y + desc_h - 4)
        )
        screen.blit(hint_surf, hint_rect)
