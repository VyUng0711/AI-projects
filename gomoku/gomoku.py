import Queue as q
import time
import random
import copy
import ast
import matplotlib.pylab as plt

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
        return type(self)==type(other) and \
           self.color==other.color

    def __ne__(self,other): 
        return not (self == other)

    def __str__(self): 
        return self.color

    def __repr__(self): 
        return str(self)

    def opponent_color(self): 
        #Return the color of your opponent
        return Player(not self.isBlack)
        
class Board:
    """
    A class that defines the board
    for a game of gomoku
    """
    def __init__(self,size,max_consecutive):
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
        string+="                x axis         \n"
        string+="        _______________________\n"
        string+="          "
        for i in range(self.size):
            string+="{0}{1}".format(i%10, " " if i<10 else "'")
            #string+="{0}{1}".format(i, " ")
        string +="\n"
        i = 0

        for k in range(len(self.board[0])):
            if k == len(self.board[0])//2:
                string += "y axis |"
            else:
                string += "       |"
            string +="{0}{1}".format(i%10," " if i<10 else "'")
            i+=1
            for h in self.board:
                string+="{0} ".format(h[k])
            string+="\n"

        if self.win:
            string += self.final_result +"\n"
        return string

    def __len__(self): 
        """
        Return the number of consecutive points needed to win 
        """
        return self.max_consecutive \

    def __repr__(self): 
        return str(self)

    def __getitem__(self,num): 
        return self.board[num]

    def __eq__(self,other):
        return ( 
        type(self) == type(other) and \
        self.white == other.white and \
        self.black == other.black and \
        self.size  == other.size)

    def __ne__(self,other):
        return not (self == other)

    def turn(self): 
        #return the player whose current turn it is 
        return Player(len(self.black)==len(self.white))

    def is_valid_move(self, (x,y)):
        """
        Return True if the position is to an empty position.
        which means a move there would be valid.  
        Otherwise, return False
        """
        return self.is_inBoard((x,y)) and self.board[x][y] == "."


    def is_inBoard(self,(x,y)):
        """
        Return True if a position is in the board.
        Otherwise, return False 
        """
        return x >= 0 and \
               x < self.size and \
               y >= 0 and \
               y < self.size

    def move(self,(x,y)):
        """
        Return the updated board after a move is made. 

        """
        turn = self.turn()
        updated = copy.deepcopy(self)
        if self.win:
            #If the game has been won, simply return a copy of the previous state
            return updated
        #Else: we update the state board with that move. 
        updated.board[x][y] = turn.symbol
        if turn.isBlack:
            updated.black.append((x,y))
        else:
            updated.white.append((x,y))
        updated.checkWinningMove()
        return updated


    def count_path_len(self, Player, (x,y), (px,py), counter):
        """
        Returns the number of consecutive
        symbols of a given color of a player along a path
        """
        if not counter or \
           not self.is_inBoard((x,y)) or \
           self.board[x][y] != Player.symbol:
            return 0
        return 1 + \
    (self.count_path_len(Player,(x+px,y+py),(px,py),counter -1) if self.is_inBoard((x+px,y+py)) else 0)



    def checkWinningMove(self):
        """
        Function retrieves the last move made,
        and checks if that move won the game.  If so,
        it sets self.win to True, and sets value for
        final result.
        """
        last_Player = self.turn().opponent_color() #Get the Player who just made a move in the previous step.
        if last_Player.isBlack:
            pos = self.black[-1]
        else:
            pos = self.white[-1]

        checklist = []
        depth = self.max_consecutive -1

        for move in ((1,0),(0,1),(1,1),(1,-1)):
            opp = tuple(map(lambda x: -x, move))
            checklist.append(1 +\
                      self.count_path_len(last_Player,tuple(sum(x) for x in zip(pos,move)),move,depth) +\
                      self.count_path_len(last_Player,tuple(sum(x) for x in zip(pos,opp)), opp, depth)
                      )
        if self.max_consecutive in checklist:
            self.final_result = "{0} wins!".format(str(last_Player))
            self.winner = str(last_Player)
            self.win = True
        elif len(self.black)+len(self.white) == self.size**2:
            self.win = True
            self.final_result = "It's a Draw"
            return



def calculate_score(board,position,attack):
    """
    This function takes a board, and a position on that board,
    and evaluates the importance of that position on
    the board. It does so by evaluating the number of 
    ways that that position can be used to get to winning state.
    If attack = True, the function evaluates the attack power of the position 
    for whoever's turn it is; if attack = False, the function evaluates the attack power 
    for the other player. 
    """
    (x,y) = position
    if attack:
        color = board.turn()
    else:
        color = board.turn().opponent_color()

    total_score = 0
    
    for pair in ((1,0),(0,1),(1,1),(1,-1)):
        (dx,dy) = pair
        pathlist =["."]
        #When sign = 1, we are going on the right upper direction 
        #When sign = -1, we are going on the left lower direction 
        for sign in (1,-1):
            for i in range(1,board.max_consecutive):
                #Get the new coordinates:
                new_x = x+dx*i*sign 
                new_y = y+dy*i*sign 
                if not board.is_inBoard((new_x,new_y)):
                    break
                else: 
                    occupied_by_opponent = (board[new_x][new_y] == color.opponent_color().symbol)
                    overline = (i+1 == board.max_consecutive and \
                board.is_inBoard((new_x+dx*sign,new_y+dy*sign)) and \
                board[new_x+dx*sign][new_y+dy*sign] == color.symbol)
                    if occupied_by_opponent or overline:
                        break
                    else:
                        if sign>0:
                            pathlist.append(board[new_x][new_y])
                        elif sign<0:
                            pathlist.insert(0,board[new_x][new_y])
        #Get the number of ways you can make to winning state (max_consecutive points in a row)
        #using this position. 
        num_ways_to_win = len(pathlist) - len(board) + 1 
        if num_ways_to_win>0:
            for i in range(num_ways_to_win):
                consec = pathlist[i:i+board.max_consecutive].count(color.symbol)
                if consec != board.max_consecutive-1:
                    #If we haven't reached winning move yet, the score will be given 
                    #based on the number of consecutive symbols for this particular way, 
                    total_score += consec**6
                else:
                    #If this way leads to a win, we give extremely high score. 
                    #However, we give a slightly higher score for a move if you are trying to reach a win
                    #rather than prevent a win from your opponent
                    if attack:
                        total_score += 10**11
                    else:
                        total_score += 10**10
    return total_score


def evaluate_function(board,position):
    """
    The importance of a position is evaluated as the sum of its attack power and its defense power, which
    also mean the sum of its attack power and its opponent's attack power. 
    If input is an invalid move, return 0. 
    """
    if board.is_valid_move(position):
        return calculate_score(board,position,True)+calculate_score(board,position,False)
    else:
        return 0


def connect_zone((x,y), max_consecutive):
    """
    Takes a coordinate, and returns a list of the coordinates
    within max_consecutive spaces of (x,y) that could make 
    consecutive vertical, horizontal and diagonal path. 
    """
    area = []
    for pair in ((1,0),(0,1),(1,1),(1,-1)):
        (dx,dy) = pair
        for s in (1,-1):
            for i in range(1,max_consecutive):
                new_x = x+dx*i*s
                new_y = y+dy*i*s
                area.append((new_x,new_y))
    return area

       
def firstmove(board):
    """
    If the AI goes first, it will
    pick the middle position by default 
    """
    x = board.size//2
    return (x,x)


def secondmove(board):
    """
    If the AI must go second, it will go diagonal 
    adjacent to the first placed tile (on the side 
    that has larger area on the board)
    """
    (first_x,first_y) = board.black[0]
    if first_x <= board.size/2:
        dx = 1
    else: dx = -1

    if first_y <=board.size/2:
        dy = 1
    else: 
        dy = -1
    return (first_x+dx,first_y+dy)   

def nextMove(board, no_of_best_moves = 10, max_depth=20):
    """
    If it was not the first move of the robot, we utilize 
    quiescent search to find the next best move. 
    Returns a move where quiescent search predicts a win, or
    the best move according to evaluate_function()
    """

    #NO_OF_BEST_MOVES = 10
    NO_OF_BEST_MOVES = no_of_best_moves
    #The larger the depth, the longer it takes for AI to make the move. 
    MAX_DEPTH = max_depth
    neutral_list = []
    other_list = []

    # Using degree heuristics, find the top 10 number of moves based on their evaluation scores 
    ranked_queue = q.PriorityQueue()
    spots = set()
    for t in board.black+board.white:
        for m in connect_zone(t,len(board)):
            if board.is_inBoard(m):
                spots.add(m)
    for r in spots:
        ranked_queue.put((evaluate_function(board,r)*(-1),r))
    toplist = []       
    for x in range(NO_OF_BEST_MOVES):
        toplist.append(ranked_queue.get())

    top_moves = map(lambda (x,y): (-x,y), toplist)

    #Run search on those top moves: 
    for atom in top_moves:
        (val,move) = atom
        nextboard = board.move(move)
        if nextboard.win:
        #If this move immediately followed by a win, return the move 
            return move
        else:
        #If this this move is not immediately followed by a win, do quiescent search 
        #after each recursion the depth is reduced by 1
            score = -search(nextboard, MAX_DEPTH-1)
        if score ==1:
        #If this move finally leads to a win based on quiescent search, return the move
            return move
        elif score ==0:
            neutral_list.append((score,move))
        elif score > -1:
            other_list.append((score,move))
    if len(neutral_list): 
        return neutral_list[0][1]
    elif len(other_list):
        other_list.sort()
        return other_list[-1][1]
    else: 
        return top_moves[0][1]
  
def search(board, max_depth):
    """
    Performing search on a limited depth. 
    """
    #Get the best move at each recursion of search. 
    ranked_queue = q.PriorityQueue()
    spots = set()
    for t in board.black+board.white:
        for m in connect_zone(t,len(board)):
            if board.is_inBoard(m):
                spots.add(m)
    for r in spots:
        ranked_queue.put((evaluate_function(board,r)*(-1),r))
    top_one = ranked_queue.get()
    bestmove = top_one[1]
    newboard = board.move(bestmove)
    if newboard.win: 
        #Return 1 if the end state is a winning state
        return 1
    elif not max_depth: 
        #Return 0 if max_depth is reached before finding an end state
        return 0
    else:            
        #If not, continue to recurse
        return -search(newboard,max_depth-1)

def game_for_sim(board_size, max_consecutive, no_of_best_moves, max_depth):
    board = Board(board_size, max_consecutive)  
    move = firstmove(board)
    board = board.move(move)
    move = secondmove(board)
    board = board.move(move)
    while not board.win:
        t = time.time()
        move = nextMove(board, no_of_best_moves,max_depth)
        this_time = time.time() - t
        board.total_time += this_time
        board.total_moves += 1
        board = board.move(move)
    average_time = board.total_time/board.total_moves
    winner = board.winner
    return (average_time, winner) 


def game(board_size, max_consecutive, computer_first, mode, no_of_best_moves=10, max_depth=20):
    """
    board_size is the size of the board (typical is 15)
    max_consecutive is the number of max_consecutiveions needed to win (typical is 5) 
    computer_first is the indicator of whether AI moves first or human Player moves first in 
        a game between computer and human 
    mode is the playing mode, either computer vs computer or human vs computer
    no_of_best_moves is the number of best moves that would be chosen for further search in each step
    max_depth is the depth of search. 

    """
    

    board = Board(board_size, max_consecutive)
    print("X moves first")
    print(board)
    
    if computer_first: 
        print ("You choose computer moved first")
        move = firstmove(board)
    elif mode == True:
        move = firstmove(board)
    else:
        while True:
            try:
                move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                if not board.is_valid_move(move):
                    print ("This spot has already been taken or not available in current board, please enter other move")
                else:
                    break
            except(ValueError,SyntaxError,TypeError):
                continue
    board = board.move(move)
    print("X moved {0}".format(move))

    if not computer_first or mode == True:
        move = secondmove(board)
    else:
        print(board)
        while True:
            try:
                move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                if not board.is_valid_move(move):
                    print ("This spot has already been taken or not available in curent board, please enter other move")
                else:
                    break
            except(ValueError,SyntaxError,TypeError):
                continue
    board = board.move(move)
    print(board)
    print("O moved {0}".format(move))
    

    while not board.win:
        #Black Moves
        if computer_first or mode == True:
            t = time.time()
            move = nextMove(board, no_of_best_moves,max_depth)
            this_time = time.time() - t
            board.total_time += this_time
            board.total_moves += 1
            print('This move took: {} seconds'.format(this_time))
        else:
            while not board.win or not board.is_valid_move(move):
                try:
                    move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                    if not board.is_valid_move(move):
                        print ("This spot has already been taken or not available in current board, please enter other move")
                    else:
                        break
                except (ValueError,SyntaxError,TypeError):
                    continue
        board = board.move(move)
        print(board)
        print("X moves {0}".format(move))

        if not computer_first or mode == True:
            t= time.time()
            move = nextMove(board, no_of_best_moves, max_depth)
            this_time = time.time() - t
            board.total_time += this_time
            board.total_moves += 1
            print('This move took: {} seconds'.format(time.time() -t))
        else:
            while not board.win or not board.is_valid_move(move):
                try:
                    move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                    if not board.is_valid_move(move):
                        print ("This spot has already been taken or not available in current board, please enter other move")
                    else:
                        break
                except(ValueError,SyntaxError,TypeError):
                    continue
        board = board.move(move)
        print(board)
        print("O moves {0}".format(move))
 
    print("GAME'S OVER")
    print("Average time taken per move: {}". format(board.total_time/board.total_moves))
    average_time = board.total_time/board.total_moves
    winner = board.winner
    return (average_time, winner) 
    #return (average_time) 

if __name__=="__main__":
    print("------------------------------------------")
    print("             Welcome to Gomoku            ")
    print("------------------------------------------")

    print("Please choose a playing mode:              ")
    print("1. Computer vs Computer                    ")
    print("2. Human vs Computer"                       )
    print("")
    while True:
        try:
            i = int(input("Enter 1 or 2: "))
            if i == 1:
                mode = True
                break;
            elif i == 2:
                mode = False
                break;
        except ValueError:
            print ("Invalid choice")
            continue;

    if mode == 2:
        print("Please choose starting Player:             ")
        print(" 1. Computer can start first.                       ")
        print(" 2. I want to start first.                      ")
        while True:
            try:
                i = int(input("Enter 1 or 2: "))
                if i == 1:
                    computer_first = True
                    break;
                elif i == 2:
                    computer_first = False
                    break;
            except ValueError:
                print ("Invalid choice")
                continue;
    else:
        computer_first = False
    while True:
        try:
            board_size = int(raw_input("Please input a positive integer board size: "))
            break;
        except ValueError:
            print("Invalid Board Size")
            continue;

    while True:
        try:
            max_consecutive = int(raw_input("Please input a positive integer for length of consecutive points to win: "))
            break;
        except ValueError:
            print("Invalid max_consecutiveion Length")
            continue;

    
    game(board_size, max_consecutive, computer_first, mode)


#print (game_for_sim(10,5,10,10)[0])
def simulation_depths():
    board_size = 10
    max_consecutive = 5
    computer_first = False
    mode = True
    list_max_depths = (10,20,30,40,50)
    times = []
    for i in list_max_depths:
        this_game_time = game_for_sim(board_size, max_consecutive, 10, i)[0]
        times.append(this_game_time)
    print times
    plt.plot(list_max_depths, times)
    plt.title("Plot on how long a move is made given a specific depth of search")
    plt.xlabel("Depths of search")
    plt.ylabel("Average time per move")
    plt.show()



def simulation_options():
    board_size = 10
    max_consecutive = 5
    computer_first = False
    mode = True
    list_n_of_best_moves = (5,10,15,20,25)
    times = []
    for i in list_n_of_best_moves:
        this_game_time = game_for_sim(board_size, max_consecutive, i, 20)[0]
        times.append(this_game_time)
    print times
    plt.plot(list_n_of_best_moves, times)
    plt.title("Plot on how long a move is made given a specific number of best moves to choose from")
    plt.xlabel("Number of best moves")
    plt.ylabel("Average time per move")
    plt.show()


#simulation_who_wins()
#simulation_options()
#simulation_options()
#print game(10, 5, False, True, 10, 50)[1]


