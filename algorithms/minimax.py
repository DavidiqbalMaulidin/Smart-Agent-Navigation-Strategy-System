def check_winner(board):

    winning_combinations = [

        [0,1,2],
        [3,4,5],
        [6,7,8],

        [0,3,6],
        [1,4,7],
        [2,5,8],

        [0,4,8],
        [2,4,6]
    ]

    for combo in winning_combinations:

        a,b,c = combo

        if (
            board[a] == board[b] ==
            board[c] != ""
        ):
            return board[a]

    if "" not in board:
        return "Draw"

    return None


def minimax(
    board,
    depth,
    is_maximizing,
    alpha,
    beta
):

    result = check_winner(board)

    if result == "O":
        return 1

    if result == "X":
        return -1

    if result == "Draw":
        return 0

    if is_maximizing:

        best_score = -999

        for i in range(9):

            if board[i] == "":

                board[i] = "O"

                score = minimax(
                    board,
                    depth + 1,
                    False,
                    alpha,
                    beta
                )

                board[i] = ""

                best_score = max(
                    score,
                    best_score
                )

                alpha = max(
                    alpha,
                    best_score
                )

                if beta <= alpha:
                    break

        return best_score

    else:

        best_score = 999

        for i in range(9):

            if board[i] == "":

                board[i] = "X"

                score = minimax(
                    board,
                    depth + 1,
                    True,
                    alpha,
                    beta
                )

                board[i] = ""

                best_score = min(
                    score,
                    best_score
                )

                beta = min(
                    beta,
                    best_score
                )

                if beta <= alpha:
                    break

        return best_score


def best_move(board):

    best_score = -999
    move = None
    
    # Inisialisasi alpha dan beta global untuk level root (teratas)
    alpha = -999
    beta = 999

    for i in range(9):

        if board[i] == "":

            board[i] = "O"

            score = minimax(
                board,
                0,
                False,
                alpha,  # Membawa nilai alpha dinamis yang sudah ter-update
                beta
            )

            board[i] = ""

            if score > best_score:
                best_score = score
                move = i
            
            # CRITICAL FIX: Update nilai alpha di level root agar cabang berikutnya
            # bisa langsung dipangkas jika tidak lebih baik dari move terbaik saat ini.
            alpha = max(alpha, best_score)

    return move