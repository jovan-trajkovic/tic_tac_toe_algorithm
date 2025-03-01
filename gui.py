import tkinter
from tkinter import ttk
import sv_ttk # Sun Valley theme for tkinter
from tictactoe_ai_logic import is_winner, is_board_full, minimax, minimax_alpha_beta

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        
        self.selected_algorithm = tkinter.StringVar(value="Minimax")
        self.difficulty = tkinter.IntVar(value=1)

        self.main_menu_frame = ttk.Frame(self.root)
        self.board_frame = ttk.Frame(self.root)

        self.create_main_menu()

    def create_main_menu(self):
        """Creates the main menu UI (Algorithm selection, difficulty, and play button)"""
        for widget in self.main_menu_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.main_menu_frame, text="Choose AI Algorithm:").pack()
        ttk.Combobox(self.main_menu_frame, textvariable=self.selected_algorithm, values=["Minimax", "Minimax (Alpha-Beta)"], state="readonly").pack()

        ttk.Label(self.main_menu_frame, text="Select Difficulty (Depth 1-9):").pack()
        ttk.Combobox(self.main_menu_frame, textvariable=self.difficulty, values=[i for i in range(1, 10)], state="readonly").pack()
        
        ttk.Button(self.main_menu_frame, text="Play", command=self.start_game).pack(pady=10)
        self.main_menu_frame.pack()
    
    def reset_board(self):
        """Clears the board and creates a fresh game grid"""
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        for row in range(3):
            for col in range(3):
                btn = ttk.Button(self.board_frame, text="", width=5, command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col, ipadx=20, ipady=20, padx=5, pady=5)
                self.buttons[row][col] = btn

        self.status_label = ttk.Label(self.board_frame, text="Your Turn (X)")
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        ttk.Button(self.board_frame, text="Main Menu", command=self.return_to_main_menu).grid(row=4, column=0, columnspan=3, pady=10)

    def return_to_main_menu(self):
        """Returns to the main menu"""
        self.board_frame.pack_forget()
        self.main_menu_frame.pack()
    
    def start_game(self):
        """Starts the game by locking in settings and displaying the Tic-Tac-Toe board"""
        self.algorithm = self.selected_algorithm.get()
        self.depth = self.difficulty.get()

        self.main_menu_frame.pack_forget()
        self.board_frame.pack()
        
        self.reset_board()
        
    def make_move(self, row, col):
        """Handles player move"""
        if self.board[row][col] == " ":
            self.board[row][col] = "X"
            self.buttons[row][col]["text"] = "X"
            self.buttons[row][col]["state"] = "disabled"

            if self.check_winner():
                return
        
        self.computer_move()

    def computer_move(self):
        """Makes AI move"""
        if self.algorithm == "Minimax":
            _, ai_move = minimax(self.board, self.depth, True)
        else:
            _, ai_move = minimax_alpha_beta(self.board, self.depth, float('-inf'), float('inf'), True)
            
        if ai_move:
            ai_row, ai_col = ai_move
            self.board[ai_row][ai_col] = "O"
            self.buttons[ai_row][ai_col]["text"] = "O"
            self.buttons[ai_row][ai_col]["state"] = "disabled"

            if self.check_winner():
                return

    def check_winner(self):
        """Checks for game end conditions"""
        if is_winner(self.board, "X"):
            self.status_label["text"] = "You Win!"
            return True
        elif is_winner(self.board, "O"):
            self.status_label["text"] = "You Lose!"
            return True
        elif is_board_full(self.board):
            self.status_label["text"] = "Draw!"
            return True
        return False

if __name__ == "__main__":
    root = tkinter.Tk()
    app = TicTacToeGUI(root)
    sv_ttk.set_theme("dark")
    root.mainloop()