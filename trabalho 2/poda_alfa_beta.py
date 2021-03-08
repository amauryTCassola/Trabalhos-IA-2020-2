import sys
from tabuleiro_utils import *
from heuristics import heuristics
import heapq
from sucessores import sucessores
from constants import *

#TRANSPOSITION TABLE
#dict de estados já encontrados, pra n precisar avaliar eles de novo
transposition_table = {}

color_max = ""
color_min = ""
is_static = None
successores_estado_atual = []

#for(int distance = 1; distance < MAX_DISTANCE && !outOfTime(); distance++) {
#  bestmove = alphaBetaAtRoot(position, distance);
#}
#play(bestmove);

def teste_de_corte(cur_depth, max_depth):
    return cur_depth == max_depth

def decisao_minimax_alfa_beta(estado, profundidade):
    (v, x, y) = valor_max(estado,neg_infinity,pos_infinity,0,profundidade) 
    return (x,y)

def valor_max(estado, alfa, beta, cur_depth, max_depth):
    px = None
    py = None
    
    if teste_de_corte(cur_depth, max_depth):
        return (avalia(estado), estado.movimento[0], estado.movimento[1])
    for s in sucessores(estado, color_max):
        (min_v, min_x, min_y) = valor_min(s,alfa,beta, cur_depth+1, max_depth)
        if min_v > alfa:
            alfa = min_v
            px = s.movimento[0]
            py = s.movimento[1]

        if beta < alfa: return (alfa, px, py)
    return (alfa, px, py)

def valor_min(estado, alfa, beta, cur_depth, max_depth):
    px = None
    py = None
    
    if teste_de_corte(cur_depth, max_depth):
        return (avalia(estado), estado.movimento[0], estado.movimento[1])
    for s in sucessores(estado, color_min):
        (max_v, max_x, max_y) = valor_max(s, alfa, beta, cur_depth+1, max_depth)
        
        if max_v < beta:
            beta = max_v
            px = s.movimento[0]
            py = s.movimento[1]
        
        if alfa > beta:
            return (beta, px, py)
    return (beta, px, py)

def avalia(estado):
    if not str(estado.tabuleiro) in transposition_table:
        valor = heuristics(estado, color_max, is_static)
        transposition_table[str(estado.tabuleiro)] = valor

    return transposition_table[str(estado.tabuleiro)]

def iterative_deepening(estado):
    print(str(decisao_minimax_alfa_beta(estado, 6)))



if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: launch.sh arquivo_estado_tabuleiro cor")
    else:
        arquivo_tabuleiro = sys.argv[1]
        estado = ler_tabuleiro(arquivo_tabuleiro)
        cor = sys.argv[2]
        if cor != white and cor != black: 
            print("COLOR ERROR. Assuming black")
            cor = black
        
        if cor == black:
            color_max = blackChar
            color_min = whiteChar
        else:
            color_max = whiteChar
            color_min = blackChar


        is_static = True

        iterative_deepening(estado)