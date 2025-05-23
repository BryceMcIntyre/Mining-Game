from streamlit.components.v1 import html
import streamlit as st
import time

st.set_page_config(layout="centered")  # Stabilizes layout
html("<style>#root { overflow-anchor: none; }</style>")  # Prevents jump

# Initialize game state
if 'game_initialized' not in st.session_state:
    st.session_state.rocks = 0
    st.session_state.upgrade_levels = {
        "Auto Miner": 0,
        "Super Pickaxe": 0,
        "Diamond Drill": 0,
        "Emerald Drill": 0,
        "Ruby Blaster": 0,
    }
    st.session_state.game_initialized = True

# Base costs
BASE_COSTS = {
    "Auto Miner": 10,
    "Super Pickaxe": 50,
    "Diamond Drill": 100,
    "Emerald Drill": 1000,
    "Ruby Blaster": 3000
}

def calculate_cost(upgrade):
    return int(BASE_COSTS[upgrade] * (1.5 ** st.session_state.upgrade_levels[upgrade]))

# --- UI Layout ---
st.title("⛏️ The Mindless Miner")

# Display rocks
st.header(f"Rocks: {st.session_state.rocks}") 

# Mining button
if st.button("⛏️ Mine", key="mine"):
    amount = 1 + (
        st.session_state.upgrade_levels["Super Pickaxe"] * 1 +
        st.session_state.upgrade_levels["Diamond Drill"] * 2 +
        st.session_state.upgrade_levels["Emerald Drill"] * 5 +
        st.session_state.upgrade_levels["Ruby Blaster"] * 10
    )
    st.session_state.rocks += amount
    st.toast(f"+{amount} rocks!")  # Nice visual feedback

# Upgrades section
for upgrade in BASE_COSTS.keys():
    cost = calculate_cost(upgrade)
    current_level = st.session_state.upgrade_levels[upgrade]  # Get current level
    
    col1, col2 = st.columns([3, 1])
    with col1:
        disabled = st.session_state.rocks < cost
        if st.button(
            f"{upgrade} (Lv {current_level+1}) - {cost} rocks",  # Use current_level here
            disabled=disabled,
            key=f"buy_{upgrade}"
        ):
            st.session_state.rocks -= cost
            st.session_state.upgrade_levels[upgrade] += 1
            st.rerun()
    
    with col2:
        if current_level > 0:
            st.success(f"Lv {current_level}")

# Auto-mining
if st.session_state.upgrade_levels["Auto Miner"] > 0:
    time.sleep(1)
    st.session_state.rocks += st.session_state.upgrade_levels["Auto Miner"]
    st.experimental_rerun()  # Smoother refresh

# Update display every interaction
rocks_display.header(f"Rocks: {st.session_state.rocks}")
