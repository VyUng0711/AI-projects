import game
import matplotlib.pylab as plt


def simulation_depths():
    board_size = 10
    max_consecutive = 5
    list_max_depths = (10,20,30,40,50)
    times = []
    for i in list_max_depths:
        this_game_time = game.game_for_sim(board_size, max_consecutive, 10, i)[0]
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
    list_n_of_best_moves = (5,10,15,20,25)
    times = []
    for i in list_n_of_best_moves:
        this_game_time = game.game_for_sim(board_size, max_consecutive, i, 20)[0]
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
