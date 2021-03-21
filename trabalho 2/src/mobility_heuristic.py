from constants import *
import numpy as np

def check_line_match(who,dr,dc,r,c,board):
    if board[r][c] == who: return True

    if board[r][c] == empty: return False

    next_position_row = r+dr
    next_position_col = c+dc

    if next_position_row < 0 or next_position_row > 7: return False
    if next_position_col < 0 or next_position_col > 7: return False

    return check_line_match(who,dr,dc,next_position_row,next_position_col,board)

"""
    Dada uma posição no tabuleiro [row, column] e uma direção [delta_row, delta_column]
    partindo desta posição, checa se essa posição seria um movimento válido considerando
    a direção informada. Primeiro checa se nesta direção há uma peça do oponente adjacente
    e, se tiver, se, continuando em linha reta, eventualmente se chega a uma peça do jogador
    sem passar por espaços em branco, assim trancando as peças do oponente entre duas
    peças do jogador, o que configura uma jogada válida
    
"""
def valid_move(who,delta_row,delta_column,row,column,board):
    if who == blackChar: other = whiteChar
    else: other = blackChar

    next_position_row = row+delta_row
    next_position_col = column+delta_column

    '''checando se a posição seguinte não fica fora do tabuleiro'''
    if next_position_row < 0 or next_position_row > 7: return False
    if next_position_col < 0 or next_position_col > 7: return False

    '''checando se a próxima posição contém uma peça do oponente'''
    if board[next_position_row][next_position_col] != other: return False

    '''checando se a próxima posição não fica numa beirada do tabuleiro'''
    if next_position_row+delta_row < 0 or next_position_row+delta_row > 7: return False
    if next_position_col+delta_column < 0 or next_position_col+delta_column > 7: return False

    return check_line_match(who,delta_row,delta_column,next_position_row+delta_row,next_position_col+delta_column,board)

def calculate_square_mobility(who,board,row,column):
    nw = valid_move(who,-1,-1,row,column,board) #is it a valid move coming from north-west?
    nn = valid_move(who,-1, 0,row,column,board)#is it a valid move coming from north?
    ne = valid_move(who,-1, 1,row,column,board)#is it a valid move coming from north-east?

    sw = valid_move(who,1,-1,row,column,board)#mesma coisa pra south
    ss = valid_move(who,1, 0,row,column,board)
    se = valid_move(who,1, 1,row,column,board)

    e = valid_move(who,0, 1,row,column,board)#east
    w = valid_move(who,0,-1,row,column,board)#west

    return (nw or nn or ne or sw or ss or se or e or w)

def calculate_valid_moves(who,board):
    valid_moves_count = 0
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == empty:
                    if calculate_square_mobility(who,board,row,column):
                        valid_moves_count += 1
                    
    return valid_moves_count


def mobility_heuristic(board, color_max, weight):
    if color_max == blackChar: color_min = whiteChar
    else: color_min = blackChar

    max_mobility = calculate_valid_moves(color_max, board)
    min_mobility = calculate_valid_moves(color_min, board)
    
    if max_mobility + min_mobility != 0:
        return weight*(max_mobility - min_mobility)/(max_mobility + min_mobility)
    else: return 0