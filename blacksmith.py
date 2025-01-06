import streamlit as st
from utils import warrior_profile, ItemType
import random

def calculate_upgrade_cost(item):
    """Calculate the cost to upgrade an item based on its current value and type"""
    base_cost = item.cost * 0.5  # 50% of item's value as base cost
    
    # Get current upgrade level (if any)
    current_level = getattr(item, 'upgrade_level', 0)
    
    # Cost increases exponentially with upgrade level
    level_multiplier = 1.5 ** current_level
    
    # Different item types have different base costs
    type_multiplier = {
        ItemType.WEAPON: 1.2,  # Weapons cost more to upgrade
        ItemType.ARMOR: 1.0,   # Standard cost for armor
        ItemType.ACCESSORY: 0.8 # Accessories are cheaper to upgrade
    }.get(item.item_type, 1.0)
    
    return int(base_cost * level_multiplier * type_multiplier)

def calculate_success_chance(item):
    """Calculate the chance of a successful upgrade"""
    current_level = getattr(item, 'upgrade_level', 0)
    
    # Base chance starts high and decreases with each level
    base_chance = 0.95 - (current_level * 0.1)  # -10% per level
    
    # Quality affects success chance
    quality_bonus = {
        "Poor": -0.1,
        "Crude": -0.05,
        "Common": 0,
        "Standard": 0,
        "Good": 0.05,
        "Fine": 0.1,
        "Masterwork": 0.15
    }.get(getattr(item, 'quality', 'Standard'), 0)
    
    # Calculate final chance
    success_chance = base_chance + quality_bonus
    
    # Clamp between 5% and 95%
    return max(0.05, min(0.95, success_chance))

def attempt_upgrade(item, warrior):
    """Attempt to upgrade an item"""
    upgrade_cost = calculate_upgrade_cost(item)
    success_chance = calculate_success_chance(item)
    
    # Initialize upgrade level if not present
    if not hasattr(item, 'upgrade_level'):
        item.upgrade_level = 0
    
    # Return if not enough gold
    if warrior.gold < upgrade_cost:
        return False, f"Not enough gold! Need {upgrade_cost} gold."
    
    # Deduct gold
    warrior.gold -= upgrade_cost
    
    # Roll for success
    if random.random() < success_chance:
        # Success!
        item.upgrade_level += 1
        item.effect_value += 2  # Base stat increase
        
        # Update name to show upgrade level
        if not item.name.endswith(f"+{item.upgrade_level}"):
            if "+" in item.name:
                item.name = item.name.split("+")[0].strip() + f"+{item.upgrade_level}"
            else:
                item.name = f"{item.name} +{item.upgrade_level}"
        
        return True, f"Success! {item.name} was upgraded!"
    else:
        # Failure
        failure_roll = random.random()
        if failure_roll < 0.1 and item.upgrade_level > 0:  # 10% chance to lose a level
            item.upgrade_level -= 1
            item.effect_value -= 2
            return False, f"The upgrade failed and {item.name} lost a level!"
        elif failure_roll < 0.02:  # 2% chance to break
            warrior.inventory.remove(item)
            return False, f"Oh no! {item.name} was destroyed in the upgrade attempt!"
        else:
            return False, f"The upgrade failed but {item.name} is safe."

# Remove form borders
st.markdown("""
    <style>
        div[data-testid="stForm"] {
            border: none;
            padding: 0;
        }
    </style>
    """, unsafe_allow_html=True)

if st.session_state.warrior:
    warrior = st.session_state.warrior
    
    with st.sidebar:
        warrior_profile()
    
    messages = [
        "*The sound of hammering echoes through the smithy as you enter...*",
        "*Heat radiates from the forge as the blacksmith looks up from their work...*",
        "*The blacksmith wipes their brow and nods in greeting...*",
        "*Sparks fly from the anvil as you approach the master blacksmith...*"
    ]
    st.markdown(random.choice(messages))
    
    left, right = st.columns([2, 1])
    
    with left:
        # Only show upgradeable items
        upgradeable_items = [
            item for item in warrior.inventory 
            if item.item_type in [ItemType.WEAPON, ItemType.ARMOR, ItemType.ACCESSORY]
        ]
        
        if not upgradeable_items:
            st.warning("You don't have any equipment that can be upgraded!")
        else:
            st.subheader("💪 Upgrade Equipment")
            
            for idx, item in enumerate(upgradeable_items):
                upgrade_cost = calculate_upgrade_cost(item)
                success_chance = calculate_success_chance(item)
                
                with st.form(key=f"upgrade_form_{idx}"):
                    cols = st.columns([3, 2, 2])
                    with cols[0]:
                        st.write(f"{item.icon} {item.name}")
                        if hasattr(item, 'description'):
                            st.caption(item.description)
                        current_level = getattr(item, 'upgrade_level', 0)
                        st.write(f"Current level: +{current_level}")
                    
                    with cols[1]:
                        st.write(f"Upgrade cost: {upgrade_cost} gold")
                        st.write(f"Success chance: {int(success_chance * 100)}%")
                    
                    with cols[2]:
                        if st.form_submit_button("Upgrade"):
                            success, message = attempt_upgrade(item, warrior)
                            if success:
                                st.success(message)
                                warrior.update_stats()  # Update warrior's stats
                            else:
                                st.error(message)
                                if "destroyed" in message:
                                    st.rerun()  # Refresh if item was destroyed
        
        # Display some lore/tips
        with st.expander("Blacksmith's Tips"):
            st.markdown("""
            * Higher quality items have better upgrade success rates
            * Each upgrade becomes more expensive and risky
            * Failed upgrades might damage or destroy your equipment
            * Items can be upgraded multiple times, but the risk increases
            * Some special items might have different upgrade properties
            """)

    with right:
        st.image("images/blacksmith_side.png", use_container_width=True)
else:
    st.error("You need to create a warrior first!")
    st.warning("Go back to the character creation page and create your warrior.")