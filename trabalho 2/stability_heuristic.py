from constants import *
from mobility_heuristic import calculate_square_mobility

def is_edge(x,y):
    return (x == 0 or x == 7 or y == 0 or y == 7)

def is_adjacent_to_stable_edge_of_same_color(stability_board, board, row, col):
    adjacent_coords = [ [row-1, col-1], [row-1, col], [row-1, col+1], 
                        [row, col-1],                 [row, col+1],
                        [row+1, col-1], [row+1, col], [row+1, col+1]]

    result = False
    color = board[row][col]

    for coords in adjacent_coords:
        if (not coords[0] < 0) and (not coords[0] > 7) and (not coords[1] < 0) and (not coords[1] > 7):
            if is_edge(coords[0], coords[1]):
                if stability_board[coords[0]][coords[1]] == True:
                    result = True
                    break

    return result

def is_between_two_of_opposing_color(board, row, col):
    color = board[row][col]
    if color == blackChar: op_color = whiteChar
    else: op_color = blackChar

    res = False

    #é beirada esquerda ou direita, temos que conferir verticalmente
    if row == 0 or row == 7:
        found_op_color_up = False
        colA = col - 1
        while colA >= 0 and board[row][colA] != empty:
            if board[row][colA] == op_color:
                found_op_color_up = True
                break
            colA -= 1
        if found_op_color_up:
            found_op_color_down = False
            colA = col + 1
            while colA <= 7 and board[row][colA] != empty:
                if board[row][colA] == op_color:
                    found_op_color_down = True
                    break
                colA += 1
            if found_op_color_down: res = True

    #é beirada superior ou inferior, temos que conferir horizontalmente
    elif col == 0 or col == 7:
        found_op_color_right = False
        rowA = row - 1
        while rowA >= 0 and board[rowA][col] != empty:
            if board[rowA][col] == op_color:
                found_op_color_right = True
                break
            rowA -= 1
        if found_op_color_right:
            found_op_color_left = False
            rowA = row + 1
            while rowA <= 7 and board[rowA][col] != empty:
                if board[rowA][col] == op_color:
                    found_op_color_left = True
                    break
                rowA += 1
            if found_op_color_left: res = True
        
    return res

def is_semi_stable(color, board, row, column):
    if color == blackChar: other_color = whiteChar
    else: other_color = blackChar
    return not calculate_square_mobility(other_color,board,row,column)

def is_le_edge_full(board):
    res = True
    for index in range(8):
        if board[0][index] == empty:
            res = False
            break
    return res

def is_r_edge_full(board):
    res = True
    for index in range(8):
        if board[7][index] == empty:
            res = False
            break
    return res

def is_u_edge_full(board):
    res = True
    for index in range(8):
        if board[index][0] == empty:
            res = False
            break
    return res

def is_l_edge_full(board):
    res = True
    for index in range(8):
        if board[index][7] == empty:
            res = False
            break
    return res

def internal_stability(board, stability_board, row, col):
    vertical_stability = False
    horizontal_stability = False
    diag1_stability = False
    diag2_stability = False

    #check vertical stability
    vertical_stability = (stability_board[row][col-1] and board[row][col-1] == board[row][col]) or (stability_board[row][col+1] and board[row][col+1] == board[row][col])
    #se não conseguirmos estabilidade por estável adjacente da mesma cor, vamos conferir se a coluna está cheia
    if not vertical_stability:
        vertical_stability = True
        for index in range(8):
            if board[row][index] == empty:
                vertical_stability = False
                return False

    #check horizontal stability
    horizontal_stability = (stability_board[row-1][col] and board[row-1][col] == board[row][col]) or (stability_board[row+1][col] and board[row+1][col] == board[row][col])
    #se não conseguirmos estabilidade por estável adjacente, vamos conferir se a linha está cheia
    if not horizontal_stability:
        horizontal_stability = True
        for index in range(8):
            if board[index][col] == empty:
                horizontal_stability = False
                return False

    #check diagonal1 stability
    diag1_stability = (stability_board[row-1][col-1] and board[row-1][col-1] == board[row][col]) or (stability_board[row+1][col+1] and board[row+1][col+1] == board[row][col])
    #se não conseguirmos estabilidade por estável adjacente, vamos conferir se a diagonal está cheia
    if not diag1_stability:
        diag1_stability = True
        diag_row = row+1
        diag_col = col+1
        while diag_row <= 7 and diag_col <= 7:
            if board[diag_row][diag_col] == empty:
                diag1_stability = False
                return False
            diag_row += 1
            diag_col += 1

        if diag1_stability:
            diag_row = row-1
            diag_col = col-1
            while diag_row >= 0 and diag_col >= 0:
                if board[diag_row][diag_col] == empty:
                    diag1_stability = False
                    return False
                diag_row -= 1
                diag_col -= 1

    #check diagonal2 stability
    diag2_stability = (stability_board[row-1][col+1] and board[row-1][col+1] == board[row][col]) or (stability_board[row+1][col-1] and board[row+1][col-1] == board[row][col])
    #se não conseguirmos estabilidade por estável adjacente, vamos conferir se a diagonal está cheia
    if not diag2_stability:
        diag2_stability = True
        diag_row = row-1
        diag_col = col+1
        while diag_row >= 0 and diag_col <= 7:
            if board[diag_row][diag_col] == empty:
                diag2_stability = False
                return False
            diag_row -= 1
            diag_col += 1

        if diag2_stability:
            diag_row = row+1
            diag_col = col-1
            while diag_row <= 7 and diag_col >= 0:
                if board[diag_row][diag_col] == empty:
                    diag2_stability = False
                    return False
                diag_row += 1
                diag_col -= 1

    return vertical_stability and horizontal_stability and diag1_stability and diag2_stability

def calculate_stability(board, max_color, weight):
    stability_board = [ [ False for i in range(8) ] for j in range(8) ]

    max_stability = 0
    min_stability = 0

    if max_color == blackChar: min_color = whiteChar
    else: min_color = blackChar

    corner = 4
    stable = 1
    unstable = -1
    semi_stable = 0


    #primeiro decidimos se cada beirada está cheia ou não
    #em uma beirada cheia, todas as peças são estáveis, então
    #computar isso primeiro pode poupar trabalho
    is_left_edge_full = is_le_edge_full(board)
    is_right_edge_full = is_r_edge_full(board)
    is_upper_edge_full = is_u_edge_full(board)
    is_lower_edge_full = is_l_edge_full(board)


    if is_left_edge_full:
        for index in range(8):
            stability_board[0][index] = True

    if is_right_edge_full:
        for index in range(8):
            stability_board[7][index] = True

    if is_upper_edge_full:
        for index in range(8):
            stability_board[index][0] = True

    if is_lower_edge_full:
        for index in range(8):
            stability_board[index][7] = True


    #passamos pelos 4 cantos, vendo se estão ocupados. Se um canto estiver ocupado, ele é automaticamente estável
    #um canto estável estabiliza as peças das beiradas adjacentes ao canto, se estiverem em uma string ininterrupta
    
    #CANTO 0,0
    if board[0][0] != empty:
        stability_board[0][0] = True
        if board[0][0] == max_color: max_stability += corner
        else: min_stability += corner

        i = 1
        while i <= 7 and board[0][i] != empty and board[0][i] == board[0][0]:
            stability_board[0][i] = True
            i += 1

        i = 1
        while i <= 7 and board[i][0] != empty and board[i][0] == board[0][0]:
            stability_board[i][0] = True
            i += 1

    #CANTO 0,7
    if board[0][7] != empty:
        stability_board[0][7] = True

        if board[0][7] == max_color: max_stability += corner
        else: min_stability += corner

        i = 6
        while i >= 0 and board[0][i] != empty and board[0][i] == board[0][7]:
            stability_board[0][i] = True
            i -= 1

        i = 1
        while i <= 7 and board[i][7] != empty and board[i][7] == board[0][7]:
            stability_board[i][7] = True
            i += 1

    #CANTO 7,0
    if board[7][0] != empty:
        stability_board[7][0] = True

        if board[7][0] == max_color: max_stability += corner
        else: min_stability += corner

        i = 6
        while i >= 0 and board[i][0] != empty and board[i][0] == board[7][0]:
            stability_board[i][0] = True
            i -= 1

        i = 1
        while i <= 7 and board[7][i] != empty and board[7][i] == board[7][0]:
            stability_board[7][i] = True
            i += 1

    #CANTO 7,7
    if board[7][7] != empty:
        stability_board[7][7] = True

        if board[7][7] == max_color: max_stability += corner
        else: min_stability += corner

        i = 6
        while i >= 0 and board[i][7] != empty and board[i][7] == board[7][7]:
            stability_board[i][7] = True
            i -= 1

        i = 6
        while i >= 0 and board[7][i] != empty and board[7][i] == board[7][7]:
            stability_board[7][i] = True
            i -= 1

    #depois de resolvidos os cantos, vamos ver as outras peças da beirada

    #BEIRADA ESQUERDA
    if not is_left_edge_full:
        for index in range (1,7):
            if not stability_board[0][index] and board[0][index] != empty:
                #CHECK IF STABLE
                if is_adjacent_to_stable_edge_of_same_color(stability_board, board, 0, index) or is_between_two_of_opposing_color(board, 0, index):
                    stability_board[0][index] = True

                #CHECK IF SEMI-STABLE    
                elif is_semi_stable(board[0][index], board, 0, index):
                    if board[0][index] == max_color: max_stability += semi_stable
                    else: min_stability += semi_stable

    #BEIRADA DIREITA
    if not is_right_edge_full:
        for index in range (1,7):
            if not stability_board[7][index] and board[7][index] != empty:
                #CHECK IF STABLE
                if is_adjacent_to_stable_edge_of_same_color(stability_board, board, 7, index) or is_between_two_of_opposing_color(board, 7, index):
                    stability_board[7][index] = True

                #CHECK IF SEMI-STABLE    
                elif is_semi_stable(board[7][index], board, 7, index):
                    if board[7][index] == max_color: max_stability += semi_stable
                    else: min_stability += semi_stable

    #BEIRADA SUPERIOR
    if not is_upper_edge_full:
        for index in range (1,7):
            if not stability_board[index][0] and board[index][0] != empty:
                #CHECK IF STABLE
                if is_adjacent_to_stable_edge_of_same_color(stability_board, board, index, 0) or is_between_two_of_opposing_color(board, index, 0):
                    stability_board[index][0] = True

                #CHECK IF SEMI-STABLE    
                elif is_semi_stable(board[index][0], board, index, 0):
                    if board[index][0] == max_color: max_stability += semi_stable
                    else: min_stability += semi_stable

    #BEIRADA INFERIOR
    if not is_lower_edge_full:
        for index in range (1,7):
            if not stability_board[index][7] and board[index][7] != empty:
                #CHECK IF STABLE
                if is_adjacent_to_stable_edge_of_same_color(stability_board, board, index, 7) or is_between_two_of_opposing_color(board, index, 7):
                    stability_board[index][7] = True

                #CHECK IF SEMI-STABLE    
                elif is_semi_stable(board[index][7], board, index, 7):
                    if board[index][7] == max_color: max_stability += semi_stable
                    else: min_stability += semi_stable
    
    
    #calculada a estabilidade das bordas, vamos para as peças internas
    #Para serem estáveis, precisam, para cada uma das 4 direções (vert, horiz, diag1 e diag2)
    #ter uma peça estável OU estar em uma linha cheia naquela direção
    
    #estabilidade interna só existe se pelo menos uma dessas casas está ocupada:
    if board[0][0] != empty or board[0][1] != empty or board[1][0] != empty or board[0][7] != empty or board[0][6] != empty or board[1][7] != empty or board[7][0] != empty or board[7][1] != empty or board[6][0] != empty or board[7][7] != empty or board[7][6] != empty or board[6][7] != empty:
        
        # Temos que calcular a estabilidade interna em espiral, assim considerando a estabilidade
        #das bordas que calculamos anteriormente
        top = 1
        bottom = 6
        left = 1
        right = 6

        # Defining the direction in which the array is to be traversed.
        dir = 0
        reverse = False
    

        while (top <= bottom and left <=right):    
            if dir ==0:
                if not reverse:
                    for col in range(left,right+1): # moving left->right
                        if board[top][col] != empty:
                            if internal_stability(board,stability_board,top,col):
                                #É ESTÁVEL
                                stability_board[top][col] = True
                            elif is_semi_stable(board[top][col], board, top, col):
                                #É SEMI-ESTÁVEL
                                if board[top][col] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                    
                else:
                    for col in range(right, left-1, -1): # moving right->left
                        if board[top][col] != empty:
                            if internal_stability(board,stability_board,top,col):
                                #É ESTÁVEL
                                stability_board[top][col] = True
                            elif is_semi_stable(board[top][col], board, top, col):
                                #É SEMI-ESTÁVEL
                                if board[top][col] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                    top +=1
                dir = 1

            elif dir ==1:
                if not reverse:
                    for row in range(top,bottom+1): # moving top->bottom
                        if board[row][right] != empty:
                            if internal_stability(board,stability_board,row,right):
                                #É ESTÁVEL
                                stability_board[row][right] = True
                            elif is_semi_stable(board[row][right], board, row, right):
                                #É SEMI-ESTÁVEL
                                if board[row][right] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                else:
                    for row in range(bottom, top-1, -1): # moving bottom->top
                        if board[row][right] != empty:
                            if internal_stability(board,stability_board,row,right):
                                #É ESTÁVEL
                                stability_board[row][right] = True
                            elif is_semi_stable(board[row][right], board, row, right):
                                #É SEMI-ESTÁVEL
                                if board[row][right] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                    right -=1 
                dir = 2
                
            elif dir ==2:
                if not reverse:
                    for col in range(left-1,-1): # moving right->left
                        if board[bottom][col] != empty:
                            if internal_stability(board,stability_board,bottom,col):
                                #É ESTÁVEL
                                stability_board[bottom][col] = True
                            elif is_semi_stable(board[bottom][col], board, bottom, col):
                                #É SEMI-ESTÁVEL
                                if board[bottom][col] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                else:
                    for col in range(left, right+1): # moving left->right
                        if board[bottom][col] != empty:
                            if internal_stability(board,stability_board,bottom,col):
                                #É ESTÁVEL
                                stability_board[bottom][col] = True
                            elif is_semi_stable(board[bottom][col], board, bottom, col):
                                #É SEMI-ESTÁVEL
                                if board[bottom][col] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                    bottom -=1
                dir = 3
                
            elif dir ==3:
                if not reverse:
                    for row in range(bottom,top-1,-1): # moving bottom->top
                        if board[row][left] != empty:
                            if internal_stability(board,stability_board,row,left):
                                #É ESTÁVEL
                                stability_board[row][left] = True
                            elif is_semi_stable(board[row][left], board, row, left):
                                #É SEMI-ESTÁVEL
                                if board[row][left] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                    reverse = True
                else:
                    for row in range(top,bottom+1): # moving top->bottom
                        if board[row][left] != empty:
                            if internal_stability(board,stability_board,row,left):
                                #É ESTÁVEL
                                stability_board[row][left] = True
                            elif is_semi_stable(board[row][left], board, row, left):
                                #É SEMI-ESTÁVEL
                                if board[row][left] == max_color: max_stability += semi_stable
                                else: min_stability += semi_stable
                    left +=1
                    reverse = False
                dir = 0
        



    #agora que já populamos o tabuleiro de estabilidade, basta computar os valores da heurística
    for row in range(8):
        for col in range(8):
            if stability_board[row][col]: #se for estável
                if board[row][col] == max_color: max_stability += stable
                else: min_stability += stable

    stability_heuristic = 0

    if (max_stability + min_stability) != 0:
        stability_heuristic = weight * (max_stability-min_stability)/(max_stability+min_stability)

    return stability_heuristic