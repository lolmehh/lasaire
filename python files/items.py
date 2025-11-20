# items.py
import uuid

class Item:
    def __init__(
        self,
        template_id: str,     # rusty_sword, slime_goo, etc.
        unique_id: str,       # actual instance ID
        name: str,
        category: str,
        description: str = "",
        damage: int = 0,
        heal_amount: int = 0,
        value: int = 0,
        stackable: bool = True,
        max_stack: int = 99,
    ):
        self.template_id = template_id
        self.unique_id = unique_id
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

# Item definitions

ITEM_DEFS = {
    # Weapons
    "stick": {
        "name": "Stick",
        "category": "weapon",
        "description": "Something is better than nothing.",
        "damage": 2,
        "heal_amount": 0,
        "value": 1,
        "stackable": False,
        "max_stack": 1,
    },
    "rusty_sword": {
        "name": "Rusty Sword",
        "category": "weapon",
        "description": "Old, but it still hurts.",
        "damage": 5,
        "heal_amount": 0,
        "value": 10,
        "stackable": False,
        "max_stack": 1,
    },

    # Consumables
    "small_hp_potion": {
        "name": "Small health potion",
        "category": "consumable",
        "description": "Heals a little bit of health.",
        "damage": 0,
        "heal_amount": 20,
        "value": 15,
        "stackable": True,
        "max_stack": 99,
    },
    "medium_hp_potion": {
        "name": "Medium health potion",
        "category": "consumable",
        "description": "Heals a little bit more of health.",
        "damage": 0,
        "heal_amount": 80,
        "value": 30,
        "stackable": True,
        "max_stack": 99,
    },
    "large_hp_potion": {
        "name": "Large health potion",
        "category": "consumable",
        "description": "Heals a little bit more of health.",
        "damage": 0,
        "heal_amount": 200,
        "value": 60,
        "stackable": True,
        "max_stack": 99,
    },
    # Mob drops / materials
    "slime_goo": {
        "name": "Slime Goo",
        "category": "material",
        "description": "Sticky residue from a slime. ew.",
        "damage": 0,
        "heal_amount": 0,
        "value": 2,
        "stackable": True,
        "max_stack": 99,
    },
}

def generate_uid():
    return str(uuid.uuid4())


def create_item(item_id: str) -> Item:
    """
    Factory function:
      create_item("slime_goo") -> new Item instance
    """
    if item_id not in ITEM_DEFS:
        raise ValueError(f"Unknown item_id: {item_id}")

    data = ITEM_DEFS[item_id]
    return Item(
        template_id=item_id,
        unique_id=generate_uid(),
        name=data["name"],
        category=data["category"],
        description=data["description"],
        damage=data["damage"],
        heal_amount=data["heal_amount"],
        value=data["value"],
        stackable=data["stackable"],
        max_stack=data["max_stack"],
    )


