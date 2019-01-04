
import game


if __name__ == "__main__":
    print("------------------------------------------")
    print("             Welcome to Gomoku            ")
    print("------------------------------------------")

    print("Please choose a playing mode:              ")
    print("1. Computer vs Computer                    ")
    print("2. Human vs Computer")
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
            print("Invalid choice")
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
                print("Invalid choice")
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
            max_consecutive = int(
                raw_input("Please input a positive integer for length of consecutive points to win: "))
            break;
        except ValueError:
            print("Invalid max_consecutiveion Length")
            continue;

    game.game(board_size, max_consecutive, computer_first, mode)

# print (game_for_sim(10,5,10,10)[0])


