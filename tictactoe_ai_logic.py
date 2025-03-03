import copy
import random

def is_winner(board, player): # Check rows, columns, and diagonals for a winner
    return any(
        all(cell == player for cell in row) for row in board
    ) or any(
        all(board[i][j] == player for i in range(3)) for j in range(3)
    ) or all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3))

def is_board_full(board): # Checks if the board is full
    return all(cell != " " for row in board for cell in row)

def evaluate_board(board, attack_heuristic): # Evaluates the board based on our heuristics
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
    
    def check_open_lines(line, player):
        count = line.count(player)
        empty_spaces = line.count(" ")

        if count == 2 and empty_spaces == 1:
            return 1
        elif count == 1 and empty_spaces == 2:
            return 1
        return 0

    lines = []
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])

    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    if attack_heuristic: # Attack heuristic gives score bonuses if a player is doing well
        for line in lines:
            score -= check_line(line, "X")  # X is minimizing (Player)
            score += check_line(line, "O")  # O is maximizing (Computer)
    else:
        for line in lines:
            score -= check_open_lines(line, "X")  # X is minimizing (Player)
            score += check_open_lines(line, "O")  # O is maximizing (Computer)

    return score

def minimax(board, depth, is_maximizing_player, is_attack):
    if (depth == 0) or is_winner(board, "X") or is_winner(board, "O") or is_board_full(board):
        return evaluate_board(board, is_attack), None

    best_move = None
    best_moves = []

    if is_maximizing_player: # Calculating the computer's move
        val = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ": 
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = "O"
                    eval_score, _ = minimax(new_board, depth - 1, False, is_attack)  # Now calculate the player's move

                    if eval_score > val:
                        val = eval_score
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
                    eval_score, _ = minimax(new_board, depth - 1, True, is_attack)  # Now calculate the computer's move

                    if eval_score < val:
                        val = eval_score
                        best_move = (i, j)

        return val, best_move
    
def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing_player, is_attack):
    if (depth == 0) or is_winner(board, "X") or is_winner(board, "O") or is_board_full(board):
        return evaluate_board(board, is_attack), None

    best_move = None
    best_moves = []

    if is_maximizing_player: # Calculating the computer's move
        val = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ": 
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = "O"
                    eval_score, _ = minimax_alpha_beta(new_board, depth - 1, alpha, beta, False, is_attack)  # Now calculate the player's move

                    if eval_score > val:
                        val = eval_score
                        best_moves = [(i, j)]
                    elif eval_score == val:
                        best_moves.append((i, j))

                    alpha = max(alpha, val)
                    if val >= beta:
                        return val, random.choice(best_moves)
        
        best_move = random.choice(best_moves)

        return val, best_move
        
    else: # Calculating the player's move
        val = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    new_board = copy.deepcopy(board)
                    new_board[i][j] = "X"
                    eval_score, _ = minimax_alpha_beta(new_board, depth - 1, alpha, beta, True, is_attack)  # Now calculate the computer's move

                    if eval_score < val:
                        val = eval_score
                        best_move = (i, j)
                    
                    beta = min(beta, val)
                    if val <= alpha:
                        return val, best_move

        return val, best_move