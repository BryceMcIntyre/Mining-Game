# At the top
import json

# On startup
if 'loaded' not in st.session_state:
    try:
        with open('save.json') as f:
            data = json.load(f)
            st.session_state.update(data)
    except FileNotFoundError:
        pass

# When rocks change
if st.session_state.rocks % 10 == 0:  # Auto-save every 10 rocks
    with open('save.json', 'w') as f:
        json.dump({
            'rocks': st.session_state.rocks,
            'upgrade_active': st.session_state.upgrade_active
        }, f)



import streamlit as st
import time

# Initialize game state 
if 'rocks' not in st.session_state:
    st.session_state.rocks = 0
    st.session_state.auto_miners = 0
    st.session_state.ruby_blasters = 0  # NEW: Added this counter
    st.session_state.upgrade_active = {
        "Auto Miner": False,
        "Super Pickaxe": False,
        "Diamond Drill": False,
        "Emerald Drill": False,
        "Ruby Blaster": False,
    }

# Upgrade costs
UPGRADE_COSTS = {
    "Auto Miner": 10,
    "Super Pickaxe": 50,
    "Diamond Drill": 100,
    "Emerald Drill": 1000,
    "Ruby Blaster": 3000
}

# --- Streamlit UI ---
st.title("For those who yearn for the mines:")

# Display rocks at the top
st.header(f"Rocks: {st.session_state.rocks}")

# Mine button
if st.button("⛏️ Mine Rock", key="mine"):
    amount = 1
    if st.session_state.upgrade_active["Super Pickaxe"]:
        amount += 1
    if st.session_state.upgrade_active["Diamond Drill"]:
        amount += 3
    if st.session_state.upgrade_active["Emerald Drill"]:
        amount += 15
    if st.session_state.upgrade_active["Ruby Blaster"]:  # NEW: Added this bonus
        amount += 50
    st.session_state.rocks += amount
    st.rerun()

# Upgrades section
st.subheader("Upgrades")
for upgrade, cost in UPGRADE_COSTS.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        if not st.session_state.upgrade_active[upgrade]:
            if st.button(
                f"Buy {upgrade} ({cost} rocks)",
                disabled=(st.session_state.rocks < cost),
                type="primary" if st.session_state.rocks >= cost else "secondary"
            ):
                st.session_state.rocks -= cost
                st.session_state.upgrade_active[upgrade] = True
                # Handle special upgrades
                if upgrade == "Auto Miner":
                    st.session_state.auto_miners += 1
                elif upgrade == "Ruby Blaster":  # NEW: Added this handler
                    st.session_state.ruby_blasters += 1
                st.success(f"Purchased {upgrade}!")
                st.rerun()
    with col2:
        if st.session_state.upgrade_active[upgrade]:
            st.success("✔️ Owned")

# Combined auto-mining logic (NEW: More efficient)
if st.session_state.upgrade_active["Auto Miner"] or st.session_state.upgrade_active["Ruby Blaster"]:
    time.sleep(0.5)  # Single timer
    if st.session_state.upgrade_active["Auto Miner"]:
        st.session_state.rocks += st.session_state.auto_miners
    if st.session_state.upgrade_active["Ruby Blaster"]:
        st.session_state.rocks += st.session_state.ruby_blasters * 10  # Ruby gives 10x boost!
    st.rerun()
