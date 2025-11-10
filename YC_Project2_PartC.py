"""
Author: Yuanseng Choo
Date: 2025-11-9
Program: Tic-Tac-Toe (Random Forest Classifier AI)

Overview:
- Starts a new Tic-Tac-Toe game with X going first.
- Prompts players for row and column input (0-2).
- Validates input and occupied cells.
- Updates and prints the board after each valid move.
- Detects wins (rows, columns, diagonals) and draws.
- Offers replay at the end.
- Uses Random Forest Classifier for AI moves.
- The chosen dataset is "tictac_single.txt" for the intermediate boards optimal play (multi-class classification).
"""

import re
import random
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def load_tictac_dataset_with_pandas(path):
    """
    Load tic-tac-toe dataset with pandas.
    Expect rows of 10 integers per row: 9 features (x0..x8) and label (0..8).
    Returns X (n_samples x 9) as numpy array and y (n_samples,) as numpy array.
    """
    df = pd.read_table(path, delim_whitespace=True, header=None)
    df = df.iloc[:, :10]
    X = df.iloc[:, 0:9].to_numpy(dtype=int)
    y = df.iloc[:, 9].to_numpy(dtype=int)
    return X, y

def train_model(X, y, verbose=True):
    """Train RandomForest on X,y and print evaluation."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)
    if verbose:
        preds = clf.predict(X_test)
        print("Model evaluation on held-out test set:")
        print("Accuracy:", accuracy_score(y_test, preds))
        print(classification_report(y_test, preds, zero_division=0))
    return clf

class Board:
    def __init__(self):
        """Initialize a 3x3 board filled with spaces."""
        self.c = [[" ", " ", " "] for _ in range(3)]

    def printBoard(self):
        """Display the current board to the console."""
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)
        for i in range(3):
            print(f"| {i} | {self.c[i][0]} | {self.c[i][1]} | {self.c[i][2]} |")
            print("-----------------")
        print()

class Game:
    """Human (X) vs ML model (O)."""
    def __init__(self, model=None):
        self.board = Board()
        self.turn = "X"
        self.model = model

    def validateEntry(self, row, col):
        """Return True if valid, otherwise False (and print helpful message)."""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Invalid entry: try again. Row & column must be 0, 1, or 2.")
            print()
            return False
        
        if self.board.c[row][col] != " ":
            print("That cell is already taken. Please make another selection.")
            print()
            return False
        
        return True

    def checkFull(self):
        """Return True if board is full (draw)."""
        for r in range(3):
            for c in range(3):
                if self.board.c[r][c] == " ":
                    return False
        return True
    
    def checkWin_for_turn(self, turn):
        """
        Check if a specific player (turn) has won.
        Args:
            turn (str): 'X' or 'O'
        Returns:
            bool: True if player has a 3-in-a-row, False otherwise.
        """
        b = self.board.c
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] == turn:
                return True
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] == turn:
                return True
        if b[0][0] == b[1][1] == b[2][2] == turn:
            return True
        if b[0][2] == b[1][1] == b[2][0] == turn:
            return True
        return False

    def checkEnd(self):
        """Check if the game has ended (win or draw)."""
        if self.checkWin_for_turn('X'):
            print("X IS THE WINNER!!!")
            return True
        if self.checkWin_for_turn('O'):
            print("O IS THE WINNER!!!")
            return True
        if self.checkFull():
            print("DRAW! NOBODY WINS!")
            return True
        return False

    def board_to_model_features(self):
        """
        Convert the current board state into a numeric feature vector for ML model.
        Mapping:
            'X' -> +1
            'O' -> -1
            ' ' -> 0
        Returns:
            list[int]: 9-length list representing the board.
        """
        mapping = {'X': 1, 'O': -1, ' ': 0}
        return [mapping[self.board.c[r][c]] for r in range(3) for c in range(3)]

    def get_available_moves(self):
        """Return a list of available (row, col) moves."""
        return [(r, c) for r in range(3) for c in range(3) if self.board.c[r][c] == " "]

    def model_move(self):
        """Predict the best move for O using trained model."""
        moves = self.get_available_moves()
        if not moves:
            return

        feats = np.array(self.board_to_model_features()).reshape(1, -1)
        probs = self.model.predict_proba(feats)[0]
        classes = self.model.classes_
        ranked = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)

        for idx, _p in ranked:
            r, c = divmod(int(idx), 3)
            if self.board.c[r][c] == " ":
                self.board.c[r][c] = 'O'
                print(f"Computer places O at row #{r} and column #{c}")
                return

        # fallback to random valid move
        r, c = random.choice(moves)
        self.board.c[r][c] = 'O'
        print(f"Computer falls back and places O at row #{r} and column #{c}")

    def get_move_from_user(self):
        """Get human input and return (row, col)."""
        while True:
            print(f"{self.turn}'s turn.")
            print(f"Where do you want your {self.turn} placed?")
            print("Please enter row number and column number separated by a comma.")

            try:
                raw = input().strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return None

            # If the user entered nothing or only spaces, re-prompt
            if not raw:
                print("Invalid entry: try again.")
                print("Row & column numbers must be either 0, 1, or 2.")
                print()       
                continue

            # Split on either a comma or any whitespace (one or more)
            parts = [t for t in re.split(r"[,\s]+", raw) if t]

            # handle no tokens (e.g., input was "," or ",,")
            if not parts:
                print("Invalid entry: try again.")
                print("Row & column numbers must be either 0, 1, or 2.")
                print()
                continue  

            # Handle one-value inputs cleanly
            if len(parts) == 1:
                only = parts[0]
                if only.isdigit():
                    print(f"You entered only one number: {only}")
                    print("Please enter two numbers 0, 1, or 2, for example: 1,2")
                else:
                    print(f"You entered invalid number: {only}")
                    print("Use numbers 0, 1, or 2, for example: 1,2")
                print()
                continue

            # Validate we got exactly two numeric tokens
            row1 = str(parts[0])
            col1 = str(parts[1])

            if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
                print(f"You have entered row #{row1}")
                print(f"{'and column':>20} #{col1}")
                print("Invalid entry: try again.")
                print("Row & column numbers must be either 0, 1, or 2.")
                print()
                continue

            # Convert to integers
            row = int(parts[0])
            col = int(parts[1])
            print(f"You have entered row #{row}")
            print(f"{'and column':>20} #{col}")
            return (row, col)

    def human_move(self):
        """Get and validate human move, place X on board."""
        mv = self.get_move_from_user()
        if mv is None:
            return False
        row, col = mv
        if not self.validateEntry(row, col):
            return self.human_move()
        self.board.c[row][col] = 'X'
        return True

    def playGame(self):
        """Run one full Player vs ML Model game."""
        self.board = Board()
        self.turn = 'X'

        print("Mode: Player vs ML Model (You are X; Computer is O).\n")
        self.board.printBoard()

        while True:
            ok = self.human_move()
            if not ok:
                return
            if self.checkEnd():
                print(); self.board.printBoard(); break

            self.board.printBoard()
            self.model_move()
            if self.checkEnd():
                print(); self.board.printBoard(); break

            self.board.printBoard()

def main():
    X, y = load_tictac_dataset_with_pandas("tictac_single.txt")
    print(f"Loaded {X.shape[0]} samples.")
    print("Training RandomForest model...")
    model = train_model(X, y)
    print("Model ready. Let's play!\n")

    again = 'y'
    while again.lower().startswith('y'):
        game = Game(model=model)
        game.playGame()
        try:
            again = input("Another game? Enter Y or y for yes.\n").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return
    print("Thank you for playing!")

if __name__ == "__main__":
    main()