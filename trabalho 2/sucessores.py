from constants import *
from estado_othello import *
from copy import deepcopy

def flip_line(who,dr,dc,r,c,board):
    #print("flip line")
    #print("(r+dr, c+dc): ("+str(r+dr)+", "+str(c+dc)+")")
    #print("conteudo: "+str(board[r+dr][c+dc]))
    #input()
    
    
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

    
    if not (flip_line(who, -1, -1,row,column,board) or
            flip_line(who, -1, 0,row,column,board) or
            flip_line(who, -1, 1,row,column,board) or
            flip_line(who, 0, -1,row,column,board) or
            flip_line(who, 0, 1,row,column,board) or
            flip_line(who, 1, -1,row,column,board) or
            flip_line(who, 1, 0,row,column,board) or
            flip_line(who, 1, 1,row,column,board)):
        row_content = board.pop(row)
        row_content[column] = empty
        board.insert(row,row_content)
        return False
    return True

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

def get_velocity_between(x1,y1,x2,y2):
    xv = 0
    if x1 != x2:
        if x1 > x2:
            xv = -1
        else:
            xv = 1
    
    yv = 0
    if y1 != y2:
        if y1 > y2:
            yv = -1
        else:
            yv = 1

    return (xv,yv)

def sucessores(estado, cor):
    if cor == blackChar: other_color = whiteChar
    else: other_color = blackChar

    sucessores_list = []
    tabuleiro = estado.tabuleiro
    for row in range(len(tabuleiro)):
        for column in range(len(tabuleiro[row])):
            if tabuleiro[row][column] == other_color:
                empty_adjacents = get_empty_adjacents(tabuleiro,row,column)
                #print("cor: "+str(cor))
                #print("branca: "+str((row,column)))
                new_board = deepcopy(tabuleiro)
                for adj in empty_adjacents:
                    (dx,dv) = get_velocity_between(adj[0],adj[1],row,column)
                    #print(str((dx,dv)))
                    new_board = deepcopy(tabuleiro)

                    #print("espaço: ("+str(adj[0])+", "+str(adj[1])+")")
                    if flip_line(cor, dx, dv, adj[0], adj[1], new_board):
                        #print("VALIDO")
                        #input()
                        novo_estado = Estado_othello(estado, new_board, (adj[0],adj[1]), 0)
                        sucessores_list.append(novo_estado)

    return sucessores_list