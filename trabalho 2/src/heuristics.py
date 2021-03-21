from constants import *
from mobility_heuristic import mobility_heuristic
from potential_mob_heuristic import potential_mobility_heuristic
from coin_parity_heuristic import coin_parity_heuristic
from stability_heuristic import calculate_stability
from static_heuristic import get_static_heuristic
from corners_heuristics import corners_heuristic
import time

def heuristics(state, color_max, is_static):

    board = state.tabuleiro

    if color_max == black: color_max = blackChar
    else: color_max = whiteChar

    #calculate_stability(board, color_max, 1) +

    m = mobility_heuristic(board, color_max, 1) + potential_mobility_heuristic(board, color_max, 1) + coin_parity_heuristic(board, color_max, 1) + corners_heuristic(board, color_max, 1)

    return m