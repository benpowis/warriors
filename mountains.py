# mountains.py
import streamlit as st
from region import Region
from region_configs import MOUNTAIN_CONFIG
from utils import init_session

def main():
    init_session()
    mountains = Region(MOUNTAIN_CONFIG)
    mountains.render()

main()