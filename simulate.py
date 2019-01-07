# import main
import sys
import globVar
import Player
import utils
import board
import Canvas
from multiprocessing import Pool, Process, Value, Queue, Lock, cpu_count
import os
import colors

W_victories = 0
b_victories = 0
N = 0

def run(total_num_moves, games_played, W_v, b_v, lock, i):
    # lock.acquire()
    # draw_status(i, N)
    # draw_score(i, W_v, b_v, total_num_moves, games_played)
    # lock.release()

    board.populate()
    playing = True
    while playing:
        if (globVar.playerCount % 2) == 0:
            globVar.player = "W"
        else:
            globVar.player = "b"

        Player.turn()
        globVar.playerCount += 1
        playing = not utils.checkWin()

        # lock.acquire()
        # progress(games_played)
        # # print(".", flush = True, end = "")
        # # print(name, flush = True, end = "")
        # lock.release()
        total_num_moves.value += 1
    games_played.value += 1
    W_v.value += W_victories
    b_v.value += b_victories
    lock.acquire()
    progress(games_played)
    lock.release()

def begin(n):
    set_globals()
    global N
    N = n
    W_v = Value('i', 0)
    b_v = Value('i', 0)
    total_num_moves = Value('i', 0)
    games_played = Value('i', 0)
    lock = Lock()

    procs = []
    for i in range(int(n)):
        procs.append(Process(target = run, args = (total_num_moves, games_played, W_v, b_v, lock, i)))

    progress(games_played)

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    Canvas.clear()
    print("\n Done! Below is the final score.")
    draw_score(int(n) - 1, W_v, b_v, total_num_moves, games_played)

def draw_status(i, n):
    Canvas.clear()
    print("\n Running simulation " + str(i + 1) + " of " + str(n) + ".")

def progress(games_played):
    Canvas.clear()
    title = "PROGRESS"
    buffer = int(os.get_terminal_size().columns / 2) - int(len(title) / 2)
    print("\n", end = "")
    for i in range(buffer):
        print(" ", end = "")
    print(colors.BOLD + title + colors.RESET)

    length = int((os.get_terminal_size().columns - 2) / 2)
    r_complete = games_played.value / int(N)
    num_to_draw = int(r_complete * length)

    print("\n " + colors.BRIGHT_GREEN_BG, end = "")
    for i in range(num_to_draw):
        print("  ", end = "")
    print(colors.RESET + colors.DULL_WHITE_BG, end = "")
    for i in range(length - num_to_draw):
        print("  ", end = "")
    print(colors.RESET)

    print("\n " + str(round(100 * r_complete, 2)) + "% ( " + str(games_played.value) + " / " + str(N) + " ) completed." )

def draw_score(i, W_v, b_v, total_num_moves, games_played):
    print("\n WHITE : " + str(W_v.value) + "  |  ", end = "")
    print("BLACK : " + str(b_v.value))
    total = int(W_v.value) + int(b_v.value)
    if total == 0:
        print("   0.0%           0.0%")
    else:
        W_r = round(((W_v.value / total) * 100), 2)
        b_r = round(((b_v.value / total) * 100), 2)
        print("   " + str(W_r) + "%", end = "")
        print("         " + str(b_r) + "%")

    print("\n Average number of moves: ", end = "")
    if i == 0:
        print(total_num_moves.value)
    else:
        avg_moves = round(total_num_moves.value / int(N), 2)
        print(avg_moves)
    print("\n Played " + str(games_played.value) + " games.")


def set_globals():
    globVar.simulation = True
    globVar.numPlayers = 0
    globVar.slow_speed = False
    globVar.ready = True

if __name__ == "__main__":
    set_globals()
    run()
