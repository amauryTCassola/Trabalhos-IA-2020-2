from constants import *
import numpy as np

static_board = np.array([[ 4, -3,  2,  2,  2,  2, -3,  4],
                [-3, -4, -1, -1, -1, -1, -4, -3],
                [ 2, -1,  1,  0,  0,  1, -1,  2],
                [ 2, -1,  0,  1,  1,  0, -1,  2],
                [ 2, -1,  0,  1,  1,  0, -1,  2],
                [ 2, -1,  1,  0,  0,  1, -1,  2],
                [-3, -4, -1, -1, -1, -1, -4, -3],
                [ 4, -3,  2,  2,  2,  2, -3,  4]])



def get_static_heuristic(board,max_color):
    static_max = 0
    static_min = 0
    
    if max_color == blackChar: min_color = whiteChar
    else: min_color = blackChar

    for row in range(8):
        for col in range(8):
            if board[row][col] == max_color:
                static_max += static_board[row][col]
            elif board[row][col] == min_color:
                static_min += static_board[row][col]

    return static_max - static_min