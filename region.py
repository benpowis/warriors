import streamlit as st
from utils import init_session, warrior_profile, area
from encounters import generate_encounter, handle_chest, handle_blessing, handle_trap, handle_combat
import random

class Region:
    def __init__(self, config):
        self.config = config
        
    def check_requirements(self):
        if not st.session_state.warrior:
            st.error(f"You need to create a warrior first in order to enter the {self.config['name']}.")
            st.warning("Go back to the character creation page and create your warrior.")
            return False
            
        warrior = st.session_state.warrior
        if warrior.level < self.config['required_level']:
            st.error(f"The {self.config['name']} is too dangerous for inexperienced warriors!")
            st.warning(f"Reach level {self.config['required_level']} before attempting this area.")
            return False
            
        if warrior.status == "Dead":
            st.write(f"Here lies {warrior.name}, a brave warrior who fought valiantly.")
            return False
            
        return True

    def handle_area_selection(self, area_name, difficulty):
        encounter_type = generate_encounter()
        warrior = st.session_state.warrior
        
        # Use area message from config
        st.session_state.combat_log.append(self.config['area_messages'][difficulty])
        
        if encounter_type == "enemy":
            area(f"{area_name}_{difficulty}")
            return True
        elif encounter_type == "chest":
            message = handle_chest(difficulty, area_name)
            st.session_state.combat_log.append(message)
        elif encounter_type == "blessing":
            message = handle_blessing(area_name)
            st.session_state.combat_log.append(message)
        elif encounter_type == "trap":
            message = handle_trap(area_name)
            st.session_state.combat_log.append(message)
            if warrior.status == "Dead":
                return True
        
        return False

    def render(self):
        if not self.check_requirements():
            return

        with st.sidebar:
            warrior_profile()

        left, right = st.columns([2, 1])
        
        with left:
            if not st.session_state.current_enemy:
                st.markdown(random.choice(self.config['welcome_messages']))
                st.subheader("Choose an area to explore")

                area_cols = st.columns(len(self.config['areas']))
                for col, (area_name, difficulty) in zip(area_cols, self.config['areas']):
                    with col:
                        st.image(f"images/{self.config['area_image_prefix']}_{difficulty}.png", use_container_width=True)
                        if st.button(f"{area_name} ({difficulty.title()})", key=f"{self.config['name']}_{difficulty}", use_container_width=True):
                            needs_rerun = self.handle_area_selection(self.config['name'], difficulty)
                            if needs_rerun:
                                st.rerun()

            if st.session_state.current_enemy:
                handle_combat()

            if st.session_state.combat_log:
                st.subheader("Adventure Log")
                for log in reversed(st.session_state.combat_log):
                    st.write(log)

        with right:
            st.image(self.config['side_image'], use_container_width=True)