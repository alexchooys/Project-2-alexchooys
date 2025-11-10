"""
Author: Yuanseng Choo
Date: 2025-11-9
Program: Tic-Tac-Toe (Minimax Algorithm)

Overview:
- Starts a new Tic-Tac-Toe game with X going first.
- Prompts players for row and column input (0-2).
- Validates input and occupied cells.
- Updates and prints the board after each valid move.
- Detects wins (rows, columns, diagonals) and draws.
- Offers replay at the end.
"""

import re

class Board:
    """Represents the Tic-Tac-Toe board."""
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]

    def printBoard(self):
        """Display the current board to the console."""
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)
        for i in range(3):
            print(f"| {i} | {self.c[i][0]} | {self.c[i][1]} | {self.c[i][2]} |")
            print("-----------------")
        print()

class Game:
    """Game logic and control for Tic-Tac-Toe."""
    def __init__(self):
        self.board = Board()
        self.turn = "X"

    def switchPlayer(self):     
        """Switch the current player X <-> O."""
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def validateEntry(self, row, col):
        """Return True if valid, otherwise False (and print helpful message)."""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            print("Invalid entry: try again.")
            print("Row & column numbers must be either 0, 1, or 2.")
            return False
        
        if self.board.c[row][col] != " ":
            print("That cell is already taken.")
            print("Please make another selection.")
            return False
        
        return True
    
    def checkFull(self):
        """Return True if board is full (draw)."""
        for r in range(3):
            for c in range(3):
                if self.board.c[r][c] == " ":
                    return False
        return True

    def checkWin(self):
        """Return True if current player (self.turn) wins."""
        b = self.board.c
        t = self.turn

        # rows
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] == t:
                return True
            
        # cols
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] == t:
                return True
            
        # diagonals
        if b[0][0] == b[1][1] == b[2][2] == t:
            return True
        if b[0][2] == b[1][1] == b[2][0] == t:
            return True
        return False

    def checkEnd(self):
        """Return True if game is over (win or draw)."""
        if self.checkWin():
            print(f"{self.turn} IS THE WINNER!!!")
            return True
        if self.checkFull():
            print("DRAW! NOBODY WINS!")
            return True
        return False
    

    def check_winner_static(self, board):
        """
        Check winner without using self.turn.
        Returns 'X' or 'O' if winner found, otherwise None.
        """
        b = board
        # rows
        for r in range(3):
            if b[r][0] == b[r][1] == b[r][2] and b[r][0] != " ":
                return b[r][0]
        # cols
        for c in range(3):
            if b[0][c] == b[1][c] == b[2][c] and b[0][c] != " ":
                return b[0][c]
        # diagonals
        if b[0][0] == b[1][1] == b[2][2] and b[0][0] != " ":
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] and b[0][2] != " ":
            return b[0][2]
        return None

    def minimax(self, board, is_maximizing):
        """Minimax: +1 for O win, -1 for X win, 0 for draw."""
        winner = self.check_winner_static(board)
        if winner == 'O':
            return 1
        if winner == 'X':
            return -1
        # draw?
        if all(cell != " " for row in board for cell in row):
            return 0

        if is_maximizing:
            best_score = -999
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = 'O'
                        score = self.minimax(board, False)
                        board[r][c] = " "
                        if score > best_score:
                            best_score = score
            return best_score
        else:
            # minimizing (opponent X)
            best_score = 999
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = 'X'
                        score = self.minimax(board, True)
                        board[r][c] = " "
                        if score < best_score:
                            best_score = score
            return best_score

    def computer_move(self):
        """Choose the best move for the computer (O) using minimax and place it."""
        best_score = -999
        best_move = None
        b = self.board.c

        # evaluate all possible moves
        for r in range(3):
            for c in range(3):
                if b[r][c] == " ":
                    b[r][c] = 'O'
                    score = self.minimax(b, False)  # after O moves, it's X's turn
                    b[r][c] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)

        # place the chosen move
        if best_move is not None:
            r, c = best_move
            self.board.c[r][c] = 'O'
            print(f"Computer places O at row #{r} and column #{c}")
        else:
            # no valid moves (shouldn't happen here)
            print("Computer has no moves!")



    def playGame(self):
        """Run one full game (without replay prompt)."""
        # new clean board each game
        self.board = Board()
        self.turn = "X"

        print("Mode: Player vs Computer (You are X; Computer is O).")
        print()
        print("New Game: X goes first.")
        print()
        self.board.printBoard()

        while True:
            print(f"{self.turn}'s turn.")
            print(f"Where do you want your {self.turn} placed?")
            print("Please enter row number and column number separated by a comma.")

            while True:
                raw = input().strip()  

                # If the user entered nothing or only spaces, re-prompt
                if not raw:
                    print("Invalid entry: try again.")
                    print("Row & column numbers must be either 0, 1, or 2.")
                    print()
                    print(f"{self.turn}'s turn.")
                    print(f"Where do you want your {self.turn} placed?")
                    print("Please enter row number and column number separated by a comma.")
                    continue

                # Split on either a comma or any whitespace (one or more)
                parts = [t for t in re.split(r"[,\s]+", raw) if t]

                # handle no tokens (e.g., input was "," or ",,")
                if not parts:
                    print("Invalid entry: try again.")
                    print("Row & column numbers must be either 0, 1, or 2.")
                    print()
                    print(f"{self.turn}'s turn.")
                    print(f"Where do you want your {self.turn} placed?")
                    print("Please enter row number and column number separated by a comma.")
                    continue               

                # Handle one-taken inputs cleanly
                if len(parts) == 1:
                    only = parts[0]
                    if only.isdigit():
                        print(f"You entered only one number: {only}")
                        print("Please enter two numbers 0, 1, or 2, for example: 1,2")
                    else:
                            print(f"You entered invalid number: {only}")
                            print("Use numbers 0, 1, or 2, for example: 1,2")
                    print()
                    print(f"{self.turn}'s turn.")
                    print(f"Where do you want your {self.turn} placed?")
                    print("Please enter row number and column number separated by a comma.")
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
                    print(f"{self.turn}'s turn.")
                    print(f"Where do you want your {self.turn} placed?")
                    print("Please enter row number and column number separated by a comma.")
                    continue

                row = int(parts[0])
                col = int(parts[1])
                print(f"You have entered row #{row}")
                print(f"{'and column':>20} #{col}")

                # Validate coordinates and occupancy
                if not self.validateEntry(row, col):
                    print()
                    print(f"{self.turn}'s turn.")
                    print(f"Where do you want your {self.turn} placed?")
                    print("Please enter row number and column number separated by a comma.")
                    continue
                
                print("Thank you for your selection.")
                print()
                self.board.c[row][col] = self.turn
                break

            # After human move, check if human won or board is full
            self.turn = 'X'  # ensure turn reflects current mover for checkEnd()
            if self.checkEnd():
                print()
                self.board.printBoard()
                break

            # Print board after human move
            self.board.printBoard()

            # --- Computer's immediate response (O) ---
            self.turn = 'O'  # set turn to O so checkEnd prints correctly if O wins
            self.computer_move()
            print()

            # After computer move, check for end (win/draw)
            if self.checkEnd():
                print()
                self.board.printBoard()
                break

            # Print board after computer move
            self.board.printBoard()

            # prepare for next human turn
            self.turn = 'X'

def main():
    again = 'y'
    
    # using while-loop that runs until the user says no for another game
    while again.lower().startswith('y'):
        game = Game()
        game.playGame()
        print()
        
        again = input("Another game? Enter Y or y for yes.\n").strip()
    
    print("Thank you for playing!")

if __name__ == "__main__":
    main()