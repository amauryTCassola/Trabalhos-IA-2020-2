from constants import *
from estado_othello import *
from copy import deepcopy

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

def flip_line(who,dr,dc,r,c,board):
    if (r+dr < 0) or (r + dr > 7): 
        return False
    elif (c+dc < 0) or (c+dc > 7): 
        return False
    elif board[r+dr][c+dc] == empty: 
        return False
    elif board[r+dr][c+dc] == who: 
        return True
    elif flip_line(who,dr,dc,r+dr,c+dc,board):
        row = board.pop(r+dr)
        row[c+dc] = who
        board.insert(r+dr,row)
        return True
    else: return False

def execute_move(who,board,row,column):
    row_content = board.pop(row)
    row_content[column] = who
    board.insert(row,row_content)

    
    flip_line(who, -1, -1,row,column,board)
    flip_line(who, -1, 0,row,column,board)
    flip_line(who, -1, 1,row,column,board)
    
    flip_line(who, 0, -1,row,column,board)
    flip_line(who, 0, 1,row,column,board)

    flip_line(who, 1, -1,row,column,board)
    flip_line(who, 1, 0,row,column,board)
    flip_line(who, 1, 1,row,column,board)

def sucessores(estado, cor):
    sucessores_list = []
    tabuleiro = estado.tabuleiro
    for row in range(len(tabuleiro)):
        for column in range(len(tabuleiro[row])):
            if tabuleiro[row][column] == empty:
                if calculate_square_mobility(cor,tabuleiro,row,column):
                    new_board = deepcopy(tabuleiro)
                    execute_move(cor, new_board, row, column)
                    novo_estado = Estado_othello(estado, new_board, (row,column), 0)
                    sucessores_list.append(novo_estado)
    return sucessores_list