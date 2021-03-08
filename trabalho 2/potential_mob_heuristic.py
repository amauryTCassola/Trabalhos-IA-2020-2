from constants import *

def check_if_empty(board, row, column):
    if row < 0 or row > 7 or column < 0 or column > 7: return False
    else: return board[row][column] == empty

def check_if_color(board, row, column, color):
    if row < 0 or row > 7 or column < 0 or column > 7: return False
    else: return board[row][column] == color


def potential_mobility_heuristic(board, color_max, weight):
    if color_max == blackChar: color_min = whiteChar
    else: color_min = blackChar

    empty_adjacents_max = 0
    sum_empty_adjacents_max = 0
    frontier_discs_max = 0

    frontier_discs_min = 0
    empty_adjacents_min = 0
    sum_empty_adjacents_min = 0

    is_frontier_disc = False
    is_adjacent_max = False
    is_adjacent_min = False

    for row in range(len(board)):
        for column in range(len(board[row])):
            
            if board[row][column] == color_max:
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if i != 0 or j != 0:
                            if check_if_empty(board, row+i, column+j): 
                                sum_empty_adjacents_max += 1
                                is_frontier_disc = True
                if is_frontier_disc: frontier_discs_max += 1
                is_frontier_disc = False

            elif board[row][column] == color_min:
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if i != 0 or j != 0:
                            if check_if_empty(board, row+i, column+j): 
                                sum_empty_adjacents_min += 1
                                is_frontier_disc = True
                if is_frontier_disc: frontier_discs_min += 1
                is_frontier_disc = False
            else:
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if i != 0 or j != 0:
                            if check_if_color(board, row+i, column+j, color_max): 
                                is_adjacent_max = True
                            if check_if_color(board, row+i, column+j, color_min):
                                is_adjacent_min = True
                if is_adjacent_min: empty_adjacents_min += 1
                if is_adjacent_max: empty_adjacents_max += 1
                is_adjacent_max = False
                is_adjacent_min = False


    frontier_discs_h = weight*(frontier_discs_max - frontier_discs_min)/(frontier_discs_max + frontier_discs_min)
    empty_adjacents_h = weight*(empty_adjacents_max - empty_adjacents_min)/(empty_adjacents_max + empty_adjacents_min)
    sum_empty_adjacents_h = weight*(sum_empty_adjacents_max - sum_empty_adjacents_min)/(sum_empty_adjacents_max + sum_empty_adjacents_min)

    return frontier_discs_h + empty_adjacents_h + sum_empty_adjacents_h