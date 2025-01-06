# encounters.py
import streamlit as st
import random
from utils import area, Item, Enemy, Buff, ItemType

def calculate_damage(attacker_strength, defender_armor):
    """Calculate damage considering strength and armor"""
    base_damage = random.randint(3, 8) + attacker_strength
    damage_reduction = min(0.75, defender_armor / 100)  # Cap damage reduction at 75%
    reduced_amount = int(base_damage * damage_reduction)
    final_damage = max(1, base_damage - reduced_amount)
    return final_damage, reduced_amount, base_damage

def calculate_critical_chance(luck):
    """Calculate critical hit chance based on luck"""
    base_crit_chance = 0.05  # 5% base chance
    luck_bonus = luck / 200  # Each point of luck adds 0.5% crit chance
    return min(0.25, base_crit_chance + luck_bonus)  # Cap at 25% chance

def dodge_attack(luck, attacker_strength=0):
    """
    Calculate dodge chance based on luck and attacker's strength
    
    Args:
        luck (int): The defender's luck stat
        attacker_strength (int, optional): The attacker's strength stat. Defaults to 0.
    
    Returns:
        bool: True if dodge successful, False otherwise
    """
    base_dodge = min(0.3, luck / 150)  # Base dodge chance from luck, capped at 30%
    strength_penalty = attacker_strength / 300  # Strong attacks are harder to dodge
    final_dodge_chance = max(0.05, base_dodge - strength_penalty)  # Minimum 5% dodge chance
    return random.random() < final_dodge_chance

def generate_encounter():
    """Generate a random encounter type"""
    encounters = [
        {"type": "enemy", "weight": 60},
        {"type": "chest", "weight": 25},
        {"type": "blessing", "weight": 10},
        {"type": "trap", "weight": 5}
    ]
    
    total_weight = sum(e["weight"] for e in encounters)
    roll = random.randint(1, total_weight)
    
    current_weight = 0
    for encounter in encounters:
        current_weight += encounter["weight"]
        if roll <= current_weight:
            return encounter["type"]
        
def get_weapon(area, difficulty):
    """Get area and difficulty appropriate weapon with random stat variation"""
    multiplier = {"easy": 1, "medium": 1.5, "hard": 2}
    
    if area == "forest":
        weapons = [
            {
                "name": "Wooden Sword",
                "cost": 50,
                "base_effect": 2,
                "variance": 1,  # Can vary by ±1
                "difficulty": "easy"
            },
            {
                "name": "Iron Sword",
                "cost": 100,
                "base_effect": 4,
                "variance": 2,  # Can vary by ±2
                "difficulty": "easy"
            },
            {
                "name": "Steel Sword",
                "cost": 200,
                "base_effect": 6,
                "variance": 3,  # Can vary by ±3
                "difficulty": "medium"
            },
            {
                "name": "Enchanted Blade",
                "cost": 400,
                "base_effect": 8,
                "variance": 4,  # Can vary by ±4
                "difficulty": "medium"
            },
            {
                "name": "Ancient Elven Sword",
                "cost": 800,
                "base_effect": 12,
                "variance": 5,  # Can vary by ±5
                "difficulty": "hard"
            }
        ]
    elif area == "mountain":
        weapons = [
            {
                "name": "Stone Axe",
                "cost": 150,
                "base_effect": 5,
                "variance": 2,
                "difficulty": "easy"
            },
            {
                "name": "Frost Blade",
                "cost": 300,
                "base_effect": 7,
                "variance": 3,
                "difficulty": "medium"
            },
            {
                "name": "Giant's Hammer",
                "cost": 600,
                "base_effect": 10,
                "variance": 4,
                "difficulty": "hard"
            }
        ]
    
    # Filter weapons by difficulty
    appropriate_weapons = [w for w in weapons if w["difficulty"] == difficulty]
    if not appropriate_weapons:
        appropriate_weapons = weapons  # Fallback to all weapons if none match
    
    weapon = random.choice(appropriate_weapons)
    
    # Add random variance to effect value
    variance = random.randint(-weapon["variance"], weapon["variance"])
    base_effect = weapon["base_effect"]
    final_effect = max(1, base_effect + variance)  # Ensure minimum of 1
    
    # Scale by difficulty multiplier
    final_effect = int(final_effect * multiplier[difficulty])
    
    # Adjust cost based on variance
    cost_modifier = 1 + (variance / weapon["variance"] / 2)  # ±50% cost based on stats
    final_cost = int(weapon["cost"] * cost_modifier * multiplier[difficulty])
    
    # Add quality prefix based on variance
    if variance > 0:
        if variance >= weapon["variance"] * 0.8:
            prefix = "Masterwork"
        elif variance >= weapon["variance"] * 0.4:
            prefix = "Fine"
        else:
            prefix = "Good"
        final_name = f"{prefix} {weapon['name']}"
    elif variance < 0:
        if variance <= -weapon["variance"] * 0.8:
            prefix = "Poor"
        elif variance <= -weapon["variance"] * 0.4:
            prefix = "Crude"
        else:
            prefix = "Common"
        final_name = f"{prefix} {weapon['name']}"
    else:
        final_name = weapon['name']

    description = (
        f"A {difficulty} weapon from the {area}\n"
        f"Quality: {prefix if variance != 0 else 'Standard'}"
    )
    
    return Item(
        name=final_name,
        cost=final_cost,
        effect_type="strength",
        effect_value=final_effect,
        icon="⚔️",
        item_type=ItemType.WEAPON,
        description=description
    )

def get_armor(area, difficulty):
    """Get area and difficulty appropriate armor with random stat variation"""
    multiplier = {"easy": 1, "medium": 1.5, "hard": 2}
    
    if area == "forest":
        armors = [
            {
                "name": "Leather Armor",
                "cost": 80,
                "base_effect": 5,
                "variance": 2,
                "difficulty": "easy"
            },
            {
                "name": "Studded Leather",
                "cost": 150,
                "base_effect": 8,
                "variance": 3,
                "difficulty": "easy"
            },
            {
                "name": "Chain Mail",
                "cost": 300,
                "base_effect": 12,
                "variance": 4,
                "difficulty": "medium"
            },
            {
                "name": "Elven Mail",
                "cost": 600,
                "base_effect": 15,
                "variance": 5,
                "difficulty": "medium"
            },
            {
                "name": "Ancient Treant Bark",
                "cost": 1000,
                "base_effect": 20,
                "variance": 6,
                "difficulty": "hard"
            }
        ]
    elif area == "mountain":
        armors = [
            {
                "name": "Fur Armor",
                "cost": 200,
                "base_effect": 10,
                "variance": 3,
                "difficulty": "easy"
            },
            {
                "name": "Ice-Forged Mail",
                "cost": 400,
                "base_effect": 15,
                "variance": 4,
                "difficulty": "medium"
            },
            {
                "name": "Frost Giant Hide",
                "cost": 800,
                "base_effect": 25,
                "variance": 6,
                "difficulty": "hard"
            }
        ]
    # Filter armors by difficulty
    appropriate_armors = [a for a in armors if a["difficulty"] == difficulty]
    if not appropriate_armors:
        appropriate_armors = armors  # Fallback to all armors if none match
    
    armor = random.choice(appropriate_armors)
    varied_stats = apply_quality_variance(armor, difficulty)
    
    return Item(
        name=varied_stats["name"],
        cost=varied_stats["cost"],
        effect_type="armour",
        effect_value=varied_stats["effect_value"],
        icon="🛡️",
        item_type=ItemType.ARMOR,
        description=f"A {difficulty} armor from the {area}\nQuality: {varied_stats['quality']}"
    )

def get_accessory(area, difficulty):
    """Get area and difficulty appropriate accessory with random stat variation"""
    multiplier = {"easy": 1, "medium": 1.5, "hard": 2}
    
    if area == "forest":
        accessories = [
            # Luck-based accessories
            {
                "name": "Lucky Charm",
                "cost": 100,
                "base_effect": 3,
                "variance": 1,
                "effect_type": "luck",
                "difficulty": "easy"
            },
            {
                "name": "Forest Talisman",
                "cost": 400,
                "base_effect": 5,
                "variance": 2,
                "effect_type": "luck",
                "difficulty": "medium"
            },
            # Strength-based accessories
            {
                "name": "Warrior's Ring",
                "cost": 200,
                "base_effect": 3,
                "variance": 1,
                "effect_type": "strength",
                "difficulty": "easy"
            },
            {
                "name": "Bear Tooth Necklace",
                "cost": 500,
                "base_effect": 6,
                "variance": 2,
                "effect_type": "strength",
                "difficulty": "medium"
            },
            # Armor-based accessories
            {
                "name": "Barkskin Amulet",
                "cost": 300,
                "base_effect": 4,
                "variance": 2,
                "effect_type": "armour",
                "difficulty": "easy"
            },
            {
                "name": "Ancient Medallion",
                "cost": 600,
                "base_effect": 8,
                "variance": 3,
                "effect_type": "armour",
                "difficulty": "medium"
            },
            # Mixed high-level accessories
            {
                "name": "Dragon Heart Pendant",
                "cost": 1000,
                "base_effect": 10,
                "variance": 4,
                "effect_type": "strength",
                "difficulty": "hard"
            }
        ]
    elif area == "mountain":
        accessories = [
            {
                "name": "Frost Ring",
                "cost": 200,
                "base_effect": 5,
                "variance": 2,
                "effect_type": "luck",
                "difficulty": "easy"
            },
            {
                "name": "Giant's Belt",
                "cost": 400,
                "base_effect": 8,
                "variance": 3,
                "effect_type": "strength",
                "difficulty": "medium"
            },
            {
                "name": "Ice Heart Amulet",
                "cost": 800,
                "base_effect": 12,
                "variance": 4,
                "effect_type": "armour",
                "difficulty": "hard"
            }
        ]
    # Filter accessories by difficulty
    appropriate_accessories = [a for a in accessories if a["difficulty"] == difficulty]
    if not appropriate_accessories:
        appropriate_accessories = accessories  # Fallback to all accessories if none match
    
    accessory = random.choice(appropriate_accessories)
    varied_stats = apply_quality_variance(accessory, difficulty)
    
    return Item(
        name=varied_stats["name"],
        cost=varied_stats["cost"],
        effect_type=accessory["effect_type"],  # Keep original effect type
        effect_value=varied_stats["effect_value"],
        icon="💍",
        item_type=ItemType.ACCESSORY,
        description=f"A {difficulty} accessory from the {area}\nQuality: {varied_stats['quality']}"
    )

def apply_quality_variance(item_data, difficulty):
    """Apply quality variance to an item"""
    multiplier = {"easy": 1, "medium": 1.5, "hard": 2}
    
    # Add random variance to effect value
    variance = random.randint(-item_data["variance"], item_data["variance"])
    base_effect = item_data["base_effect"]
    final_effect = max(1, base_effect + variance)
    
    # Scale by difficulty multiplier
    final_effect = int(final_effect * multiplier[difficulty])
    
    # Adjust cost based on variance
    cost_modifier = 1 + (variance / item_data["variance"] / 2)
    final_cost = int(item_data["cost"] * cost_modifier * multiplier[difficulty])
    
    # Determine quality prefix
    if variance > 0:
        if variance >= item_data["variance"] * 0.8:
            prefix = "Masterwork"
        elif variance >= item_data["variance"] * 0.4:
            prefix = "Fine"
        else:
            prefix = "Good"
    elif variance < 0:
        if variance <= -item_data["variance"] * 0.8:
            prefix = "Poor"
        elif variance <= -item_data["variance"] * 0.4:
            prefix = "Crude"
        else:
            prefix = "Common"
    else:
        prefix = None
    
    final_name = f"{prefix} {item_data['name']}" if prefix else item_data['name']
    
    return {
        "name": final_name,
        "cost": final_cost,
        "effect_value": final_effect,
        "quality": prefix if prefix else "Standard"
    }

def handle_chest(difficulty="easy", area="forest"):
    """Handle chest discovery and loot with difficulty multipliers"""
    multiplier = {
        "easy": 1,
        "medium": 1.5,
        "hard": 2
    }
    
    if area == "forest":
        loot_table = [
            {"item": "gold", "min": 10, "max": 50, "weight": 40},
            # Consumables
            {
                "item": "health_potion",
                "name": "Leafy Health Potion",
                "cost": 30,
                "effect_type": "health",
                "effect_value": 50,
                "icon": "🧪",
                "type": ItemType.CONSUMABLE,
                "weight": 20
            },
            {
                "item": "strength_potion",
                "name": "Oak Strength Potion",
                "cost": 50,
                "effect_type": "strength",
                "effect_value": 2,
                "icon": "💪",
                "type": ItemType.CONSUMABLE,
                "weight": 15
            },
            # Equipment
            {"item": "weapon", "weight": 10},
            {"item": "armor", "weight": 10},
            {"item": "accessory", "weight": 5}
        ]
    elif area == "mountain":
        loot_table = [
            {"item": "gold", "min": 30, "max": 100, "weight": 40},
            # Mountain Consumables
            {
                "item": "mountain_brew",
                "name": "Mountain Brew",
                "cost": 60,
                "effect_type": "health",
                "effect_value": 80,
                "icon": "🧪",
                "type": ItemType.CONSUMABLE,
                "weight": 20
            },
            {
                "item": "giant_strength",
                "name": "Giant's Strength Potion",
                "cost": 80,
                "effect_type": "strength",
                "effect_value": 4,
                "icon": "💪",
                "type": ItemType.CONSUMABLE,
                "weight": 15
            },
            # Equipment
            {"item": "weapon", "weight": 10},
            {"item": "armor", "weight": 10},
            {"item": "accessory", "weight": 5}
        ]
    
    total_weight = sum(item["weight"] for item in loot_table)
    roll = random.randint(1, total_weight)
    
    current_weight = 0
    for loot in loot_table:
        current_weight += loot["weight"]
        if roll <= current_weight:
            if loot["item"] == "gold":
                gold_amount = int(random.randint(loot["min"], loot["max"]) * multiplier[difficulty])
                st.session_state.warrior.gold += gold_amount
                return f"💰 Found {gold_amount} gold!"
                
            elif loot["item"] in ["health_potion", "strength_potion", "mountain_brew", "giant_strength"]:
                effect_value = int(loot["effect_value"] * multiplier[difficulty])
                item = Item(
                    name=loot["name"],
                    cost=loot["cost"],
                    effect_type=loot["effect_type"],
                    effect_value=effect_value,
                    icon=loot["icon"],
                    item_type=ItemType.CONSUMABLE
                )
                st.session_state.warrior.inventory.append(item)
                return f"{item.icon} Found a {item.name}!"
                
            elif loot["item"] == "weapon":
                weapon = get_weapon(area, difficulty)  # This already has correct ItemType.WEAPON
                st.session_state.warrior.inventory.append(weapon)
                return f"{weapon.icon} Found a {weapon.name}!"
                
            elif loot["item"] == "armor":
                armor = get_armor(area, difficulty)  # This already has correct ItemType.ARMOR
                st.session_state.warrior.inventory.append(armor)
                return f"{armor.icon} Found {armor.name}!"
                
            elif loot["item"] == "accessory":
                accessory = get_accessory(area, difficulty)  # This already has correct ItemType.ACCESSORY
                st.session_state.warrior.inventory.append(accessory)
                return f"{accessory.icon} Found a {accessory.name}!"

def handle_blessing(area="forest"):
    """Handle divine blessing encounters with area-specific effects"""
    if area == "forest":
        blessings = [
            {
                "name": "Divine Healing",
                "type": "heal",
                "value": 30,
                "duration": None,  # Instant effect
                "text": ":sparkling_heart: A spirit of the forest shines a divine light and heals your wounds",
                "icon": ":sparkling_heart:"
            },
            {
                "name": "Warrior's Blessing",
                "type": "strength",
                "value": 3,
                "duration": 5,  # Lasts 5 combat rounds
                "text": ":muscle: A tree ent fills your body with renewed strength, you feel temporarily stronger",
                "icon": ":muscle:"
            },
            {
                "name": "Fortune's Favor",
                "type": "luck",
                "value": 4,
                "duration": 3,  # Lasts 3 combat rounds
                "text": ":four_leaf_clover: Fortune smiles upon you",
                "icon": ":four_leaf_clover:"
            }
        ]
    elif area == "mountain":
        blessings = [
            {
                "name": "Mountain's Strength",
                "type": "heal",
                "value": 50,  # Stronger healing in mountains
                "duration": None,
                "text": ":material/mountain: The mountain's ancient power restores you",
                "icon": ":material/heart-plus:"
            },
            {
                "name": "Giant's Might",
                "type": "strength",
                "value": 5,
                "duration": 3,
                "text": ":material/arm-flex: The spirit of the mountain giants fills you",
                "icon": ":material/arm-flex:"
            },
            {
                "name": "Ice Shield",
                "type": "armour",
                "value": 8,
                "duration": 4,
                "text": ":material/snowflake: A shield of ice forms around you",
                "icon": ":material/shield:"
            }
        ]
    
    blessing = random.choice(blessings)
    warrior = st.session_state.warrior
    
    if blessing["type"] == "heal":
        # Instant healing effect
        warrior.health = min(warrior.max_health, warrior.health + blessing["value"])
        return f"{blessing['text']} (+{blessing['value']} health)"
    else:
        # Temporary buff effect
        buff = Buff(
            name=blessing["name"],
            stat=blessing["type"],
            value=blessing["value"],
            duration=blessing["duration"],
            icon=blessing["icon"]
        )
        warrior.apply_buff(buff)
        return f"{blessing['text']} (+{blessing['value']} {blessing['type']} for {blessing['duration']} rounds)"

def level_up_warrior():
    """Handle warrior level up with increased rewards for higher levels"""
    warrior = st.session_state.warrior
    warrior.level += 1
    warrior.experience = 0
    
    # Scale health gains with level
    health_gain = 10 + (warrior.level - 1) * 2
    warrior.max_health += health_gain
    warrior.base_max_health += health_gain  # Update base max health too
    warrior.health = warrior.max_health
    
    # Scale stat gains with level
    stat_gain = 3 + (warrior.level - 1) // 3  # Increase stats more every 3 levels
    
    # Only update base stats - total stats will be recalculated automatically
    if warrior.build_type == "Barbarian":
        warrior.base_strength += stat_gain
    elif warrior.build_type == "Rogue":
        warrior.base_luck += stat_gain
    elif warrior.build_type == "Knight":
        warrior.base_armour += stat_gain
    
    # Recalculate total stats based on new base stats
    warrior.update_stats()
    
    next_xp = warrior.calculate_xp_needed()
    st.session_state.combat_log.append(
        f":material/star: Level Up! You are now level {warrior.level}!\n"
        f"• Health increased by {health_gain}\n"
        f"• {warrior.build_type} bonus: +{stat_gain} to primary stat\n"
        f"• Next level requires {next_xp} XP"
    )
    st.balloons()

def handle_trap(area="forest"):
    """Handle trap encounters"""
    if area == "forest":
        traps = [
            {"damage": 10, "text": "You trigger a tripwire and take damage", "icon": ":spider_web:"},
            {"damage": 15, "text": "Poisonous spores burst from a mushroom", "icon": ":mushroom:"},
            {"damage": 20, "text": "A hidden pit opens beneath your feet", "icon": ":hole:"}
        ]
    elif area == "mountain":
        traps = [
            {"damage": 15, "text": "You slip on ice and fall", "icon": ":material/snowflake:"},
            {"damage": 20, "text": "An avalanche catches you", "icon": ":material/weather-snowy-heavy:"},
            {"damage": 25, "text": "You fall into a deep crevasse", "icon": ":material/crack:"},
            {"damage": 30, "text": "Freezing winds sap your strength", "icon": ":material/weather-windy:"}
        ]
    
    trap = random.choice(traps)
    warrior = st.session_state.warrior
    warrior.health -= trap["damage"]
    
    if warrior.health <= 0:
        warrior.status = "Dead"
        return f"{trap['icon']} {trap['text']}! The trap was fatal!"
    return f"{trap['icon']} {trap['text']}! You take {trap['damage']} damage"

def handle_combat():
    """Handle combat encounters"""
    warrior = st.session_state.warrior
    enemy = st.session_state.current_enemy
    
    st.subheader(f":material/swords: Combat with {enemy.name}")
    
    # Create main layout
    info_col, image_col = st.columns([3, 2])
    
    with info_col:
        st.markdown(f"{enemy.name} emerges from the shadows!")
        st.metric("Enemy Health", enemy.health)
        st.metric("Enemy Strength", enemy.strength)
        
        # Instead of nested columns, use horizontal spacing
        st.write("")  # Add some spacing
        attack_button = st.button("Attack!", icon=":material/swords:", use_container_width=True)
        run_away_button = st.button("Run Away", icon=":material/directions_run:", use_container_width=True)
    
    with image_col:
        # Load and display enemy image
        try:
            st.image(f"images/monsters/{enemy.image}", use_container_width=True)
        except:
            st.image("images/monsters/placeholder.png", use_container_width=True)

    if attack_button:
        process_combat_round()
    elif run_away_button:
        st.session_state.combat_log.append(":material/run: You ran away from the battle!")
        st.session_state.current_enemy = None

def handle_enemy_defeat():
    """Enhanced enemy defeat with luck-based bonuses"""
    warrior = st.session_state.warrior
    enemy = st.session_state.current_enemy
    
    st.session_state.combat_log.append(f"🏆 You defeated {enemy.name}!")
    
    # Lucky loot chance
    lucky_bonus = random.random() < (warrior.luck / 150)  # Chance for bonus rewards
    
    # Calculate base rewards
    level_diff = enemy.level - warrior.level if hasattr(enemy, 'level') else 0
    xp_multiplier = 1.2 ** level_diff if level_diff > 0 else 0.8 ** abs(level_diff)
    base_xp = int(enemy.xp * xp_multiplier)
    base_gold = enemy.gold
    
    # Apply lucky bonuses
    if lucky_bonus:
        bonus_multiplier = 1.5
        xp_gained = int(base_xp * bonus_multiplier)
        gold_gained = int(base_gold * bonus_multiplier)
        st.session_state.combat_log.append("🍀 Lucky! You found extra rewards!")
    else:
        xp_gained = base_xp
        gold_gained = base_gold
    
    warrior.experience += xp_gained
    warrior.gold += gold_gained
    st.session_state.combat_log.append(
        f"💰 Gained {gold_gained} gold and {xp_gained} experience!"
    )
    
    xp_needed = warrior.calculate_xp_needed()
    st.session_state.combat_log.append(
        f"📊 Progress to next level: {warrior.experience}/{xp_needed} XP"
    )
    
    if warrior.experience >= xp_needed:
        level_up_warrior()
    
    st.session_state.current_enemy = None

def handle_warrior_defeat():
    """Handle warrior defeat"""
    st.session_state.combat_log.append(":material/skull: You have been defeated!")
    st.session_state.warrior.status = "Dead"
    st.session_state.current_enemy = None


def process_combat_round():
    """Process a single round of combat"""
    warrior = st.session_state.warrior
    enemy = st.session_state.current_enemy
    
    # Player attack phase
    if random.random() < calculate_critical_chance(warrior.luck):
        # Critical hit
        base_damage, blocked_damage, original_damage = calculate_damage(warrior.strength, enemy.armour if hasattr(enemy, 'armour') else 0)
        damage = base_damage * 2
        st.session_state.combat_log.append(f"⚡ Critical Hit! You strike {enemy.name} for {original_damage} damage!")
        if blocked_damage > 0:
            st.session_state.combat_log.append(f"🛡️ Enemy armor blocks {blocked_damage} damage!")
        st.session_state.combat_log.append(f"💥 Final damage dealt: {damage} (Critical!)")
    else:
        # Normal attack
        damage, blocked_damage, original_damage = calculate_damage(warrior.strength, enemy.armour if hasattr(enemy, 'armour') else 0)
        st.session_state.combat_log.append(f"🗡️ You strike {enemy.name} for {original_damage} damage")
        if blocked_damage > 0:
            st.session_state.combat_log.append(f"🛡️ Enemy armor blocks {blocked_damage} damage!")
        st.session_state.combat_log.append(f"💥 Final damage dealt: {damage}")
    
    enemy.health -= damage

    # Check for enemy defeat
    if enemy.health <= 0:
        handle_enemy_defeat()
        return

    # Enemy attack phase
    if dodge_attack(warrior.luck, enemy.strength):
        st.session_state.combat_log.append(f"💨 {warrior.name} gracefully dodges {enemy.name}'s attack!")
    else:
        enemy_damage, blocked_damage, original_damage = calculate_damage(enemy.strength, warrior.armour)
        warrior.health -= enemy_damage
        st.session_state.combat_log.append(f"⚔️ {enemy.name} strikes you for {original_damage} damage")
        if blocked_damage > 0:
            st.session_state.combat_log.append(f"🛡️ Your armor blocks {blocked_damage} damage!")
        st.session_state.combat_log.append(f"💥 Final damage taken: {enemy_damage}")
        
        # Counter-attack chance based on luck
        if random.random() < (warrior.luck / 200):  # 0.5% chance per luck point
            counter_damage, counter_blocked, counter_original = calculate_damage(
                warrior.strength, 
                enemy.armour if hasattr(enemy, 'armour') else 0
            )
            counter_damage = max(1, int(counter_damage * 0.5))  # Counter attacks do 50% damage
            enemy.health -= counter_damage
            st.session_state.combat_log.append(f"↪️ You counter-attack for {counter_damage} damage!")
            
            if enemy.health <= 0:
                handle_enemy_defeat()
                return

    # Check for warrior defeat
    if warrior.health <= 0:
        handle_warrior_defeat()
        return

    # Status effects and buff updates
    expired_buffs = warrior.update_buff_durations()
    for buff in expired_buffs:
        st.session_state.combat_log.append(f"{buff.icon} {buff.name} has worn off!")