import streamlit as st
from utils import Enemy, ItemType

def celebrate():
    if st.button("Party time!"):
        st.balloons()

def initialize_session():
    if 'warrior' not in st.session_state:
        st.session_state.warrior = None
    if 'current_enemy' not in st.session_state:
        st.session_state.current_enemy = None
    if 'combat_log' not in st.session_state:
        st.session_state.combat_log = []

def handle_area_selection(area):
    st.session_state.current_enemy = Enemy(area)
    st.session_state.combat_log = []

def warrior_profile():
    warrior = st.session_state.warrior
    st.header(f"Warrior: {warrior.name}")
    st.subheader(f"Level {warrior.level} {warrior.build_type}")
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Health", f"{warrior.health}/{warrior.max_health}")
        st.metric("Strength", warrior.strength)
    with col2:
        st.metric("Armour", warrior.armour)
        st.metric("Luck", warrior.luck)
    
    # XP and Gold
    xp_needed = warrior.calculate_xp_needed()
    st.progress(warrior.get_xp_progress())
    st.text(f"Experience: {warrior.experience}/{xp_needed}")
    st.metric(":material/money_bag: Gold", warrior.gold)
    
    # Equipment Section
    st.subheader("⚔️ Equipment")
    equip_col1, equip_col2, equip_col3 = st.columns(3)
    
    with equip_col1:
        st.markdown("**Weapon**")
        if warrior.equipment.weapon:
            # st.info(f"{warrior.equipment.weapon.icon} {warrior.equipment.weapon.name}\n\n" +
            #        f"+{warrior.equipment.weapon.effect_value} {warrior.equipment.weapon.effect_type}")
            st.info(f"{warrior.equipment.weapon.icon}"+ f"+{warrior.equipment.weapon.effect_value}")
            if st.button(":material/close:", key="unequip_weapon", use_container_width=True):
                warrior.unequip_item(ItemType.WEAPON)
                st.rerun()
        else:
            st.text("Empty slot")
            
    with equip_col2:
        st.markdown("**Armor**")
        if warrior.equipment.armor:
            # st.info(f"{warrior.equipment.armor.icon} {warrior.equipment.armor.name}\n\n" +
            #        f"+{warrior.equipment.armor.effect_value} {warrior.equipment.armor.effect_type}")
            st.info(f"{warrior.equipment.armor.icon}" + f"+{warrior.equipment.armor.effect_value}")
            if st.button(":material/close:", key="unequip_armour", use_container_width=True):
                warrior.unequip_item(ItemType.ARMOR)
                st.rerun()
        else:
            st.text("Empty slot")
            
    with equip_col3:
        st.markdown("**Accessory**")
        if warrior.equipment.accessory:
            # st.info(f"{warrior.equipment.accessory.icon} {warrior.equipment.accessory.name}\n\n" +
            #        f"+{warrior.equipment.accessory.effect_value} {warrior.equipment.accessory.effect_type}")
            st.info(f"{warrior.equipment.accessory.icon}" f"+{warrior.equipment.accessory.effect_value}")
            if st.button(":material/close:", key="unequip_accessory", use_container_width=True):
                warrior.unequip_item(ItemType.ACCESSORY)
                st.rerun()
        else:
            st.text("Empty slot")
    
    # Inventory Section
    st.subheader("🎒 Inventory")
    for idx, item in enumerate(warrior.inventory):
        cols = st.columns([3, 2])
        with cols[0]:
            if item.item_type != ItemType.CONSUMABLE:
                st.write(f"{item.icon} {item.name} (+{item.effect_value} {item.effect_type})")
            else:
                st.write(f"{item.icon} {item.name}")
        with cols[1]:
            if item.item_type == ItemType.CONSUMABLE:
                button_text = "Use"
            else:
                button_text = "Equip"
            if st.button(button_text, key=f"use_{idx}"):
                result = warrior.use_item(idx)
                st.toast(result)
                st.rerun()
    
    # Active Buffs Section
    if warrior.active_buffs:
        st.subheader("✨ Active Blessings")
        for buff in warrior.active_buffs:
            st.markdown(
                f"{buff.icon} {buff.name}: +{buff.value} {buff.stat} "
                f"({buff.duration} rounds remaining)"
            )