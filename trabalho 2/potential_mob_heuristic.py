from constants import *

def check_if_empty(board, row, column):
    if row < 0 or row > 7 or column < 0 or column > 7: return False
    else: return board[row][column] == empty

def num_frontier_discs(board, color):
    result = 0
    is_frontier_disc = False
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == color:
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if i != 0 or j != 0:
                            if check_if_empty(board, row+i, column+j): is_frontier_disc = True
                if is_frontier_disc: result += 1
                is_frontier_disc = False
                
    return result

def check_if_color(board, row, column, color):
    if row < 0 or row > 7 or column < 0 or column > 7: return False
    else: return board[row][column] == color

def num_empty_adjacent_to_discs(board, color):
    result = 0
    is_adjacent = False
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == empty:
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if i != 0 or j != 0:
                            if check_if_color(board, row+i, column+j, color): is_adjacent = True
                if is_adjacent: result += 1
                is_adjacent = False
    return result

#empty squares that are adjacent to more than one of the discs will be counted multiply -- once for each disc
def sum_empty_adjacent_to_each_disc(board, color):
    result = 0
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == color:
                for i in range(-1,2,1):
                    for j in range(-1,2,1):
                        if i != 0 or j != 0:
                            if check_if_empty(board, row+i, column+j): result += 1
    return result


def potential_mobility_heuristic(board, color_max, weight):
    if color_max == blackChar: color_min = whiteChar
    else: color_min = blackChar

    frontier_discs_max = num_frontier_discs(board, color_max)
    frontier_discs_min = num_frontier_discs(board, color_min)

    empty_adjacents_max = num_empty_adjacent_to_discs(board, color_max)
    empty_adjacents_min = num_empty_adjacent_to_discs(board, color_min)

    sum_empty_adjacents_max = sum_empty_adjacent_to_each_disc(board, color_max)
    sum_empty_adjacents_min = sum_empty_adjacent_to_each_disc(board, color_min)

    frontier_discs_h = weight*(frontier_discs_max - frontier_discs_min)/(frontier_discs_max + frontier_discs_min)
    empty_adjacents_h = weight*(empty_adjacents_max - empty_adjacents_min)/(empty_adjacents_max + empty_adjacents_min)
    sum_empty_adjacents_h = weight*(sum_empty_adjacents_max - sum_empty_adjacents_min)/(sum_empty_adjacents_max + sum_empty_adjacents_min)

    return frontier_discs_h + empty_adjacents_h + sum_empty_adjacents_h