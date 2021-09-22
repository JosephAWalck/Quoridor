# Author: Joseph Walck
# Date: 8/11/2021
# Description: A two player version of the game Quoridor. The game is played on a 9x9 board of cells where each player
#              can move their pawn in any orthogonal direction so long as a fence is not blocking that move. Special
#              moves such as diagonal moves and jump moves are also allowed under the rules of Quoridor.
#              Each player starts with 10 fences and can place a fence in any position within the bounds of the board
#              that is not already occupied by a fence in that orientation (horizontal or vertical). Neither player is
#              allowed to completely lock one side of the board with fences (i.e., a path to each base must aways
#              exist).
#              A player wins once their pawn has reached the opponent's base line.

class QuoridorGame:
    """
    Represents a Quoridor game board. This class handles the game initialization, printing the board state to the
    console, keeping track of turns, keeping track of available fences, declaring a winner, moving the players' pawns,
    and placing the players' fences. All pawn movements and fence placement is also validated so that they follow the
    rules of Quoridor.
    """

    def __init__(self):
        """
        Initialize the size of the board, player starting positions, player base lines, player total fences,
        the starting turn, and the win condition. self._pawns, self._total_fences, self._horizontal_fences, and
        self._vertical_fences are also implemented to conveniently store other data members for access throughout the
        QuoridorGame class.
        """
        self._size = 9
        self._rows = self._size
        self._columns = self._size
        self._p1 = (4, 0)
        self._p2 = (4, 8)
        self._pawns = [self._p1, self._p2]
        self._p1_base = 0
        self._p2_base = 8
        self._win_con = [self._p2_base, self._p1_base]
        self._p1_fences = 10
        self._p2_fences = 10
        self._total_fences = [self._p1_fences, self._p2_fences]
        self._horizontal_fences = []
        self._vertical_fences = []
        self._turn = 1
        self._visited = []

    def __str__(self):
        """
        Creates a string illustrating the current board state that can be printed to the console.
        """
        board = ""
        player_one = self._pawns[0]
        player_two = self._pawns[1]
        for i in range(self._size):
            for j in range(self._size):
                if player_one[1] == i and player_one[0] == j:
                    board += "P1"
                elif player_two[1] == i and player_two[0] == j:
                    board += "P2"
                else:
                    board += "**"
                if (j + 1, i) in self._vertical_fences:
                    board += "|"
                else:
                    board += " "
            board += "\n"
            for j in range(self._size):
                if (j, i + 1) in self._horizontal_fences:
                    board += "-- "
                else:
                    board += "   "
            board += "\n"
        return board

    def print_board(self):
        """
        Prints the board as a string to console.
        """
        print(self.__str__())

    def is_turn(self, player):
        """
        Takes a player number (1 or 2) and returns True if it is that player's turn and False if it is not that player's
        turn.
        """
        if player == 1 and self._turn % 2 == 1:
            return True
        if player == 2 and self._turn % 2 == 0:
            return True
        else:
            return False

    def next_turn(self):
        """
        Increments the turn by one.
        """
        self._turn += 1

    def is_winner(self, player):
        """
        Takes a player number (1 or 2) and returns whether or not that player has won the game.
        """
        if self._pawns[player - 1][1] == self._win_con[player - 1]:
            return True
        else:
            return False

    def reset_visited(self):
        """Reset the visited data member to be an empty list."""
        self._visited = []

    def fair_play_rec(self, player, current_pos):
        """Recursive method that takes a player number and position and returns True if that player is able to reach
        their opponent's base line. Returns False otherwise"""
        (col, row) = current_pos
        self._visited.append(current_pos)

        if player == 1 and current_pos[1] == self._p2_base:
            return True
        if player == 2 and current_pos[1] == self._p1_base:
            return True

        fence_right = (col + 1, row) in self._vertical_fences
        fence_left = (col - 1, row) in self._vertical_fences
        fence_up = (col, row - 1) in self._horizontal_fences
        fence_down = (col, row + 1) in self._horizontal_fences

        if not fence_right and (col + 1) < self._size:
            if (col + 1, row) not in self._visited:
                if self.fair_play_rec(player, (col + 1, row)):
                    return True
                else:
                    self.fair_play_rec(player, (col + 1, row))
        if not fence_left and (col - 1) >= 0:
            if (col - 1, row) not in self._visited:
                if self.fair_play_rec(player, (col - 1, row)):
                    return True
                else:
                    self.fair_play_rec(player, (col - 1, row))
        if not fence_up and (row - 1) >= 0:
            if (col, row - 1) not in self._visited:
                if self.fair_play_rec(player, (col, row - 1)):
                    return True
                else:
                    self.fair_play_rec(player, (col, row - 1))
        if not fence_down and (row + 1) < self._size:
            if (col, row + 1) not in self._visited:
                if self.fair_play_rec(player, (col, row + 1)):
                    return True
                else:
                    self.fair_play_rec(player, (col, row + 1))
        return False

    def fair_play(self, player):
        """Helper method that takes a player number (1 or 2), resets the visited data member, and passes the player
        number and their current position to fair_play_rec."""
        pos = self._pawns[player - 1]
        self.reset_visited()
        self._visited.append(pos)
        return self.fair_play_rec(player, pos)

    def is_move_valid(self, player, next_pos):
        """
        Takes a player number (1 or 2) and the position that player would like to move to. Returns False if the position
        to be made is the same  as the current position and if either position coordinate is out of bounds.
        Returns True if there is no fence blocking a move to the next position.
        """
        (current_col, current_row) = self._pawns[player - 1]
        (next_col, next_row) = next_pos

        if next_row == current_row and next_col == current_col:
            return False
        if next_row >= self._size or next_row < 0:
            return False
        if next_col >= self._size or next_row < 0:
            return False

        fence_right = (current_col + 1, current_row) in self._vertical_fences
        fence_left = (current_col, current_row) in self._vertical_fences
        fence_up = (current_col, current_row) in self._horizontal_fences
        fence_down = (current_col, current_row + 1) in self._horizontal_fences

        # Move Right
        if next_row == current_row and next_col == current_col + 1:
            return not fence_right
        # Move Left
        if next_row == current_row and next_col == current_col - 1:
            return not fence_left
        # Move Up
        if next_row == current_row - 1 and next_col == current_col:
            return not fence_up
        # Move Down
        if next_row == current_row + 1 and next_col == current_col:
            return not fence_down
        else:
            return False

    def legal_moves(self, player):
        """
        Takes a player number (1 or 2) and iterates through each of the lists of moves below, checking them with
        is_move_valid and adding them to the list of legal moves if is_move_valid returns True.
        Returns the list legal_moves.
        """
        (col, row) = self._pawns[player - 1]
        (opp_col, opp_row) = self._pawns[player % 2]
        ortho_moves = [(col + 1, row), (col - 1, row), (col, row + 1), (col, row - 1)]
        opp_ortho_moves = [(opp_col + 1, opp_row), (opp_col - 1, opp_row), (opp_col, opp_row + 1),
                           (opp_col, opp_row - 1)]
        diag_moves = [(col + 1, row + 1), (col - 1, row + 1), (col + 1, row - 1), (col - 1, row - 1)]
        jump_moves = [(col + 2, row), (col - 2, row), (col, row + 2), (col, row - 2)]
        legal_moves = []

        # Ortho Moves
        for move in ortho_moves:
            if self.is_move_valid(player, move) and move != (opp_col, opp_row):
                legal_moves.append(move)

        # Jump Move
        for opp_move in opp_ortho_moves:
            for jump_move in jump_moves:
                if self.is_move_valid((player + 1) % 2, opp_move) and \
                        self.is_move_valid(player, (opp_col, opp_row)):
                    if opp_move == jump_move and self._pawns[player % 2] in ortho_moves:
                        legal_moves.append(jump_move)
                        return legal_moves

        # Diagonal Move
        for opp_move in opp_ortho_moves:
            for diag_move in diag_moves:
                if self.is_move_valid((player + 1) % 2, opp_move) and \
                        self.is_move_valid(player, (opp_col, opp_row)):
                    if opp_move == diag_move and self._pawns[player % 2] in ortho_moves:
                        legal_moves.append(diag_move)

        return legal_moves

    def move_pawn(self, player, next_pos):
        """
        Takes a player number (1 or 2) and the position on the board that player would like to move to. If is is not
        that player's turn, there is a winner, or the move is not in the list that legal_moves has returned, move_pawn
        returns false move_pawn returns False.Moves the pawn on the game board. Otherwise, the function returns True
        and moves the pawn to the position player would like to move.
        """
        if not self.is_turn(player):
            return False
        for num in range(1, 3):
            if self.is_winner(num):
                return False

        if next_pos in self.legal_moves(player):
            self._pawns[player - 1] = next_pos
            self.next_turn()
            return True
        else:
            return False

    def use_fence(self, player):
        """Decrements the player's total number of fences."""
        self._total_fences[player - 1] -= 1

    def is_fence_valid(self, player, orientation, pos):
        """
        Takes a player number (1 or 2), an orientation, and a position on the board the player would like to place a
        fence as parameters. Returns False if the player no longer has any fences, if the fences are to be placed out
        of bounds, and if the fences has already been placed in that orientation at that position. Returns True if the
        fence placement is possible.
        """
        (col, row) = pos
        if self._total_fences[player - 1] == 0:
            return False
        if orientation == "v":
            if (col <= 0 or col >= self._size) or (row < 0 or row >= self._size):
                return False
        if orientation == "h":
            if (col < 0 or col >= self._size) or (row <= 0 or row >= self._size):
                return False
        if orientation == "v" and pos in self._vertical_fences:
            return False
        if orientation == "h" and pos in self._horizontal_fences:
            return False
        else:
            return True

    def place_fence(self, player, orientation, pos):
        """
        Takes a player number (1 or 2), an orientation, and a position on the board the player would like to place a
        fence as parameters. Returns false if it is not that player's turn, if there has already been a winner declared,
        and if is_fence_valid returns False. Otherwise, the fence location is added to that fence orientation's list,
        the turn is incremented, the total fences for that player is decremented, and returns True.
        """

        if not self.is_turn(player):
            return False
        for num in range(1, 3):
            if self.is_winner(num):
                return False
        if not self.is_fence_valid(player, orientation, pos):
            return False
        if orientation == "v":
            self._vertical_fences.append(pos)
            if not self.fair_play(1) or not self.fair_play(2):
                self._vertical_fences.remove(pos)
                return "breaks the fair play rule"
            self.next_turn()
            self.use_fence(player)
            return True
        if orientation == "h":
            self._horizontal_fences.append(pos)
            if not self.fair_play(1) or not self.fair_play(2):
                self._horizontal_fences.remove(pos)
                return "breaks the fair play rule"
            self.next_turn()
            self.use_fence(player)
            return True


def main():
    q = QuoridorGame()
    q.move_pawn(2, (4, 7))  # moves the Player2 pawn -- invalid move because only Player1 can start, returns False
    q.move_pawn(1, (4, 1))  # moves the Player1 pawn -- valid move, returns True
    q.place_fence(1, 'h', (6, 5))  # places Player1's fence -- out of turn move, returns False
    q.move_pawn(2, (4, 7))  # moves the Player2 pawn -- valid move, returns True
    q.place_fence(1, 'h', (6, 5))  # places Player1's fence -- returns True
    q.place_fence(2, 'v', (3, 3))  # places Player2's fence -- returns True
    q.is_winner(1)  # returns False because Player 1 has not won
    q.is_winner(2)  # returns False because Player 2 has not won
    q.print_board()


if __name__ == "__main__":
    main()