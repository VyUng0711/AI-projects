import copy

class Player:
    """
    A class that shows the symbol/color the current player holds
    Initialized to be True if the player is x (black) and False if the player is o (white)
    """

    def __init__(self, isBlack):
        if isBlack:
            self.isBlack = True
            self.color = "BLACK"
            self.symbol = "x"
        else:
            self.isBlack = False
            self.color = "WHITE"
            self.symbol = "o"

    def __eq__(self, other):
        return type(self) == type(other) and \
               self.color == other.color

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return self.color

    def __repr__(self):
        return str(self)

    def opponent_color(self):
        # Return the color of your opponent
        return Player(not self.isBlack)


class Board:
    """
    A class that defines the board
    for a game of gomoku
    """

    def __init__(self, size, max_consecutive):
        """
        White contains list of positions that are occupied by white (o)
        Black contains list of positions that are occupied by black (x)
        Board is represented as a 2x2 matrix (array of array)
            A position is marked "." if it is empty
            A position is marked "o" if it is occupied by white
            A position is marked "x" if it is occupied by black
        max_consecutive: number of consecutive points that you need to win the game

        """
        self.white = []
        self.black = []
        self.board = [["." for i in range(size)] for i in range(size)]
        self.size = size
        self.max_consecutive = max_consecutive
        self.win = False
        self.winner = "None"
        self.final_result = ""
        self.total_time = 0
        self.total_moves = 0

    def __str__(self):
        """
        Represent the UI of a board
        """
        string = ""
        string += "                x axis         \n"
        string += "        _______________________\n"
        string += "          "
        for i in range(self.size):
            string += "{0}{1}".format(i % 10, " " if i < 10 else "'")
            # string+="{0}{1}".format(i, " ")
        string += "\n"
        i = 0

        for k in range(len(self.board[0])):
            if k == len(self.board[0]) // 2:
                string += "y axis |"
            else:
                string += "       |"
            string += "{0}{1}".format(i % 10, " " if i < 10 else "'")
            i += 1
            for h in self.board:
                string += "{0} ".format(h[k])
            string += "\n"

        if self.win:
            string += self.final_result + "\n"
        return string

    def __len__(self):
        """
        Return the number of consecutive points needed to win
        """
        return self.max_consecutive

    def __repr__(self):

        return str(self)

    def __getitem__(self, num):
        return self.board[num]

    def __eq__(self, other):
        return (
                type(self) == type(other) and \
                self.white == other.white and \
                self.black == other.black and \
                self.size == other.size)

    def __ne__(self, other):
        return not (self == other)

    def turn(self):
        # return the player whose current turn it is
        return Player(len(self.black) == len(self.white))

    def is_valid_move(self, (x, y)):
        """
        Return True if the position is to an empty position.
        which means a move there would be valid.
        Otherwise, return False
        """
        return self.is_inBoard((x, y)) and self.board[x][y] == "."

    def is_inBoard(self, (x, y)):
        """
        Return True if a position is in the board.
        Otherwise, return False
        """
        return x >= 0 and x < self.size and y >= 0 and y < self.size

    def move(self, (x, y)):
        """
        Return the updated board after a move is made.

        """
        turn = self.turn()
        updated = copy.deepcopy(self)
        if self.win:
            # If the game has been won, simply return a copy of the previous state
            return updated
        # Else: we update the state board with that move.
        updated.board[x][y] = turn.symbol
        if turn.isBlack:
            updated.black.append((x, y))
        else:
            updated.white.append((x, y))
        updated.checkWinningMove()
        return updated

    def count_path_len(self, Player, (x, y), (px, py), counter):
        """
        Returns the number of consecutive
        symbols of a given color of a player along a path
        """
        if not counter or \
                not self.is_inBoard((x, y)) or \
                self.board[x][y] != Player.symbol:
            return 0
        return 1 + \
               (self.count_path_len(Player, (x + px, y + py), (px, py), counter - 1) if self.is_inBoard(
                   (x + px, y + py)) else 0)


    def checkWinningMove(self):
        """
        Function retrieves the last move made,
        and checks if that move won the game.  If so,
        it sets self.win to True, and sets value for
        final result.
        """
        last_Player = self.turn().opponent_color()  # Get the Player who just made a move in the previous step.
        if last_Player.isBlack:
            pos = self.black[-1]
        else:
            pos = self.white[-1]

        checklist = []
        depth = self.max_consecutive - 1

        for move in ((1, 0), (0, 1), (1, 1), (1, -1)):
            opp = tuple(map(lambda x: -x, move))
            checklist.append(1 + \
                             self.count_path_len(last_Player, tuple(sum(x) for x in zip(pos, move)), move, depth) + \
                             self.count_path_len(last_Player, tuple(sum(x) for x in zip(pos, opp)), opp, depth)
                             )
        if self.max_consecutive in checklist:
            self.final_result = "{0} wins!".format(str(last_Player))
            self.winner = str(last_Player)
            self.win = True
        elif len(self.black) + len(self.white) == self.size ** 2:
            self.win = True
            self.final_result = "It's a Draw"
            return