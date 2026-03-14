# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rock-Paper-Scissors AI", layout="wide")
st.title("✊🤚✌ Rock-Paper-Scissors AI Game")

# --- Initialize session state ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'results' not in st.session_state:
    st.session_state.results = []
if 'wins' not in st.session_state:
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0

# --- Options ---
choices = ["Rock", "Paper", "Scissors"]
emoji_map = {"Rock":"✊", "Paper":"🤚", "Scissors":"✌"}

# --- User Input ---
user_choice = st.radio("Your Move:", [f"{emoji_map[c]} {c}" for c in choices])
user_choice = user_choice.split()[1]  # get the text without emoji

# --- Play Button ---
if st.button("Play"):

    # --- Update history ---
    st.session_state.history.append(user_choice)

    # --- Smart AI: Predict next user move ---
    counts = {"Rock":0, "Paper":0, "Scissors":0}
    for move in st.session_state.history:
        counts[move] += 1
    predicted_user_move = max(counts, key=counts.get)
    counters = {"Rock":"Paper", "Paper":"Scissors", "Scissors":"Rock"}
    ai_choice = counters[predicted_user_move]

    # --- Determine winner ---
    if user_choice == ai_choice:
        result = "😐 It's a tie!"
        st.session_state.ties += 1
    elif (user_choice == "Rock" and ai_choice == "Scissors") or \
         (user_choice == "Paper" and ai_choice == "Rock") or \
         (user_choice == "Scissors" and ai_choice == "Paper"):
        result = "🎉 You win!"
        st.session_state.wins += 1
    else:
        result = "💻 AI wins!"
        st.session_state.losses += 1

    st.session_state.results.append({
        "Your Move": f"{emoji_map[user_choice]} {user_choice}",
        "AI Move": f"{emoji_map[ai_choice]} {ai_choice}",
        "Result": result
    })

    # --- Display Choices ---
    st.write(f"🧑 You chose: {emoji_map[user_choice]} {user_choice}")
    st.write(f"🤖 AI chose: {emoji_map[ai_choice]} {ai_choice}")
    st.write(result)

# --- Display Stats ---
st.subheader("📊 Stats")
st.write(f"🏆 Wins: {st.session_state.wins} | 💻 Losses: {st.session_state.losses} | 😐 Ties: {st.session_state.ties}")

# --- Display History ---
st.subheader("📝 Game History")
if st.session_state.results:
    history_df = pd.DataFrame(st.session_state.results)
    st.dataframe(history_df)

# --- Reset Button ---
if st.button("🔄 Reset Game"):
    st.session_state.history = []
    st.session_state.results = []
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.ties = 0
    st.experimental_rerun()