import streamlit as st

### AUTHS ###

### GLOBAL PAGE ELEMENTS ###

# logo
#logo = "images/logo.png"
#st.logo(logo, size="large", link=None, icon_image=None)

# navigation
warrior = st.Page("warrior.py", title="Warrior", icon=":material/swords:", default=True)
shop = st.Page("shop.py", title="Shop", icon=":material/money_bag:")
blacksmith = st.Page("blacksmith.py", title="Blacksmith", icon=":material/hardware:")
tavern = st.Page("tavern.py", title="Tavern", icon=":material/sports_bar:")
quests = st.Page("quest_board.py", title="Quest board", icon=":material/comment_bank:")

# battle arenas
forest = st.Page("forest.py", title="Forlorn Forest", icon=":material/forest:")
mountains = st.Page("mountains.py", title="Misty Mountains", icon=":material/landscape_2:")

pg = st.navigation(
        {
            "Village": [warrior, shop, blacksmith, tavern, quests],
            "Adventure": [forest, mountains],
        }
    )

# simple navigation #
# pg = st.navigation(
#         {
#             "Explore": [homepage, create, profile, shop, forest]
#         }
#     )

# global page settings
st.set_page_config(page_title="Warriors - adventure game", page_icon="⚔", layout="wide")

st.title(":material/swords: Warriors - An adventure game")

# Check for dead warrior state
if 'warrior' in st.session_state and st.session_state.warrior is not None:
    warrior = st.session_state.warrior
    if warrior.health <= 0:  # Check actual health instead of status
        st.subheader(":material/skull: You are dead")
        st.write(f"Here lies {warrior.name}, a brave warrior who fought valiantly.")
        st.write(f"{warrior.name} made it to level {warrior.level} before meeting their fate.")
        st.write("You can create a new warrior to continue your adventure.")
        
        # Clear the dead warrior
        st.session_state.warrior = None
        
        st.stop()

pg.run()