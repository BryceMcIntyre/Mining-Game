import streamlit as st
import time
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize game state
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")  # Download from Firebase console
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Save/Load scores
def update_leaderboard(name, score):
    db.collection("scores").document(name).set({"score": score})

def get_leaderboard():
    return pd.DataFrame([doc.to_dict() for doc in db.collection("scores").stream()])

# UI
name = st.text_input("Your name")
if st.button("Submit score"):
    update_leaderboard(name, st.session_state.rocks)
st.write("Leaderboard:", get_leaderboard().sort_values("score", ascending=False))

#actually starting the game
if 'rocks' not in st.session_state:
    st.session_state.rocks = 0
    st.session_state.upgrade_levels = {
        "Auto Miner": 0,
        "Super Pickaxe": 0,
        "Diamond Drill": 0,
        "Emerald Drill": 0,
        "Ruby Blaster": 0,
    }

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

# --- UI ---
st.title("The Mindless Miner")

# Mining
if st.button("⛏️ Mine"):
    amount = 1
    amount += st.session_state.upgrade_levels["Super Pickaxe"] * 1
    amount += st.session_state.upgrade_levels["Diamond Drill"] * 2
    amount += st.session_state.upgrade_levels["Emerald Drill"] * 5
    amount += st.session_state.upgrade_levels["Ruby Blaster"] * 10
    st.session_state.rocks += amount

# Upgrades
for upgrade in BASE_COSTS.keys():
    cost = calculate_cost(upgrade)
    if st.button(
        f"{upgrade} (Lv {st.session_state.upgrade_levels[upgrade]+1}) - {cost} rocks",
        disabled=st.session_state.rocks < cost
    ):
        st.session_state.rocks -= cost
        st.session_state.upgrade_levels[upgrade] += 1

# Auto-mining
if st.session_state.upgrade_levels["Auto Miner"] > 0:
    time.sleep(1)
    st.session_state.rocks += st.session_state.upgrade_levels["Auto Miner"] * 1
    st.rerun()
