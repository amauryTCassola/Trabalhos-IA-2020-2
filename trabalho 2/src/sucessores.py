from constants import *
from estado_othello import *
from copy import deepcopy
import numpy as np
import time

def flip_line(who,dr,dc,r,c,board, depth):

    if (r+dr < 0) or (r + dr > 7): 
        return False
    elif (c+dc < 0) or (c+dc > 7): 
        return False
    elif board[r+dr][c+dc] == empty: 
        return False
    elif board[r+dr][c+dc] == who:
        if depth > 0:
            return True
        else: 
            return False
    elif flip_line(who,dr,dc,r+dr,c+dc,board, depth+1):
        
        board[r+dr][c+dc] = who

        return True
    else: return False

def execute_move(who,board,row,column):
    board[row][column] = who

    a = flip_line(who, -1, -1,row,column,board,0)

    b = flip_line(who, -1, 0,row,column,board,0)

    c = flip_line(who, -1, 1,row,column,board,0)


    d = flip_line(who, 0, -1,row,column,board,0)

    e = flip_line(who, 0, 1,row,column,board,0)

    f = flip_line(who, 1, -1,row,column,board,0)

    g = flip_line(who, 1, 0,row,column,board,0)

    h = flip_line(who, 1, 1,row,column,board,0)

    if (a or b or c or d or e or f or g or h) == False:
        board[row][column] = empty
        return False
    else: return True

def get_empty_adjacents(board,row,col):

    adjacent_coords = [ [row-1, col-1], [row-1, col], [row-1, col+1], 
                        [row, col-1],                 [row, col+1],
                        [row+1, col-1], [row+1, col], [row+1, col+1]]

    empty_adjacents = []

    for coords in adjacent_coords:
        if (not coords[0] < 0) and (not coords[0] > 7) and (not coords[1] < 0) and (not coords[1] > 7):
            if board[coords[0]][coords[1]] == empty:
                empty_adjacents.append((coords[0], coords[1]))

    return empty_adjacents


transposition_table = {}

def sucessores(estado, cor):

    global transposition_table
    key = cor+''.join(ele for sub in estado.tabuleiro for ele in sub)
    res = []

    if key in transposition_table:
        res =  transposition_table[key]
    else:
        if cor == blackChar: other_color = whiteChar
        else: other_color = blackChar

        sucessores_list = []
        tabuleiro = estado.tabuleiro

        moves_checked = {}

        new_board = np.copy(tabuleiro)

        for row in range(len(tabuleiro)):
            for column in range(len(tabuleiro[row])):
                if tabuleiro[row][column] == other_color:
                    empty_adjacents = get_empty_adjacents(tabuleiro,row,column)
                    for adj in empty_adjacents:
                        if not str((adj[0], adj[1])) in moves_checked:
                            if execute_move(cor,new_board,adj[0],adj[1]):
                                novo_estado = Estado_othello(new_board, (adj[0],adj[1]))
                                sucessores_list.append(novo_estado)
                                new_board = np.copy(tabuleiro)

                            moves_checked[str((adj[0], adj[1]))] = 0
        transposition_table[key] = sucessores_list
        res = sucessores_list
    return res