import streamlit as st

from algorithms.minimax import (
    best_move,
    check_winner
)


def initialize_game():

    if "board" not in st.session_state:
        st.session_state.board = [""] * 9

    if "game_over" not in st.session_state:
        st.session_state.game_over = False


def render_game():

    initialize_game()

    st.subheader(
        "Strategic Decision Simulator"
    )

    board = st.session_state.board

    cols = st.columns(3)

    for row in range(3):

        cols = st.columns(3)

        for col in range(3):

            index = row * 3 + col

            label = (
                board[index]
                if board[index] != ""
                else " "
            )

            if cols[col].button(
                label,
                key=f"cell_{index}"
            ):

                if (
                    board[index] == ""
                    and
                    not st.session_state.game_over
                ):

                    board[index] = "X"

                    result = check_winner(board)

                    if result:

                        st.session_state.game_over = True

                    else:

                        ai_move = best_move(board)

                        if ai_move is not None:
                            board[ai_move] = "O"

                        result = check_winner(board)

                        if result:
                            st.session_state.game_over = True

                    st.rerun()

    winner = check_winner(board)

    if winner:

        if winner == "Draw":
            st.warning("Draw")

        elif winner == "X":
            st.success("You Win")

        elif winner == "O":
            st.error("AI Wins")

    if st.button("Restart Game"):

        st.session_state.board = [""] * 9
        st.session_state.game_over = False

        st.rerun()