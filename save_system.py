import json
import base64
import pickle
import os
from datetime import datetime
import streamlit as st

def save_warrior(warrior):
    """Save warrior to file"""
    if not os.path.exists('saves'):
        os.makedirs('saves')
        
    warrior_data = pickle.dumps(warrior)
    encoded_data = base64.b64encode(warrior_data).decode('utf-8')
    
    with open(f"saves/{warrior.name}.json", "w") as f:
        json.dump({
            "name": warrior.name,
            "data": encoded_data,
            "date": str(datetime.now())
        }, f)

def load_warrior(filename):
    """Load warrior from file"""
    with open(f"saves/{filename}", "r") as f:
        save_data = json.load(f)
    
    warrior_data = base64.b64decode(save_data["data"])
    return pickle.loads(warrior_data)

def add_save_load_ui():
    """Add save/load buttons to sidebar"""
    st.sidebar.subheader("💾 Save/Load")
    
    if st.sidebar.button("Save Game"):
        save_warrior(st.session_state.warrior)
        st.sidebar.success("Game saved!")
    
    save_files = [f for f in os.listdir("saves") if f.endswith('.json')]
    if save_files:
        selected_save = st.sidebar.selectbox("Load Game", save_files)
        if st.sidebar.button("Load Selected Save"):
            st.session_state.warrior = load_warrior(selected_save)
            st.rerun()