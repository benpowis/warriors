# quest_board.py
import streamlit as st
from utils import warrior_profile
from quest_config import QuestStatus, FOREST_QUESTS, MOUNTAIN_QUESTS
import random

def initialize_quests():
    """Initialize quest tracking in session state"""
    if 'quests' not in st.session_state:
        st.session_state.quests = {}
        
    # Add any new quests that aren't in session state
    all_quests = FOREST_QUESTS + MOUNTAIN_QUESTS
    for quest in all_quests:
        if quest.id not in st.session_state.quests:
            st.session_state.quests[quest.id] = quest

def display_quest_board():
    """Display the quest board interface"""
    if not st.session_state.warrior:
        st.error("You need to create a warrior first!")
        st.warning("Go back to the character creation page and create your warrior.")
        return
        
    warrior = st.session_state.warrior
    
    with st.sidebar:
        warrior_profile()
    
    messages = [
        "*You approach the weathered quest board, its surface covered in various notices and bounties...*",
        "*The quest board creaks in the wind, its ancient wood holding countless tales of adventure...*",
        "*Local villagers gather around the quest board, discussing the latest postings...*",
        "*Fresh parchment catches your eye among the older notices on the quest board...*"
    ]
    st.markdown(random.choice(messages))
    
    left, right = st.columns([2, 1])
    
    with left:
        # Create tabs for different quest categories
        available_tab, active_tab, completed_tab = st.tabs([
            "📜 Available Quests", 
            "⚔️ Active Quests", 
            "✅ Completed Quests"
        ])
        
        with available_tab:
            display_available_quests(warrior)
            
        with active_tab:
            display_active_quests(warrior)
            
        with completed_tab:
            display_completed_quests()
    
    with right:
        st.image("images/quest_board.png", use_container_width=True)

def display_available_quests(warrior):
    """Display available quests"""
    available_quests = [
        quest for quest in st.session_state.quests.values()
        if quest.status == QuestStatus.AVAILABLE and quest.check_requirements(warrior)
    ]
    
    if not available_quests:
        st.write("*No quests available at your level...*")
        return
        
    for quest in available_quests:
        with st.container():
            st.subheader(quest.title)
            st.write(quest.description)
            
            # Show requirements
            st.write("**Requirements:**")
            if quest.quest_type.value == "kill":
                for enemy, count in quest.requirements["enemies"].items():
                    st.write(f"- Defeat {count} {enemy}(s)")
            elif quest.quest_type.value == "collect":
                for item, count in quest.requirements["items"].items():
                    st.write(f"- Collect {count} {item}(s)")
            elif quest.quest_type.value == "explore":
                for area in quest.requirements["areas"]:
                    st.write(f"- Explore {area}")
            elif quest.quest_type.value == "boss":
                st.write(f"- Defeat the {quest.requirements['boss']}")
            
            # Show rewards
            st.write("**Rewards:**")
            if "gold" in quest.rewards:
                st.write(f"- {quest.rewards['gold']} gold")
            if "xp" in quest.rewards:
                st.write(f"- {quest.rewards['xp']} XP")
            if "items" in quest.rewards:
                for item in quest.rewards["items"]:
                    st.write(f"- {item}")
            
            # Accept quest button
            if st.button("Accept Quest", key=f"accept_{quest.id}"):
                quest.status = QuestStatus.ACTIVE
                quest.progress = {}  # Reset progress
                st.success(f"Accepted quest: {quest.title}")
                st.rerun()

def display_active_quests(warrior):
    """Display active quests"""
    active_quests = [
        quest for quest in st.session_state.quests.values()
        if quest.status == QuestStatus.ACTIVE
    ]
    
    if not active_quests:
        st.write("*No active quests...*")
        return
        
    for quest in active_quests:
        with st.container():
            st.subheader(quest.title)
            st.write(quest.description)
            
            # Show progress
            st.write("**Progress:**")
            st.write(quest.get_progress_text())
            
            # Abandon quest button
            if st.button("Abandon Quest", key=f"abandon_{quest.id}"):
                quest.status = QuestStatus.AVAILABLE
                quest.progress = {}
                st.warning(f"Abandoned quest: {quest.title}")
                st.rerun()

def display_completed_quests():
    """Display completed quests with reward claiming"""
    completed_quests = [
        quest for quest in st.session_state.quests.values()
        if quest.status == QuestStatus.COMPLETED
    ]
    
    if not completed_quests:
        st.write("*No completed quests...*")
        return
        
    for quest in completed_quests:
        with st.container():
            st.subheader(f"✅ {quest.title}")
            st.write(quest.description)
            
            # Show available rewards
            st.write("**Available Rewards:**")
            if "gold" in quest.rewards:
                st.write(f"- {quest.rewards['gold']} gold")
            if "xp" in quest.rewards:
                st.write(f"- {quest.rewards['xp']} XP")
            if "items" in quest.rewards:
                for item in quest.rewards["items"]:
                    st.write(f"- {item}")
            
            # Claim rewards button
            if st.button("Claim Rewards", key=f"claim_{quest.id}"):
                result = quest.claim_rewards(st.session_state.warrior)
                st.toast(result)
                st.rerun()

def display_rewarded_quests():
    """Display previously rewarded quests"""
    rewarded_quests = [
        quest for quest in st.session_state.quests.values()
        if quest.status == QuestStatus.REWARDED
    ]
    
    if rewarded_quests:
        st.write("### 📜 Quest History")
        for quest in rewarded_quests:
            with st.expander(f"✨ {quest.title}"):
                st.write(quest.description)
                st.write("*Rewards claimed*")

# Initialize quests when page loads
initialize_quests()

# display quest board when page loads:
display_quest_board()