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
    st.session_state.last_update = time.time()
    st.session_state.game_initialized = True

# Calculate time-based mining
current_time = time.time()
time_elapsed = current_time - st.session_state.last_update

if st.session_state.upgrade_levels["Auto Miner"] > 0 and time_elapsed >= 1:
    st.session_state.rocks += st.session_state.upgrade_levels["Auto Miner"] * int(time_elapsed)
    st.session_state.last_update = current_time

# Display rocks (static)
st.header(f"⛏️ Rocks: {st.session_state.rocks}")

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
    current_level = st.session_state.upgrade_levels[upgrade]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(
            f"{upgrade} (Lv {current_level+1}) - {cost} rocks",
            disabled=st.session_state.rocks < cost,
            key=f"buy_{upgrade}"
        ):
            st.session_state.rocks -= cost
            st.session_state.upgrade_levels[upgrade] += 1
    with col2:
        if current_level > 0:
            st.success(f"Lv {current_level}")
