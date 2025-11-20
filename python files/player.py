# player.py

import math
import pygame
from items import ItemStack, create_item, Item


class Player:
    def __init__(self, x, y, speed=300):
        # world coordinates (floats for smoothness)
        self.x = float(x)
        self.y = float(y)
        self.speed = speed  # pixels per second

        # Visuals
        self.size = 35
        self.color = (255, 0, 0)

        # Basic stats
        self.max_hp = 100
        self.hp = self.max_hp

        # Inventory
        self.inventory: list[ItemStack] = []
        self.inventory_max_slots = 20  # change this if you want more/fewer slots

        # Equipped items
        self.equipped_weapon: Item | None = None

    """
    Movement
    """
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

    def clamp_to_world(self, world_width, world_height):
        """
        Keep player inside the world rectangle.
        pass world size in from the game loop to avoid global constants.
        """
        half = self.size / 2
        self.x = max(half, min(world_width - half, self.x))
        self.y = max(half, min(world_height - half, self.y))

    def draw(self, screen, camera):
        """
        Draw the player using the camera to convert world->screen.
        """
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
          - an item_id string (e.g. "slime_goo")

        Returns True if everything was added, False if there's not enough space.
        """

        # If we got an item_id string instead of an Item instance, create it:
        if isinstance(item, str):
            item = create_item(item)

        # If it's stackable, try to add to an existing stack first
        if item.stackable:
            for stack in self.inventory:
                if stack.item.unique_id == item.unique_id and not stack.is_full():
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
        Called by the inventory UI when right-click or press Enter.
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
        hook this into combat system later.
        """
        weapon_damage = self.equipped_weapon.damage if self.equipped_weapon else 0
        return base_damage + weapon_damage
