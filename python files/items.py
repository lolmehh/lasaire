# items.py

class Item:
    def __init__(
        self,
        item_id: str,
        name: str,
        category: str,       # "weapon", "consumable", "material", etc.
        description: str = "",
        damage: int = 0,
        heal_amount: int = 0,
        value: int = 0,
        stackable: bool = True,
        max_stack: int = 99,
    ):
        self.id = item_id
        self.name = name
        self.category = category
        self.description = description
        self.damage = damage
        self.heal_amount = heal_amount
        self.value = value
        self.stackable = stackable
        self.max_stack = max_stack


class ItemStack:
    """
    One inventory slot: an item + an amount.
    """
    def __init__(self, item: Item, amount: int = 1):
        self.item = item
        self.amount = amount

    def is_full(self) -> bool:
        if not self.item.stackable:
            return self.amount >= 1
        return self.amount >= self.item.max_stack


# -------------------------------------------------------------------
# Item definitions
# -------------------------------------------------------------------

ITEM_DEFS = {
    # Weapons
    "stick": {
        "name": "Stick",
        "category": "weapon",
        "description": "A weak wooden stick. Better than nothing.",
        "damage": 2,
        "heal_amount": 0,
        "value": 1,
        "stackable": False,
        "max_stack": 1,
    },
    "rusty_sword": {
        "name": "Rusty Sword",
        "category": "weapon",
        "description": "Old and dull, but it still hurts.",
        "damage": 5,
        "heal_amount": 0,
        "value": 10,
        "stackable": False,
        "max_stack": 1,
    },

    # Consumables
    "small_potion": {
        "name": "Small Potion",
        "category": "consumable",
        "description": "Heals a little bit of HP.",
        "damage": 0,
        "heal_amount": 20,
        "value": 15,
        "stackable": True,
        "max_stack": 10,
    },

    # Mob drops / materials
    "slime_goop": {
        "name": "Slime Goop",
        "category": "material",
        "description": "Sticky residue from a slime. Yuck.",
        "damage": 0,
        "heal_amount": 0,
        "value": 2,
        "stackable": True,
        "max_stack": 99,
    },
}


def create_item(item_id: str) -> Item:
    """
    Factory function:
      create_item("slime_goop") -> new Item instance
    """
    if item_id not in ITEM_DEFS:
        raise ValueError(f"Unknown item_id: {item_id}")

    data = ITEM_DEFS[item_id]
    return Item(
        item_id=item_id,
        name=data["name"],
        category=data["category"],
        description=data["description"],
        damage=data["damage"],
        heal_amount=data["heal_amount"],
        value=data["value"],
        stackable=data["stackable"],
        max_stack=data["max_stack"],
    )
