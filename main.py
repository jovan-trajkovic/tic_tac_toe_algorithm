import copy
import random

# Initialize board
board = [[" " for _ in range(3)] for _ in range(3)]

def print_board(board): # Prints the board in the console for testing
    for i, row in enumerate(board):
        print(" | ".join(row))
        if i < len(board) - 1:
            print("-" * 10)

def is_winner(board, player): # Check rows, columns, and diagonals for a winner
    return any(
        all(cell == player for cell in row) for row in board
    ) or any(
        all(board[i][j] == player for i in range(3)) for j in range(3)
    ) or all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3))

def is_board_full(board): # Checks if the board is full
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                return False
    
    return True

def generate_possible_moves(board, player): # Generates all possible boards for the current player's move
    return
    possible_boards = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                new_board = [row[:] for row in board]
                new_board[i][j] = player  # Place the player's move
                possible_boards.append(new_board)
                #print_board(new_board)
    return possible_boards

def evaluate_board(board): # Evaluates the board based on our heuristics
    score = 0

    WIN_SCORE = 100
    TWO_IN_A_ROW = 10
    ONE_IN_A_ROW = 1

    def check_line(line, player): # Checks how close a player is to a win
        count = line.count(player)
        empty_spaces = line.count(" ")

        if count == 3:
            return WIN_SCORE
        elif count == 2 and empty_spaces == 1:
            return TWO_IN_A_ROW
        elif count == 1 and empty_spaces == 2:
            return ONE_IN_A_ROW
        return 0

    # Evaluates all rows, columns, and diagonals
    lines = []
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])

    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    # Calculate score for both players
    for line in lines:
        score -= check_line(line, "X")  # X is minimizing (Player)
        score += check_line(line, "O")  # O is maximizing (Computer)

    return score

def minimax(board, depth, is_maximizing_player):
    if (depth == 0) or is_winner(board, "X") or is_winner(board, "O") or is_board_full(board):
        return evaluate_board(board), None

    best_move = None
    best_moves = [None]

    if is_maximizing_player: # Calculating the computer's move
        val = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ": 
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = "O"
                    eval_score, _ = minimax(new_board, depth - 1, False)  # Now calculate the player's move

                    if eval_score > val:
                        val = eval_score
                        #best_move = (i, j)
                        best_moves = [(i, j)]
                    elif eval_score == val:
                        best_moves.append((i, j))
        
        best_move = random.choice(best_moves)

        return val, best_move
        
    else: # Calculating the player's move
        val = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = "X"
                    eval_score, _ = minimax(new_board, depth - 1, True)  # Now calculate the computer's move

                    if eval_score < val:
                        val = eval_score
                        best_move = (i, j)

        return val, best_move

# Game loop (for testing)
player_turn = True
while True:    
    if player_turn:  # For the player's move
        print_board(board)
        row, col = map(int, input("Enter your move (row col): ").split())
        if board[row][col] == " ": 
            board[row][col] = "X"
    else:  # For the computer's move
        # Call minimax to get best move
        _,row_col = minimax(board, depth=1, is_maximizing_player=True)
        row, col = row_col
        if board[row][col] == " ": 
            board[row][col] = "O"

    # Check for winner
    if is_winner(board, "X"):
        print("Player wins!")
        break
    elif is_winner(board, "O"):
        print("Computer wins!")
        break
    elif is_board_full(board):
        print_board(board)
        print("Draw")
        break
    
    # Switch turn
    player_turn = not player_turn
