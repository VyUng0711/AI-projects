import time
import ast

from move import firstMove
from move import secondMove
from move import nextMove

from board import Board


def game_for_sim(board_size, max_consecutive, no_of_best_moves, max_depth):
    board = Board(board_size, max_consecutive)
    move = firstMove(board)
    board = board.move(move)
    move = move.secondmove(board)
    board = board.move(move)
    while not board.win:
        t = time.time()
        move = move.nextMove(board, no_of_best_moves, max_depth)
        this_time = time.time() - t
        board.total_time += this_time
        board.total_moves += 1
        board = board.move(move)
    average_time = board.total_time / board.total_moves
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
        print("You choose computer moved first")
        move = firstMove(board)
    elif mode == True:
        move = firstMove(board)
    else:
        while True:
            try:
                move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                if not board.is_valid_move(move):
                    print("This spot has already been taken or not available in current board, please enter other move")
                else:
                    break
            except(ValueError, SyntaxError, TypeError):
                continue
    board = board.move(move)
    print("X moved {0}".format(move))

    if not computer_first or mode == True:
        move = secondMove(board)
    else:
        print(board)
        while True:
            try:
                move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                if not board.is_valid_move(move):
                    print("This spot has already been taken or not available in curent board, please enter other move")
                else:
                    break
            except(ValueError, SyntaxError, TypeError):
                continue
    board = board.move(move)
    print(board)
    print("O moved {0}".format(move))

    while not board.win:
        # Black Moves
        if computer_first or mode == True:
            t = time.time()
            move = nextMove(board, no_of_best_moves, max_depth)
            this_time = time.time() - t
            board.total_time += this_time
            board.total_moves += 1
            print('This move took: {} seconds'.format(this_time))
        else:
            while not board.win or not board.is_valid_move(move):
                try:
                    move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                    if not board.is_valid_move(move):
                        print(
                            "This spot has already been taken or not available in current board, please enter other move")
                    else:
                        break
                except (ValueError, SyntaxError, TypeError):
                    continue
        board = board.move(move)
        print(board)
        print("X moves {0}".format(move))

        if not computer_first or mode == True:
            t = time.time()
            move = nextMove(board, no_of_best_moves, max_depth)
            this_time = time.time() - t
            board.total_time += this_time
            board.total_moves += 1
            print('This move took: {} seconds'.format(time.time() - t))
        else:
            while not board.win or not board.is_valid_move(move):
                try:
                    move = ast.literal_eval(raw_input("Please enter your move in format '(x,y)': "))
                    if not board.is_valid_move(move):
                        print(
                            "This spot has already been taken or not available in current board, please enter other move")
                    else:
                        break
                except(ValueError, SyntaxError, TypeError):
                    continue
        board = board.move(move)
        print(board)
        print("O moves {0}".format(move))

    print("GAME'S OVER")
    print("Average time taken per move: {}".format(board.total_time / board.total_moves))
    average_time = board.total_time / board.total_moves
    winner = board.winner
    return (average_time, winner)
    # return (average_time)

