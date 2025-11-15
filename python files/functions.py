import pygame
import sys
import math

from graphs import Button
from gui import SettingsMenu

from grid import Grid    # or whatever modules you import
from items import ItemStack, create_item, Item



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

class Player:
    def __init__(self, x, y, speed=300):
        # world coordinates (floats for smoothness)
        self.x = float(x)
        self.y = float(y)
        self.speed = speed  # pixels per second

        # Visuals
        self.size = 30
        self.color = (255, 0, 0)

        # Basic stats
        self.max_hp = 100
        self.hp = self.max_hp

        # Inventory
        self.inventory: list[ItemStack] = []
        self.inventory_max_slots = 20  # change this if you want more/less slots

        # Equipped items
        self.equipped_weapon: Item | None = None

    # -----------------------------
    # Movement
    # -----------------------------
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

    def draw(self, screen, camera):
        # Convert center from world -> screen
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)

        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (int(screen_x), int(screen_y))
        pygame.draw.rect(screen, self.color, rect)

    # -----------------------------
    # Inventory helpers
    # -----------------------------
    def add_item(self, item, amount: int = 1) -> bool:
        """
        Add an Item (or multiple) to the inventory.

        You can pass:
          - an Item instance, or
          - an item_id string (e.g. "slime_goop")

        Returns True if everything was added, False if there's not enough space.
        """

        # If we got an item_id string instead of an Item instance, create it:
        if isinstance(item, str):
            item = create_item(item)

        # If it's stackable, try to add to an existing stack first
        if item.stackable:
            for stack in self.inventory:
                if stack.item.id == item.id and not stack.is_full():
                    can_add = item.max_stack - stack.amount
                    to_add = min(can_add, amount)
                    stack.amount += to_add
                    amount -= to_add
                    if amount <= 0:
                        return True  # everything added

        # If there's still some amount left, we need new slots
        while amount > 0:
            if len(self.inventory) >= self.inventory_max_slots:
                # No more slots
                return False

            to_add = min(amount, item.max_stack if item.stackable else 1)
            self.inventory.append(ItemStack(item, to_add))
            amount -= to_add

        return True

    def remove_item(self, item_id: str, amount: int = 1) -> bool:
        """
        Remove a certain amount of an item from the inventory.
        Returns True if successful, False if not enough items.
        """
        for stack in list(self.inventory):  # copy so we can remove safely
            if stack.item.id == item_id:
                if stack.amount > amount:
                    stack.amount -= amount
                    return True
                elif stack.amount == amount:
                    self.inventory.remove(stack)
                    return True
                else:
                    # Stack has less than we want: remove it and keep going
                    amount -= stack.amount
                    self.inventory.remove(stack)
                    if amount <= 0:
                        return True
        return False

    def count_item(self, item_id: str) -> int:
        """
        How many of this item the player has in total.
        """
        total = 0
        for stack in self.inventory:
            if stack.item.id == item_id:
                total += stack.amount
        return total

    def debug_print_inventory(self):
        """
        Handy while developing: prints the inventory to the console.
        """
        print("=== INVENTORY ===")
        if not self.inventory:
            print("(empty)")
        for stack in self.inventory:
            print(f"{stack.item.name} x{stack.amount}")
        print("=================")

    # -----------------------------
    # Equipping / using items
    # -----------------------------
    def equip_weapon(self, item: Item):
        """Equip a weapon (does NOT remove it from inventory)."""
        self.equipped_weapon = item
        print(f"Equipped weapon: {item.name}")

    def use_consumable(self, item: Item):
        """Use a consumable (simple heal for now)."""
        heal = getattr(item, "heal_amount", 0)
        if heal > 0:
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + heal)
            print(f"Used {item.name}: HP {old_hp} -> {self.hp}")
        else:
            print(f"Used {item.name}, but it has no heal effect (yet).")

        # Consume 1 from inventory
        self.remove_item(item.id, 1)

    def use_item(self, item: Item):
        """
        Generic "use or equip" based on item category.
        Called by the inventory UI when you right-click or press Enter.
        """
        cat = (item.category or "").lower()
        if cat == "weapon":
            self.equip_weapon(item)
        elif cat == "consumable":
            self.use_consumable(item)
        else:
            print(f"You can't use {item.name} (category: {item.category})")

    def get_equipped_weapon_name(self) -> str:
        if self.equipped_weapon is None:
            return "None"
        return self.equipped_weapon.name

    def get_attack_damage(self, base_damage: int = 1) -> int:
        """
        Example: base damage + weapon damage.
        You can hook this into your combat system later.
        """
        weapon_damage = self.equipped_weapon.damage if self.equipped_weapon else 0
        return base_damage + weapon_damage


    def remove_item(self, item_id: str, amount: int = 1) -> bool:
        """
        Remove a certain amount of an item from the inventory.
        Returns True if successful, False if not enough items.
        """
        for stack in list(self.inventory):  # copy so we can remove safely
            if stack.item.id == item_id:
                if stack.amount > amount:
                    stack.amount -= amount
                    return True
                elif stack.amount == amount:
                    self.inventory.remove(stack)
                    return True
                else:
                    # Stack has less than we want: remove it and keep going
                    amount -= stack.amount
                    self.inventory.remove(stack)
                    if amount <= 0:
                        return True
        return False

    def count_item(self, item_id: str) -> int:
        """
        How many of this item the player has in total.
        """
        total = 0
        for stack in self.inventory:
            if stack.item.id == item_id:
                total += stack.amount
        return total

    def debug_print_inventory(self):
        """
        Handy while developing: prints the inventory to the console.
        """
        print("=== INVENTORY ===")
        if not self.inventory:
            print("(empty)")
        for stack in self.inventory:
            print(f"{stack.item.name} x{stack.amount}")
        print("=================")
def start_game(screen):
    """Main game loop. main.py calls: start_game(screen)"""
    clock = pygame.time.Clock()

    grid = Grid()
    camera = Camera(screen, WORLD_WIDTH, WORLD_HEIGHT)

    # Start player in the center of the world
    player = Player(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, speed=300)

    # Give some starting items so you can see the inventory working
    player.add_item("rusty_sword", 1)
    player.add_item("small_potion", 2)
    player.add_item("slime_goop", 5)

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
    inventory_open = False
    inventory_category = "all"  # "all", "weapon", "consumable", "material", "other"

    # Selected item index (within the FILTERED list, not the full inventory)
    selected_index = 0

    # We will fill this each frame when drawing the inventory
    item_slots: list[tuple[pygame.Rect, int]] = []
    filtered_stacks: list[ItemStack] = []

    # Fonts
    font = pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont(None, 20)

    # Simple text wrap helper for description box
    def wrap_text(text: str, max_chars: int = 60):
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

    def item_matches_category(stack: ItemStack, cat_id: str) -> bool:
        cat = (stack.item.category or "").lower()
        cat_id = cat_id.lower()
        if cat_id == "all":
            return True
        if cat_id == "other":
            return cat not in ("weapon", "consumable", "material")
        return cat == cat_id

    def on_settings_close():
        nonlocal paused
        if not inventory_open:
            paused = False

    def go_back_to_main_menu():
        nonlocal paused, running, inventory_open
        paused = False
        inventory_open = False
        running = False   # exit game loop, main.py shows the menu again

    settings_menu = SettingsMenu(
        screen,
        settings=settings,
        on_close=on_settings_close,
        on_return_to_menu=go_back_to_main_menu,
    )

    def open_settings():
        nonlocal paused, inventory_open
        paused = True
        inventory_open = False   # close inventory when opening settings
        settings_menu.open()

    settings_button.callback = open_settings

    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        # Rebuild filtered list each frame, keep selected_index in range
        filtered_stacks = [s for s in player.inventory if item_matches_category(s, inventory_category)]
        if selected_index >= len(filtered_stacks):
            selected_index = max(0, len(filtered_stacks) - 1)

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
                        inventory_open = not inventory_open
                        if inventory_open:
                            paused = True
                        else:
                            paused = settings_menu.visible

                    # Category hotkeys (only when inventory is open)
                    if inventory_open:
                        if event.key == pygame.K_1:
                            inventory_category = "all"
                            selected_index = 0
                        elif event.key == pygame.K_2:
                            inventory_category = "weapon"
                            selected_index = 0
                        elif event.key == pygame.K_3:
                            inventory_category = "consumable"
                            selected_index = 0
                        elif event.key == pygame.K_4:
                            inventory_category = "material"
                            selected_index = 0
                        elif event.key == pygame.K_5:
                            inventory_category = "other"
                            selected_index = 0

                        # Selection movement with arrows
                        if filtered_stacks:
                            cols = 6  # number of columns in the grid
                            if event.key == pygame.K_RIGHT:
                                if selected_index + 1 < len(filtered_stacks):
                                    selected_index += 1
                            elif event.key == pygame.K_LEFT:
                                if selected_index - 1 >= 0:
                                    selected_index -= 1
                            elif event.key == pygame.K_DOWN:
                                if selected_index + cols < len(filtered_stacks):
                                    selected_index += cols
                            elif event.key == pygame.K_UP:
                                if selected_index - cols >= 0:
                                    selected_index -= cols

                            # Use/equip with Enter or Space
                            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                                item = filtered_stacks[selected_index].item
                                player.use_item(item)

                # --- Mouse (for inventory clicks) ---
                if inventory_open and event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    # left-click = select, right-click = use/equip
                    if event.button in (1, 3):
                        for rect, idx in item_slots:
                            if rect.collidepoint(mx, my):
                                selected_index = idx
                                if event.button == 3 and 0 <= idx < len(filtered_stacks):
                                    item = filtered_stacks[idx].item
                                    player.use_item(item)
                                break

                # Settings button only active when menu is not open
                settings_button.handle_event(event)

        if not paused:
            keys = pygame.key.get_pressed()
            player.handle_input(keys, dt)
            player.clamp_to_world()
            camera.update(player.x, player.y)

        # --- DRAW WORLD ---
        screen.fill(BACKGROUND_COLOR)

        if settings.get("show_grid", True):
            # If your Grid uses camera, call grid.draw(screen, camera)
            # If it doesn't, just use grid.draw(screen)
            try:
                grid.draw(screen, camera)
            except TypeError:
                grid.draw(screen)

        player.draw(screen, camera)
        settings_button.draw(screen)
        settings_menu.draw()

        # --- INVENTORY OVERLAY ---
        item_slots = []  # rebuild every frame we draw the inventory

        if inventory_open:
            # darken whole screen
            dim_surface = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            dim_surface.fill((0, 0, 0, 120))
            screen.blit(dim_surface, (0, 0))

            # big central panel (80% of screen)
            panel_width = int(screen_w * 0.8)
            panel_height = int(screen_h * 0.8)
            panel_x = (screen_w - panel_width) // 2
            panel_y = (screen_h - panel_height) // 2

            panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            panel_surface.fill((15, 15, 25, 230))
            screen.blit(panel_surface, (panel_x, panel_y))

            # Title
            title_text = "Inventory (I to close)"
            title_surf = font.render(title_text, True, (255, 255, 255))
            title_rect = title_surf.get_rect(midleft=(panel_x + 20, panel_y + 30))
            screen.blit(title_surf, title_rect)

            # Equipped weapon info (top-right)
            eq_text = f"Equipped weapon: {player.get_equipped_weapon_name()}"
            eq_surf = font_small.render(eq_text, True, (220, 220, 220))
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
                is_active = (cat_id == inventory_category)
                color = (255, 255, 0) if is_active else (200, 200, 200)
                cat_surf = font_small.render(cat_label, True, color)
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
            SLOT_SIZE = 64
            SLOT_PAD = 10
            COLS = 6
            desc_area_height = 120

            grid_x = panel_x + 30
            grid_y = cat_y + 40
            max_grid_bottom = panel_y + panel_height - desc_area_height - 10

            if not filtered_stacks:
                msg = "(no items in this category)"
                msg_surf = font.render(msg, True, (200, 200, 200))
                screen.blit(msg_surf, (grid_x, grid_y))
            else:
                for idx, stack in enumerate(filtered_stacks):
                    row = idx // COLS
                    col = idx % COLS

                    x = grid_x + col * (SLOT_SIZE + SLOT_PAD)
                    y = grid_y + row * (SLOT_SIZE + SLOT_PAD)

                    rect = pygame.Rect(x, y, SLOT_SIZE, SLOT_SIZE)

                    # Stop drawing if we hit the bottom of the panel
                    if rect.bottom > max_grid_bottom:
                        break

                    item_slots.append((rect, idx))

                    # Background
                    pygame.draw.rect(screen, (30, 30, 45), rect)

                    # Border color
                    border_color = (120, 120, 160)
                    if player.equipped_weapon is not None and stack.item is player.equipped_weapon:
                        border_color = (80, 200, 120)  # equipped
                    if idx == selected_index:
                        border_color = (255, 255, 0)    # selected

                    pygame.draw.rect(screen, border_color, rect, 2)

                    # Item name (shortened) and quantity
                    name = stack.item.name
                    if len(name) > 8:
                        name = name[:7] + "…"

                    name_surf = font_small.render(name, True, (230, 230, 230))
                    name_rect = name_surf.get_rect(center=(rect.centerx, rect.y + 14))
                    screen.blit(name_surf, name_rect)

                    qty_text = f"x{stack.amount}"
                    qty_surf = font_small.render(qty_text, True, (200, 200, 200))
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

            if filtered_stacks and 0 <= selected_index < len(filtered_stacks):
                stack = filtered_stacks[selected_index]
                item = stack.item

                title_line = item.name
                cat_line = f"Category: {item.category} | Damage: {item.damage} | Heal: {item.heal_amount} | Value: {item.value}"

                if player.equipped_weapon is not None and item is player.equipped_weapon:
                    cat_line += "  (Equipped)"

                desc_lines = wrap_text(item.description or "No description yet.", max_chars=70)

                y = inner_y
                title_surf = font.render(title_line, True, (255, 255, 255))
                screen.blit(title_surf, (inner_x, y))
                y += 26

                cat_surf = font_small.render(cat_line, True, (210, 210, 210))
                screen.blit(cat_surf, (inner_x, y))
                y += 24

                for line in desc_lines:
                    if y > desc_y + desc_h - 30:
                        break
                    line_surf = font_small.render(line, True, (200, 200, 200))
                    screen.blit(line_surf, (inner_x, y))
                    y += 20

            hint_text = "Right-click or Enter/Space to equip/use.  1–5 to change category."
            hint_surf = font_small.render(hint_text, True, (180, 180, 200))
            hint_rect = hint_surf.get_rect(
                bottomright=(desc_x + desc_w - 10, desc_y + desc_h - 4)
            )
            screen.blit(hint_surf, hint_rect)

        pygame.display.flip()

    return





def load_game():
    # placeholder so the "Load Game" button keeps working
    print("Load game not implemented yet.")
