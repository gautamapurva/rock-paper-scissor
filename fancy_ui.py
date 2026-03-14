# professional_ui.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import time

# -----------------------------
# Page Config and CSS
# -----------------------------
st.set_page_config(page_title="🎮 Rock-Paper-Scissors AI", layout="wide")
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f9f9f9, #e0f7fa);
}
h1 {
    color: #ff6f61;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🎮✊🤚✌ Rock-Paper-Scissors AI Game")

# -----------------------------
# Initialize Session State
# -----------------------------
if 'history' not in st.session_state:
    st.session_state.history = []
if 'results' not in st.session_state:
    st.session_state.results = []
if 'wins' not in st.session_state:
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0

# -----------------------------
# Game Choices and Emojis
# -----------------------------
choices = ["Rock", "Paper", "Scissors"]
emoji_map = {"Rock":"✊", "Paper":"🤚", "Scissors":"✌"}

# -----------------------------
# User Input
# -----------------------------
user_choice = st.radio("Your Move:", [f"{emoji_map[c]} {c}" for c in choices], horizontal=True)
user_choice = user_choice.split()[1]

# -----------------------------
# Play Button Logic
# -----------------------------
if st.button("Play"):

    # Update history
    st.session_state.history.append(user_choice)

    # Smart AI prediction
    counts = {"Rock":0, "Paper":0, "Scissors":0}
    for move in st.session_state.history:
        counts[move] += 1
    predicted_user_move = max(counts, key=counts.get)
    counters = {"Rock":"Paper", "Paper":"Scissors", "Scissors":"Rock"}
    ai_choice = counters[predicted_user_move]

    # Determine winner
    if user_choice == ai_choice:
        result = "😐 Tie!"
        st.session_state.ties += 1
    elif (user_choice == "Rock" and ai_choice == "Scissors") or \
         (user_choice == "Paper" and ai_choice == "Rock") or \
         (user_choice == "Scissors" and ai_choice == "Paper"):
        result = "🎉 You Win!"
        st.session_state.wins += 1
    else:
        result = "💻 AI Wins!"
        st.session_state.losses += 1

    st.session_state.results.append({
        "Your Move": f"{emoji_map[user_choice]} {user_choice}",
        "AI Move": f"{emoji_map[ai_choice]} {ai_choice}",
        "Result": result
    })

    # -----------------------------
    # Animate Result
    # -----------------------------
    if "Win" in result:
        st.success(result)
    elif "AI" in result:
        st.error(result)
    else:
        st.warning(result)
    time.sleep(0.2)

# -----------------------------
# Layout Columns for Moves
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🧑 Your Move")
    if st.session_state.results:
        st.markdown(f"<h2 style='text-align:center'>{st.session_state.results[-1]['Your Move']}</h2>", unsafe_allow_html=True)

with col2:
    st.subheader("🤖 AI Move")
    if st.session_state.results:
        st.markdown(f"<h2 style='text-align:center'>{st.session_state.results[-1]['AI Move']}</h2>", unsafe_allow_html=True)

with col3:
    st.subheader("🏆 Round Result")
    if st.session_state.results:
        last_result = st.session_state.results[-1]['Result']
        color = "green" if "Win" in last_result else "red" if "AI" in last_result else "orange"
        st.markdown(f"<h2 style='color:{color};text-align:center'>{last_result}</h2>", unsafe_allow_html=True)

# -----------------------------
# Stats & Leaderboard
# -----------------------------
st.subheader("📊 Scoreboard")
score_df = pd.DataFrame({
    "Player": ["You", "AI", "Ties"],
    "Score": [st.session_state.wins, st.session_state.losses, st.session_state.ties]
})
st.dataframe(score_df.style.background_gradient(cmap='coolwarm', axis=0))

# -----------------------------
# Charts
# -----------------------------
col4, col5 = st.columns(2)

with col4:
    st.subheader("🎮 Most Played Moves")
    if st.session_state.history:
        move_counts = Counter(st.session_state.history)
        fig, ax = plt.subplots()
        ax.bar(move_counts.keys(), move_counts.values(), color=["#1f77b4","#ff7f0e","#2ca02c"])
        ax.set_ylabel("Count")
        st.pyplot(fig)

with col5:
    st.subheader("📈 Wins/Losses/Ties Chart")
    stats = [st.session_state.wins, st.session_state.losses, st.session_state.ties]
    fig2, ax2 = plt.subplots()
    ax2.bar(["Wins","Losses","Ties"], stats, color=["green","red","orange"])
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

# -----------------------------
# Game History Table
# -----------------------------
st.subheader("📝 Game History")
if st.session_state.results:
    history_df = pd.DataFrame(st.session_state.results)
    st.dataframe(history_df.style.applymap(lambda x: 'color: green' if 'Win' in str(x) else 'color: red' if 'AI' in str(x) else 'color: orange'))

# -----------------------------
# Reset Button
# -----------------------------
if st.button("🔄 Reset Game"):
    st.session_state.history = []
    st.session_state.results = []
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0
    st.experimental_rerun()