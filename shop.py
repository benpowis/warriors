import streamlit as st
from utils import Item, warrior_profile, ItemType
import random

def calculate_sell_price(item):
    """Calculate sell price based on item type and cost"""
    if item.item_type == ItemType.CONSUMABLE:
        # Consumables sell for 50% of purchase price
        return int(item.cost * 0.5)
    else:
        # Equipment sells for 60-75% based on if it's equipped
        base_price = int(item.cost * 0.6)
        if hasattr(item, 'equipped') and item.equipped:
            # Equipped items sell for less since you need to unequip them
            return base_price
        return int(item.cost * 0.75)

def display_inventory_for_sale():
    """Display inventory with sell options"""
    warrior = st.session_state.warrior
    
    if not warrior.inventory:
        st.write("*Your inventory is empty...*")
        return
        
    st.subheader("🎒 Your Inventory")
    
    # Group items by type but store original indices
    consumables = []
    equipment = []
    
    for idx, item in enumerate(warrior.inventory):
        if item.item_type == ItemType.CONSUMABLE:
            consumables.append((idx, item))  # Store original inventory index
        else:
            equipment.append((idx, item))    # Store original inventory index
    
    # Display equipment first
    if equipment:
        st.write("⚔️ Equipment")
        for inv_idx, item in equipment:  # Use actual inventory index
            sell_price = calculate_sell_price(item)
            with st.form(key=f"sell_form_{inv_idx}"):  # Use inventory index for unique key
                cols = st.columns([3, 2, 1])
                with cols[0]:
                    if hasattr(item, 'equipped') and item.equipped:
                        st.write(f"{item.icon} {item.name} (Equipped)")
                    else:
                        st.write(f"{item.icon} {item.name}")
                    if hasattr(item, 'description') and item.description:
                        st.caption(item.description)
                with cols[1]:
                    st.write(f"Sell value: {sell_price} gold")
                with cols[2]:
                    if st.form_submit_button("Sell"):
                        if hasattr(item, 'equipped') and item.equipped:
                            warrior.unequip_item(item.item_type)
                        warrior.inventory.pop(inv_idx)  # Use actual inventory index
                        warrior.gold += sell_price
                        st.toast(f"Sold {item.name} for {sell_price} gold!")
                        st.rerun()
    
    # Then display consumables
    if consumables:
        st.write("🧪 Consumables")
        for inv_idx, item in consumables:  # Use actual inventory index
            sell_price = calculate_sell_price(item)
            with st.form(key=f"sell_form_{inv_idx}"):  # Use inventory index for unique key
                cols = st.columns([3, 2, 1])
                with cols[0]:
                    st.write(f"{item.icon} {item.name}")
                with cols[1]:
                    st.write(f"Sell value: {sell_price} gold")
                with cols[2]:
                    if st.form_submit_button("Sell"):
                        warrior.inventory.pop(inv_idx)  # Use actual inventory index
                        warrior.gold += sell_price
                        st.toast(f"Sold {item.name} for {sell_price} gold!")
                        st.rerun()

def get_weapons():
    return [
        Item("Iron Sword", 100, "strength", 5, ":material/swords:", 
             ItemType.WEAPON, "A reliable iron sword"),
        Item("Battle Axe", 150, "strength", 8, ":material/swords:", 
             ItemType.WEAPON, "A mighty battle axe"),
        Item("War Hammer", 200, "strength", 12, ":material/swords:", 
             ItemType.WEAPON, "A devastating war hammer"),
        Item("Legendary Blade", 500, "strength", 20, ":material/swords:", 
             ItemType.WEAPON, "A blade of legendary power")
    ]

def get_armor():
    return [
        Item("Leather Armor", 80, "armour", 8, ":material/shield:", 
             ItemType.ARMOR, "Basic but reliable protection"),
        Item("Chain Mail", 150, "armour", 15, ":material/shield:", 
             ItemType.ARMOR, "Flexible chain mail protection"),
        Item("Plate Armor", 300, "armour", 25, ":material/shield:", 
             ItemType.ARMOR, "Heavy but effective plate armor"),
        Item("Dragon Scale", 600, "armour", 40, ":material/shield:", 
             ItemType.ARMOR, "Legendary armor made from dragon scales")
    ]

def get_accessories():
    return [
        Item("Lucky Penny", 150, "luck", 10, ":material/paid:", 
             ItemType.ACCESSORY, "A coin that brings good fortune"),
        Item("Adventurer's Ring", 200, "luck", 5, ":material/money_bag:", 
             ItemType.ACCESSORY, "A ring worn by experienced adventurers"),
        Item("Ancient Medallion", 300, "health", 25, ":material/money_bag:", 
             ItemType.ACCESSORY, "A medallion pulsing with ancient power"),
        Item("Warrior's Pendant", 400, "strength", 8, ":material/money_bag:", 
             ItemType.ACCESSORY, "A pendant empowered with warrior spirit")
    ]

def get_potions():
    return [
        Item("Health Potion", 30, "health", 50, ":material/science:", 
             ItemType.CONSUMABLE, "Restores 50 health"),
        Item("Greater Health Potion", 80, "health", 100, ":material/science:", 
             ItemType.CONSUMABLE, "Restores 100 health"),
        Item("Strength Potion", 50, "strength", 2, ":material/science:", 
             ItemType.CONSUMABLE, "Temporarily increases strength"),
        Item("Greater Strength Potion", 100, "strength", 4, ":material/science:", 
             ItemType.CONSUMABLE, "Greatly increases strength"),
        Item("Stoneskin Potion", 35, "armour", 6, ":material/science:", 
             ItemType.CONSUMABLE, "Temporarily increases armor"),
        Item("Greater Stoneskin Potion", 55, "armour", 14, ":material/science:", 
             ItemType.CONSUMABLE, "Greatly increases armor")
    ]

def display_items(items):
    for item in items:
        with st.form(key=f"buy_form_{item.name}"):
            cols = st.columns([2, 1, 1])
            with cols[0]:
                st.write(f"{item.icon} {item.name} ({item.cost} gold)")
                if item.description:
                    st.caption(item.description)
            with cols[1]:
                if item.item_type == ItemType.CONSUMABLE:
                    effect_text = f"+{item.effect_value} {item.effect_type}"
                else:
                    effect_text = f"Equip: +{item.effect_value} {item.effect_type}"
                st.text(effect_text)
            with cols[2]:
                if st.form_submit_button("Buy"):
                    if warrior.gold >= item.cost:
                        warrior.gold -= item.cost
                        warrior.inventory.append(item)
                        st.toast(f"Bought {item.name}!")
                        st.rerun()
                    else:
                        st.toast(f"Not enough gold, {warrior.name}!", icon=":material/feedback:")

if st.session_state.warrior:
    warrior = st.session_state.warrior
   
    with st.sidebar:
        warrior_profile()

    messages = [
        f"*You enter a gloomy shop with items stacked from floor to ceiling. The shopkeeper looks up from his work and greets you with a smile.*",
        f"*You enter a gloomy shop with items stacked from floor to ceiling. Ah welcome back {warrior.name}, what can I help you with today?*",
        f"*You enter a gloomy shop with items stacked from floor to ceiling. Good day {warrior.name}, what do you need?*",
        f"*You enter a gloomy shop with items stacked from floor to ceiling. The shopkeeper is busy with his work but greets you with a nod.*",
    ]
    st.markdown(random.choice(messages))

    # Remove form borders
    st.markdown("""
        <style>
            div[data-testid="stForm"] {
                border: none;
                padding: 0;
            }
        </style>
        """, unsafe_allow_html=True)

    # Create tabs for buying and selling
    buy_tab, sell_tab = st.tabs(["💰 Buy", "💱 Sell"])
    
    with buy_tab:
        left, right = st.columns([2, 1])
        
        with left:
            # Create tabs for different categories
            weapons_tab, armor_tab, accessories_tab, potions_tab = st.tabs([
                ":material/swords: Weapons",
                ":material/shield: Armor",
                "💍 Accessories",
                "🧪 Potions"
            ])

            with weapons_tab:
                st.markdown("*The shopkeeper shows you an impressive array of weaponry...*")
                display_items(get_weapons())

            with armor_tab:
                st.markdown("*Sturdy armor of various materials lines the walls...*")
                display_items(get_armor())

            with accessories_tab:
                st.markdown("*Magical trinkets and mysterious accessories catch your eye...*")
                display_items(get_accessories())

            with potions_tab:
                st.markdown("*Colorful bottles bubble and fizz on the shelves...*")
                display_items(get_potions())

        with right:
            st.image("images/shop_side.png", use_container_width=True)
    
    with sell_tab:
        st.markdown("*The shopkeeper examines your items with a practiced eye...*")
        display_inventory_for_sale()

else:
    st.error("You need to create a warrior first in order to enter the shop.")
    st.warning("Go back to the character creation page and create your warrior.")