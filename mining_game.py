import streamlit as st
import time
import pandas as pd
import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_admin.exceptions import FirebaseError

# Initialize Firebase (with error handling)
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("firebase-key.json")  # Your downloaded file
        firebase_admin.initialize_app(cred)
        st.success("Connected to Firebase!")
    except FileNotFoundError:
        st.error("Firebase key file missing! Download it from Firebase Console")
    except FirebaseError as e:
        st.error(f"Firebase error: {e}")

# Leaderboard functions
def update_leaderboard(name, score):
    try:
        db = firestore.client()
        db.collection("scores").document(name).set({
            "score": score,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        st.error(f"Failed to save: {e}")

def get_leaderboard():
    try:
        db = firestore.client()
        docs = db.collection("scores").order_by("score", direction=firestore.Query.DESCENDING).limit(10).stream()
        return pd.DataFrame([{"Name": doc.id, "Score": doc.to_dict()["score"]} for doc in docs])
    except Exception as e:
        st.error(f"Failed to load leaderboard: {e}")
        return pd.DataFrame()

# UI
st.title("⛏️ Mining Leaderboard")
name = st.text_input("Your name")
if st.button("Submit your score"):
    if name:
        update_leaderboard(name, st.session_state.rocks)
    else:
        st.warning("Enter a name first!")

st.write("## Top Miners")
leaderboard = get_leaderboard()
if not leaderboard.empty:
    st.dataframe(leaderboard, hide_index=True)
else:
    st.info("No scores yet. Be the first!")

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
