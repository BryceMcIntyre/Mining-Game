import streamlit as st
import time

# Initialize game state
if 'rocks' not in st.session_state:
    st.session_state.rocks = 0
    st.session_state.auto_miners = 0
    st.session_state.ruby_blasters = 0
    st.session_state.upgrade_levels = {  # Track how many times each upgrade was bought
        "Auto Miner": 0,
        "Super Pickaxe": 0,
        "Diamond Drill": 0,
        "Emerald Drill": 0,
        "Ruby Blaster": 0,
    }
    st.session_state.upgrade_active = {  # Track if at least one of each is owned
        "Auto Miner": False,
        "Super Pickaxe": False,
        "Diamond Drill": False,
        "Emerald Drill": False,
        "Ruby Blaster": False,
    }

# Base upgrade costs
BASE_UPGRADE_COSTS = {
    "Auto Miner": 10,
    "Super Pickaxe": 50,
    "Diamond Drill": 100,
    "Emerald Drill": 1000,
    "Ruby Blaster": 3000
}

def calculate_upgrade_cost(upgrade_name):
    """Calculate current cost with 1.5x multiplier per level"""
    base_cost = BASE_UPGRADE_COSTS[upgrade_name]
    level = st.session_state.upgrade_levels[upgrade_name]
    return int(base_cost * (1.5 ** level))

# --- Streamlit UI ---
st.title("For those who yearn for the mines:")

# Display rocks at the top
st.header(f"Rocks: {st.session_state.rocks}")

# Mine button
if st.button("⛏️ Mine Rock", key="mine"):
    amount = 1
    if st.session_state.upgrade_active["Super Pickaxe"]:
        amount += 1 * st.session_state.upgrade_levels["Super Pickaxe"]
    if st.session_state.upgrade_active["Diamond Drill"]:
        amount += 3 * st.session_state.upgrade_levels["Diamond Drill"]
    if st.session_state.upgrade_active["Emerald Drill"]:
        amount += 15 * st.session_state.upgrade_levels["Emerald Drill"]
    if st.session_state.upgrade_active["Ruby Blaster"]:
        amount += 50 * st.session_state.upgrade_levels["Ruby Blaster"]
    st.session_state.rocks += amount
    st.rerun()

# Upgrades section
st.subheader("Upgrades")
for upgrade in BASE_UPGRADE_COSTS.keys():
    current_level = st.session_state.upgrade_levels[upgrade]
    current_cost = calculate_upgrade_cost(upgrade)
    
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        if st.button(
            f"Buy {upgrade} (Lv {current_level + 1}) - {current_cost} rocks",
            disabled=(st.session_state.rocks < current_cost),
            type="primary" if st.session_state.rocks >= current_cost else "secondary",
            key=f"buy_{upgrade}"
        ):
            st.session_state.rocks -= current_cost
            st.session_state.upgrade_levels[upgrade] += 1
            st.session_state.upgrade_active[upgrade] = True
            
            # Special effects for certain upgrades
            if upgrade == "Auto Miner":
                st.session_state.auto_miners += 1
            elif upgrade == "Ruby Blaster":
                st.session_state.ruby_blasters += 1
                
            st.rerun()
    
    with col2:
        if st.session_state.upgrade_levels[upgrade] > 0:
            st.success(f"Lv {current_level}")
    
    with col3:
        if st.session_state.upgrade_levels[upgrade] > 0:
            st.success("✔️")

# Auto-mining logic
if st.session_state.upgrade_active["Auto Miner"]:
    time.sleep(1)
    st.session_state.rocks += st.session_state.auto_miners * st.session_state.upgrade_levels["Auto Miner"]
    st.rerun()
    
if st.session_state.upgrade_active["Ruby Blaster"]:
    time.sleep(0.1)
    st.session_state.rocks += st.session_state.ruby_blasters * st.session_state.upgrade_levels["Ruby Blaster"] * 10
    st.rerun()
