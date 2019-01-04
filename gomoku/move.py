import Queue


def calculate_score(board, position, attack):
    """
    This function takes a board, and a position on that board,
    and evaluates the importance of that position on
    the board. It does so by evaluating the number of
    ways that that position can be used to get to winning state.
    If attack = True, the function evaluates the attack power of the position
    for whoever's turn it is; if attack = False, the function evaluates the attack power
    for the other player.
    """
    (x, y) = position
    if attack:
        color = board.turn()
    else:
        color = board.turn().opponent_color()

    total_score = 0

    for pair in ((1, 0), (0, 1), (1, 1), (1, -1)):
        (dx, dy) = pair
        pathlist = ["."]
        # When sign = 1, we are going on the right upper direction
        # When sign = -1, we are going on the left lower direction
        for sign in (1, -1):
            for i in range(1, board.max_consecutive):
                # Get the new coordinates:
                new_x = x + dx * i * sign
                new_y = y + dy * i * sign
                if not board.is_inBoard((new_x, new_y)):
                    break
                else:
                    occupied_by_opponent = (board[new_x][new_y] == color.opponent_color().symbol)
                    overline = (i + 1 == board.max_consecutive and \
                                board.is_inBoard((new_x + dx * sign, new_y + dy * sign)) and \
                                board[new_x + dx * sign][new_y + dy * sign] == color.symbol)
                    if occupied_by_opponent or overline:
                        break
                    else:
                        if sign > 0:
                            pathlist.append(board[new_x][new_y])
                        elif sign < 0:
                            pathlist.insert(0, board[new_x][new_y])
        # Get the number of ways you can make to winning state (max_consecutive points in a row)
        # using this position.
        num_ways_to_win = len(pathlist) - len(board) + 1
        if num_ways_to_win > 0:
            for i in range(num_ways_to_win):
                consec = pathlist[i:i + board.max_consecutive].count(color.symbol)
                if consec != board.max_consecutive - 1:
                    # If we haven't reached winning move yet, the score will be given
                    # based on the number of consecutive symbols for this particular way,
                    total_score += consec ** 6
                else:
                    # If this way leads to a win, we give extremely high score.
                    # However, we give a slightly higher score for a move if you are trying to reach a win
                    # rather than prevent a win from your opponent
                    if attack:
                        total_score += 10 ** 11
                    else:
                        total_score += 10 ** 10
    return total_score


def evaluate_function(board, position):
    """
    The importance of a position is evaluated as the sum of its attack power and its defense power, which
    also mean the sum of its attack power and its opponent's attack power.
    If input is an invalid move, return 0.
    """
    if board.is_valid_move(position):
        return calculate_score(board, position, True) + calculate_score(board, position, False)
    else:
        return 0


def connect_zone((x, y), max_consecutive):
    """
    Takes a coordinate, and returns a list of the coordinates
    within max_consecutive spaces of (x,y) that could make
    consecutive vertical, horizontal and diagonal path.
    """
    area = []
    for pair in ((1, 0), (0, 1), (1, 1), (1, -1)):
        (dx, dy) = pair
        for s in (1, -1):
            for i in range(1, max_consecutive):
                new_x = x + dx * i * s
                new_y = y + dy * i * s
                area.append((new_x, new_y))
    return area


def firstMove(board):
    """
    If the AI goes first, it will
    pick the middle position by default
    """
    x = board.size // 2
    return (x, x)


def secondMove(board):
    """
    If the AI must go second, it will go diagonal
    adjacent to the first placed tile (on the side
    that has larger area on the board)
    """
    (first_x, first_y) = board.black[0]
    if first_x <= board.size / 2:
        dx = 1
    else:
        dx = -1

    if first_y <= board.size / 2:
        dy = 1
    else:
        dy = -1
    return (first_x + dx, first_y + dy)


def nextMove(board, no_of_best_moves=10, max_depth=20):
    """
    If it was not the first move of the robot, we utilize
    quiescent search to find the next best move.
    Returns a move where quiescent search predicts a win, or
    the best move according to evaluate_function()
    """

    # NO_OF_BEST_MOVES = 10
    NO_OF_BEST_MOVES = no_of_best_moves
    # The larger the depth, the longer it takes for AI to make the move.
    MAX_DEPTH = max_depth
    neutral_list = []
    other_list = []

    # Using degree heuristics, find the top 10 number of moves based on their evaluation scores
    ranked_queue = Queue.PriorityQueue()
    spots = set()
    for t in board.black + board.white:
        for m in connect_zone(t, len(board)):
            if board.is_inBoard(m):
                spots.add(m)
    for r in spots:
        ranked_queue.put((evaluate_function(board, r) * (-1), r))
    toplist = []
    for x in range(NO_OF_BEST_MOVES):
        toplist.append(ranked_queue.get())

    top_moves = map(lambda (x, y): (-x, y), toplist)

    # Run search on those top moves:
    for atom in top_moves:
        (val, move) = atom
        nextboard = board.move(move)
        if nextboard.win:
            # If this move immediately followed by a win, return the move
            return move
        else:
            # If this this move is not immediately followed by a win, do quiescent search
            # after each recursion the depth is reduced by 1
            score = -search(nextboard, MAX_DEPTH - 1)
        if score == 1:
            # If this move finally leads to a win based on quiescent search, return the move
            return move
        elif score == 0:
            neutral_list.append((score, move))
        elif score > -1:
            other_list.append((score, move))
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
    # Get the best move at each recursion of search.
    ranked_queue = Queue.PriorityQueue()
    spots = set()
    for t in board.black + board.white:
        for m in connect_zone(t, len(board)):
            if board.is_inBoard(m):
                spots.add(m)
    for r in spots:
        ranked_queue.put((evaluate_function(board, r) * (-1), r))
    top_one = ranked_queue.get()
    bestmove = top_one[1]
    newboard = board.move(bestmove)
    if newboard.win:
        # Return 1 if the end state is a winning state
        return 1
    elif not max_depth:
        # Return 0 if max_depth is reached before finding an end state
        return 0
    else:
        # If not, continue to recurse
        return -search(newboard, max_depth - 1)