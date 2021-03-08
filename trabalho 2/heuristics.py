from constants import *
from mobility_heuristic import mobility_heuristic
from potential_mob_heuristic import potential_mobility_heuristic
from coin_parity_heuristic import coin_parity_heuristic
from stability_heuristic import calculate_stability
from static_heuristic import get_static_heuristic

def heuristics(state, color_max, is_static):

    board = state.tabuleiro

    if color_max == black: color_max = blackChar
    else: color_max = whiteChar

    if is_static:
        return get_static_heuristic(board,color_max)

    else:
        return calculate_stability(board, color_max, 30) + mobility_heuristic(board, color_max, 5) + potential_mobility_heuristic(board, color_max, 5) + coin_parity_heuristic(board, color_max, 25)