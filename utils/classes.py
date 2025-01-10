import random
import streamlit as st
from enum import Enum

class ItemType(Enum):
    CONSUMABLE = "consumable"
    WEAPON = "weapon"
    ARMOR = "armor"
    ACCESSORY = "accessory"

class Item:
    def __init__(self, name, cost, effect_type, effect_value, icon, item_type=ItemType.CONSUMABLE, description=""):
        self.name = name
        self.cost = cost
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.icon = icon
        self.item_type = item_type
        self.description = description
        self.equipped = False

class EquipmentSlots:
    def __init__(self):
        self.weapon = None
        self.armor = None
        self.accessory = None
    
    def get_total_bonuses(self):
        """Calculate total stat bonuses from all equipped items"""
        bonuses = {
            "strength": 0,
            "luck": 0,
            "armour": 0,
            "health": 0
        }
        
        for item in [self.weapon, self.armor, self.accessory]:
            if item:
                bonuses[item.effect_type] += item.effect_value
        return bonuses

class Enemy:
    def __init__(self, area):
        enemies = {
    "forest_easy": [
        {"name": "Wolf", "health": 50, "strength": 8, "armour": 3, "xp": 30, "gold": 15, "image": "wolf.png"},
        {"name": "Bandit", "health": 60, "strength": 10, "armour": 5, "xp": 40, "gold": 25, "image": "bandit.png"},
        {"name": "Wild Boar", "health": 55, "strength": 9, "armour": 6, "xp": 35, "gold": 20, "image": "boar.png"},
        {"name": "Goblin Scout", "health": 45, "strength": 7, "armour": 2, "xp": 25, "gold": 30, "image": "goblin.png"},
        {"name": "Giant Spider", "health": 40, "strength": 12, "armour": 4, "xp": 35, "gold": 18, "image": "spider.png"},
        {"name": "Forest Imp", "health": 35, "strength": 6, "armour": 1, "xp": 20, "gold": 35, "image": "imp.png"},
        {"name": "Rabid Bear", "health": 65, "strength": 11, "armour": 8, "xp": 45, "gold": 22, "image": "bear.png"},
        {"name": "Hostile Hunter", "health": 55, "strength": 9, "armour": 4, "xp": 32, "gold": 28, "image": "hunter.png"}
    ],
    "forest_medium": [
        {"name": "Troll", "health": 80, "strength": 12, "armour": 12, "xp": 50, "gold": 40, "image": "troll.png"},
        {"name": "Dark Dwarf", "health": 70, "strength": 15, "armour": 15, "xp": 45, "gold": 50, "image": "dark_dwarf.png"},
        {"name": "Forest Ogre", "health": 90, "strength": 14, "armour": 10, "xp": 55, "gold": 45, "image": "ogre.png"},
        {"name": "Werewolf", "health": 75, "strength": 16, "armour": 8, "xp": 60, "gold": 55, "image": "werewolf.png"},
        {"name": "Corrupted Ent", "health": 100, "strength": 13, "armour": 20, "xp": 58, "gold": 48, "image": "ent.png"},
        {"name": "Harpy Warrior", "health": 65, "strength": 18, "armour": 6, "xp": 52, "gold": 60, "image": "harpy.png"},
        {"name": "Dire Wolf Pack", "health": 85, "strength": 15, "armour": 7, "xp": 57, "gold": 52, "image": "dire_wolf.png"},
        {"name": "Forest Witch", "health": 60, "strength": 20, "armour": 5, "xp": 65, "gold": 70, "image": "witch.png"},
        {"name": "Shambling Mound", "health": 95, "strength": 14, "armour": 18, "xp": 54, "gold": 45, "image": "mound.png"},
        {"name": "Bandit Chief", "health": 70, "strength": 17, "armour": 14, "xp": 56, "gold": 65, "image": "bandit_chief.png"}
    ],
    "forest_hard": [
        {"name": "Dragon", "health": 100, "strength": 20, "armour": 25, "xp": 80, "gold": 100, "image": "dragon.png"},
        {"name": "Giant", "health": 120, "strength": 18, "armour": 20, "xp": 70, "gold": 80, "image": "giant.png"},
        {"name": "Ancient Treant", "health": 150, "strength": 16, "armour": 30, "xp": 85, "gold": 90, "image": "treant.png"},
        {"name": "Demon Hunter", "health": 90, "strength": 25, "armour": 18, "xp": 90, "gold": 120, "image": "demon_hunter.png"},
        {"name": "Forest Hydra", "health": 130, "strength": 22, "armour": 22, "xp": 95, "gold": 110, "image": "hydra.png"},
        {"name": "Dark Elf Champion", "health": 85, "strength": 28, "armour": 16, "xp": 100, "gold": 150, "image": "dark_elf.png"},
        {"name": "Corrupted Unicorn", "health": 110, "strength": 24, "armour": 15, "xp": 88, "gold": 130, "image": "unicorn.png"},
        {"name": "Elder Wyrm", "health": 140, "strength": 21, "armour": 28, "xp": 92, "gold": 140, "image": "wyrm.png"},
        {"name": "Shadow Giant", "health": 160, "strength": 19, "armour": 24, "xp": 87, "gold": 95, "image": "shadow_giant.png"}
    ],
    "mountain_easy": [
        {"name": "Mountain Goat", "health": 80, "strength": 12, "armour": 5, "xp": 50, "gold": 30, "image": "placeholder.png"},
        {"name": "Rock Elemental", "health": 90, "strength": 15, "armour": 15, "xp": 60, "gold": 40, "image": "placeholder.png"},
        {"name": "Snow Wolf", "health": 75, "strength": 14, "armour": 4, "xp": 45, "gold": 35, "image": "placeholder.png"},
        {"name": "Frost Imp", "health": 65, "strength": 10, "armour": 2, "xp": 40, "gold": 45, "image": "placeholder.png"},
        {"name": "Crystal Spider", "health": 70, "strength": 13, "armour": 8, "xp": 55, "gold": 38, "image": "placeholder.png"},
        {"name": "Ice Goblin", "health": 85, "strength": 11, "armour": 6, "xp": 48, "gold": 42, "image": "placeholder.png"},
        {"name": "Cave Dweller", "health": 95, "strength": 13, "armour": 10, "xp": 52, "gold": 36, "image": "placeholder.png"},
        {"name": "Mountain Bandit", "health": 88, "strength": 14, "armour": 7, "xp": 54, "gold": 48, "image": "placeholder.png"}
    ],
    "mountain_medium": [
        {"name": "Frost Giant", "health": 120, "strength": 18, "armour": 18, "xp": 80, "gold": 60, "image": "placeholder.png"},
        {"name": "Ice Troll", "health": 100, "strength": 20, "armour": 15, "xp": 75, "gold": 70, "image": "placeholder.png"},
        {"name": "Yeti", "health": 130, "strength": 22, "armour": 12, "xp": 85, "gold": 65, "image": "placeholder.png"},
        {"name": "Storm Harpy", "health": 95, "strength": 24, "armour": 8, "xp": 78, "gold": 75, "image": "placeholder.png"},
        {"name": "Frost Wyrm", "health": 140, "strength": 19, "armour": 20, "xp": 82, "gold": 68, "image": "placeholder.png"},
        {"name": "Ice Witch", "health": 90, "strength": 26, "armour": 10, "xp": 88, "gold": 85, "image": "placeholder.png"},
        {"name": "Mountain Ogre", "health": 150, "strength": 21, "armour": 16, "xp": 76, "gold": 72, "image": "placeholder.png"},
        {"name": "Avalanche Spirit", "health": 110, "strength": 23, "armour": 14, "xp": 84, "gold": 78, "image": "placeholder.png"},
        {"name": "Crystal Golem", "health": 160, "strength": 20, "armour": 25, "xp": 86, "gold": 66, "image": "placeholder.png"},
        {"name": "Ice Drake", "health": 125, "strength": 25, "armour": 22, "xp": 90, "gold": 80, "image": "placeholder.png"}
    ],
    "mountain_hard": [
        {"name": "Ancient Dragon", "health": 200, "strength": 25, "armour": 35, "xp": 120, "gold": 150, "image": "placeholder.png"},
        {"name": "Mountain Titan", "health": 180, "strength": 28, "armour": 30, "xp": 130, "gold": 160, "image": "placeholder.png"},
        {"name": "Glacier Queen", "health": 170, "strength": 30, "armour": 25, "xp": 140, "gold": 180, "image": "placeholder.png"},
        {"name": "Storm Giant King", "health": 220, "strength": 26, "armour": 32, "xp": 125, "gold": 165, "image": "placeholder.png"},
        {"name": "Elder Frost Wyrm", "health": 190, "strength": 29, "armour": 38, "xp": 135, "gold": 175, "image": "placeholder.png"},
        {"name": "Mountain Overlord", "health": 210, "strength": 27, "armour": 34, "xp": 145, "gold": 190, "image": "placeholder.png"},
        {"name": "Crystal Behemoth", "health": 230, "strength": 24, "armour": 40, "xp": 128, "gold": 155, "image": "placeholder.png"},
        {"name": "Eternal Ice Elemental", "health": 185, "strength": 31, "armour": 28, "xp": 138, "gold": 170, "image": "placeholder.png"},
        {"name": "Blizzard Demon", "health": 195, "strength": 32, "armour": 26, "xp": 150, "gold": 200, "image": "placeholder.png"},
        {"name": "Ancient Frost Giant", "health": 240, "strength": 28, "armour": 36, "xp": 142, "gold": 185, "image": "placeholder.png"},
        {"name": "Mountain Dragon Lord", "health": 250, "strength": 35, "armour": 45, "xp": 160, "gold": 250, "image": "placeholder.png"}
    ]
}
        enemy_type = random.choice(enemies[area])
        self.name = enemy_type["name"]
        self.health = enemy_type["health"]
        self.strength = enemy_type["strength"]
        self.armour = enemy_type["armour"]
        self.xp = enemy_type["xp"]
        self.gold = enemy_type["gold"]
        self.image = enemy_type["image"]

class Buff:
    def __init__(self, name, stat, value, duration, icon):
        self.name = name
        self.stat = stat  # stat to modify: 'strength', 'luck', etc.
        self.value = value
        self.duration = duration  # number of combat rounds remaining
        self.icon = icon

class Warrior:
    def __init__(self, name, build_type):
        self.name = name
        self.build_type = build_type
        self.status = "Alive"
        self.active_buffs = []
        self.level = 1
        self.experience = 0
        self.gold = 0
        self.inventory = []
        self.experience_to_level = 100
        
        # Initialize equipment slots
        self.equipment = EquipmentSlots()
        
        # Set initial stats based on build type
        if build_type == "Barbarian":
            self.health = 120
            self.max_health = 120
            self.strength = 18
            self.armour = 10
            self.luck = 8
        elif build_type == "Rogue":
            self.health = 100
            self.max_health = 100
            self.strength = 20
            self.armour = 5
            self.luck = 11
        elif build_type == "Knight":
            self.health = 120
            self.max_health = 120
            self.strength = 10
            self.armour = 18
            self.luck = 8
        else:
            self.health = 100
            self.max_health = 100
            self.strength = 8
            self.armour = 10
            self.luck = 15

        # Store base stats
        self.base_strength = self.strength
        self.base_luck = self.luck
        self.base_armour = self.armour
        self.base_max_health = self.max_health
    
    def use_item(self, item_index):
        """Use or equip an item from inventory"""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            
            # Handle equipment items
            if hasattr(item, 'item_type') and item.item_type != ItemType.CONSUMABLE:
                result = self.equip_item(item)
                st.toast(f"Equipped {item.name}!")
                return result
            
            # Handle consumable items
            if item.effect_type == "health":
                # Calculate healing amount
                current_missing_health = self.max_health - self.health
                heal_amount = min(item.effect_value, current_missing_health)
                self.health += heal_amount
                healing_message = f"🧪 Healed for {heal_amount} health"
                if heal_amount < item.effect_value:
                    healing_message += f" (Wasted {item.effect_value - heal_amount} healing)"
            elif item.effect_type == "xp":
                self.experience += item.effect_value
            elif item.name.lower().endswith("potion"):
                # Temporary buff for combat potions
                buff = Buff(
                    name=item.name,
                    stat=item.effect_type,
                    value=item.effect_value,
                    duration=5,  # Potions last 5 combat rounds
                    icon=item.icon
                )
                self.apply_buff(buff)
                self.update_stats()
                healing_message = f"Applied {item.name} buff"
            else:
                # Other consumables give permanent stat boosts
                if item.effect_type == "armour":
                    self.armour += item.effect_value
                    self.base_armour += item.effect_value
                elif item.effect_type == "luck":
                    self.luck += item.effect_value
                    self.base_luck += item.effect_value
                elif item.effect_type == "strength":
                    self.strength += item.effect_value
                    self.base_strength += item.effect_value
                healing_message = f"Used {item.name}"
            
            # Only remove consumable items
            self.inventory.pop(item_index)
            st.toast(healing_message)
            return healing_message
        
        return "Invalid item index!"
    
    def equip_item(self, item):
        """Equip an item in the appropriate slot"""
        # Store current equipped item to return to inventory if any
        current_equipped = None
        
        if item.item_type == ItemType.WEAPON:
            current_equipped = self.equipment.weapon
            self.equipment.weapon = item
        elif item.item_type == ItemType.ARMOR:
            current_equipped = self.equipment.armor
            self.equipment.armor = item
        elif item.item_type == ItemType.ACCESSORY:
            current_equipped = self.equipment.accessory
            self.equipment.accessory = item
            
        # Return old item to inventory if exists
        if current_equipped:
            current_equipped.equipped = False
            self.inventory.append(current_equipped)
            
        # Remove new item from inventory and mark as equipped
        if item in self.inventory:
            self.inventory.remove(item)
        item.equipped = True
        
        # Update stats with new equipment
        self.update_stats()
        return f"Equipped {item.name}!"
    
    def unequip_item(self, slot_type):
        """Unequip an item from a specific slot"""
        item = None
        if slot_type == ItemType.WEAPON and self.equipment.weapon:
            item = self.equipment.weapon
            self.equipment.weapon = None
        elif slot_type == ItemType.ARMOR and self.equipment.armor:
            item = self.equipment.armor
            self.equipment.armor = None
        elif slot_type == ItemType.ACCESSORY and self.equipment.accessory:
            item = self.equipment.accessory
            self.equipment.accessory = None
            
        if item:
            item.equipped = False
            self.inventory.append(item)
            self.update_stats()
            return f"Unequipped {item.name}"
        return "No item equipped in that slot"
    
    def update_stats(self):
        """Update total stats based on base stats, equipment, and buffs"""
        # Reset to base stats
        self.strength = self.base_strength
        self.luck = self.base_luck
        self.armour = self.base_armour
        self.max_health = self.base_max_health
        
        # Apply equipment bonuses
        if hasattr(self, 'equipment'):
            equipment_bonuses = self.equipment.get_total_bonuses()
            self.strength += equipment_bonuses["strength"]
            self.luck += equipment_bonuses["luck"]
            self.armour += equipment_bonuses["armour"]
            self.max_health += equipment_bonuses["health"]
        
        # Apply buffs
        for buff in self.active_buffs:
            if buff.stat == "strength":
                self.strength += buff.value
            elif buff.stat == "luck":
                self.luck += buff.value
            elif buff.stat == "armour":
                self.armour += buff.value
            elif buff.stat == "health":
                self.max_health += buff.value
        
        # Ensure health doesn't exceed new max
        self.health = min(self.health, self.max_health)
    
    def calculate_xp_needed(self):
        """Calculate XP needed for next level using exponential scaling"""
        return int(self.experience_to_level * (1.5 ** (self.level - 1)))
    
    def get_xp_progress(self):
        """Return progress as a fraction between 0 and 1"""
        progress = self.experience / self.calculate_xp_needed()
        return min(1.0, max(0.0, progress))  # Clamp between 0 and 1
    
    def apply_buff(self, buff):
        """Apply a temporary buff to the warrior"""
        self.active_buffs.append(buff)
        self.update_stats()
    
    def update_buff_durations(self):
        """Update buff durations after combat round"""
        expired_buffs = []
        for buff in self.active_buffs[:]:  # Create a copy of the list to iterate
            buff.duration -= 1
            if buff.duration <= 0:
                expired_buffs.append(buff)
                self.active_buffs.remove(buff)
        
        self.update_stats()
        return expired_buffs