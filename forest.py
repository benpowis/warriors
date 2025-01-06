import streamlit as st
from region import Region
from region_configs import FOREST_CONFIG
from utils import init_session

def main():
    init_session()
    forest = Region(FOREST_CONFIG)
    forest.render()

main()