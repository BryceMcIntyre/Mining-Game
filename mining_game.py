import streamlit as st
import time

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
    return int(BASE_COSTS[upgrade] * (1.5 ** st.session_state.upgrade_levels[upgrade])

# --- UI Layout ---
st.title("⛏️ The Mindless Miner")

# Display rocks
rocks_display = st.empty()  # Placeholder we'll update

# Mining button
if st.button("⛏️ Mine"):
    amount = 1
    amount += st.session_state.upgrade_levels["Super Pickaxe"] * 1
    amount += st.session_state.upgrade_levels["Diamond Drill"] * 2
    amount += st.session_state.upgrade_levels["Emerald Drill"] * 5
    amount += st.session_state.upgrade_levels["Ruby Blaster"] * 10
    st.session_state.rocks += amount

# Upgrades section
st.header("Upgrades")
for upgrade in BASE_COSTS.keys():
    cost = calculate_cost(upgrade)
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(
            f"{upgrade} (Lv {st.session_state.upgrade_levels[upgrade]+1}) - {cost} rocks",
            disabled=st.session_state.rocks < cost,
            key=f"buy_{upgrade}"
        ):
            st.session_state.rocks -= cost
            st.session_state.upgrade_levels[upgrade] += 1
            st.rerun()
    with col2:
        if st.session_state.upgrade_levels[upgrade] > 0:
            st.success(f"Lv {st.session_state.upgrade_levels[upgrade]}")

# Auto-mining
if st.session_state.upgrade_levels["Auto Miner"] > 0:
    time.sleep(1)
    st.session_state.rocks += st.session_state.upgrade_levels["Auto Miner"]
    st.rerun()

# Update display every interaction
rocks_display.header(f"Rocks: {st.session_state.rocks}")
