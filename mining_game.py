import streamlit as st
import time

# Initialize game state (Streamlit uses 'session_state' to remember variables)
if 'rocks' not in st.session_state:
    st.session_state.rocks = 0
    st.session_state.auto_miners = 0
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
    st.session_state.rocks += amount
    st.rerun()  # Refresh the UI

# Upgrades section
st.subheader("Upgrades")
for upgrade, cost in UPGRADE_COSTS.items():
    col1, col2 = st.columns([3, 1])
    with col1:
        # Show upgrade button if not purchased
        if not st.session_state.upgrade_active[upgrade]:
            if st.button(
                f"Buy {upgrade} ({cost} rocks)",
                disabled=(st.session_state.rocks < cost),
                type="primary" if st.session_state.rocks >= cost else "secondary"
            ):
                st.session_state.rocks -= cost
                st.session_state.upgrade_active[upgrade] = True
                if upgrade == "Auto Miner":
                    st.session_state.auto_miners += 1
                st.success(f"Purchased {upgrade}!")
                st.rerun()

                st.session_state.rocks -= cost
                st.session_state.upgrade_active[upgrade] = True
                if upgrade == "Ruby Blaster":
                    st.session_state.ruby_blasters += 1
                st.success(f"Purchased {upgrade}!")
                st.rerun()
                
    with col2:
        if st.session_state.upgrade_active[upgrade]:
            st.success("✔️ Owned")

# Auto-miner logic (runs every second)
if st.session_state.upgrade_active["Auto Miner"]:
    time.sleep(1)  # Wait 1 second
    st.session_state.rocks += st.session_state.auto_miners
    st.rerun()
    
if st.session_state.upgrade_active["Ruby Blaster"]:
    time.sleep(0.1)  # Wait 1 second
    st.session_state.rocks += st.session_state.ruby_blasters
    st.rerun()
