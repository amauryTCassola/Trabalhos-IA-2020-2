from constants import *
import numpy as np

def coin_count(current_state, char):
    return np.count_nonzero(current_state == char)

def coin_parity_heuristic(board, color_max, weight):
    if color_max == blackChar: color_min = whiteChar
    else: color_min = blackChar

    max_coins = coin_count(board, color_max)
    min_coins = coin_count(board, color_min)

    return weight*(max_coins - min_coins)/(max_coins + min_coins)