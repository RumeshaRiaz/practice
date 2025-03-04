import streamlit as st
import random
import time

# Snakes and Ladders positions
snakes = {17: 7, 54: 34, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 99: 78}
ladders = {3: 22, 6: 25, 11: 40, 15: 44, 22: 58, 33: 59, 41: 79, 50: 69, 54: 88, 66: 89, 74: 92, 81: 98}

# Initialize game state if not already set
if "positions" not in st.session_state:
    st.session_state.positions = {"Player 1": 1, "Player 2": 1}
    st.session_state.current_turn = "Player 1"
    st.session_state.roll_result = None
    st.session_state.winner = None

def roll_dice():
    if st.session_state.winner:
        return
    
    dice_value = random.randint(1, 6)
    player = st.session_state.current_turn
    new_position = st.session_state.positions[player] + dice_value
    
    if new_position in snakes:
        new_position = snakes[new_position]
    elif new_position in ladders:
        new_position = ladders[new_position]
    
    if new_position >= 100:
        new_position = 100
        st.session_state.winner = player
    
    st.session_state.positions[player] = new_position
    st.session_state.roll_result = dice_value
    
    if not st.session_state.winner:
        st.session_state.current_turn = "Player 2" if player == "Player 1" else "Player 1"

def reset_game():
    st.session_state.positions = {"Player 1": 1, "Player 2": 1}
    st.session_state.current_turn = "Player 1"
    st.session_state.roll_result = None
    st.session_state.winner = None

# Streamlit UI
st.title("🎲 Snakes & Ladders Game")

# Game Board Visualization
st.markdown("### Game Board")
board = ""  # Representing board as text for now
for row in range(10, 0, -1):
    for col in range(1, 11):
        num = (row - 1) * 10 + col if row % 2 != 0 else row * 10 - col + 1
        if num == st.session_state.positions["Player 1"]:
            board += "🟦 "
        elif num == st.session_state.positions["Player 2"]:
            board += "🟥 "
        else:
            board += f"{num:02d} "
    board += "\n"
st.text(board)

# Display current game state
st.write(f"**{st.session_state.current_turn}'s Turn**")
if st.session_state.roll_result is not None:
    st.write(f"🎲 Dice Roll: {st.session_state.roll_result}")
    
st.write(f"**Player 1 Position:** {st.session_state.positions['Player 1']}")
st.write(f"**Player 2 Position:** {st.session_state.positions['Player 2']}")

# Buttons for rolling dice and resetting game
if not st.session_state.winner:
    if st.button("Roll Dice 🎲"):
        roll_dice()
        time.sleep(1)
        st.experimental_rerun()
else:
    st.success(f"🎉 {st.session_state.winner} wins!")

if st.button("Restart Game 🔄"):
    reset_game()
    st.experimental_rerun()
