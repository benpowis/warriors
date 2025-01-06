import streamlit as st
from utils import Warrior, init_session, warrior_profile

def create_warrior(name, build_type):
    st.session_state.warrior = Warrior(name, build_type)

init_session()

if st.session_state.warrior is None:
    with st.form("character_creation"):
        st.subheader("Create your warrior")
        st.write("Welcome to the world of Warriors! Choose your warrior's name and class to begin your adventure.")
        name = st.text_input("Enter your warrior's name")
        build_type = st.selectbox("Choose your warrior class", ["Barbarian", "Rogue", "Knight"])
        submitted = st.form_submit_button("Create Warrior")
        
        if submitted and name:
            create_warrior(name, build_type)
            st.rerun()

else: 
    warrior = st.session_state.warrior
    st.subheader(f"Welcome to the world of warriors {warrior.name}!")
    st.markdown("*The cool morning breeze hits your face, you slowly open your eyes to find yourself standing in the centre of a small vilage.*")
    st.image("images/town.png", use_container_width=True)

    with st.sidebar:
        warrior_profile()