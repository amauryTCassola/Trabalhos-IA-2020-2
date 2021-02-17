import sys
import heapq

class Node:
    """Classe representando um nodo no grafo de busca"""
    def __init__(self, pai, estado, acao, custo):
        self.pai = pai
        self.estado = estado
        self.acao = acao
        self.custo = custo

    def __lt__(self, other):
        return self.custo < other.custo

vazio = "_"
estado_objetivo = "12345678_"

def acao_cima(estado):
    '''executa a ação de mover o espaço vazio para cima

    Argumentos:
    estado -- o estado atual do 8-puzzle, formatado como '12345678_'

    Retorna: string representando o estado após executar a ação

    '''

    pos_vazio = estado.find("_")
    if pos_vazio <= 2: 
        return estado
    else:
        pos_acima_vazio = pos_vazio - 3
        num_acima_vazio = estado[pos_acima_vazio]
        estado = estado[:pos_acima_vazio] + vazio + estado[pos_acima_vazio+1:pos_vazio] + num_acima_vazio + estado[pos_vazio+1:]
        return estado

def acao_baixo(estado):
    '''executa a ação de mover o espaço vazio para baixo

    Argumentos:
    estado -- o estado atual do 8-puzzle, formatado como '12345678_'

    Retorna: string representando o estado após executar a ação

    '''

    pos_vazio = estado.find("_")
    if pos_vazio >= 6: 
        return estado
    else:
        pos_abaixo_vazio = pos_vazio + 3
        num_abaixo_vazio = estado[pos_abaixo_vazio]
        estado = estado[:pos_vazio] + num_abaixo_vazio + estado[pos_vazio+1:pos_abaixo_vazio] + vazio + estado[pos_abaixo_vazio+1:]
        return estado

def acao_direita(estado):
    '''executa a ação de mover o espaço vazio para direita

    Argumentos:
    estado -- o estado atual do 8-puzzle, formatado como '12345678_'

    Retorna: string representando o estado após executar a ação

    '''
    pos_vazio = estado.find("_")
    if pos_vazio == 2 or pos_vazio == 5 or pos_vazio == 8: 
        return estado
    else:
        pos_direita_vazio = pos_vazio + 1
        num_direita_vazio = estado[pos_direita_vazio]
        estado = estado[:pos_vazio] + num_direita_vazio + vazio + estado[pos_direita_vazio+1:]
        return estado

def acao_esquerda(estado):
    '''executa a ação de mover o espaço vazio para esquerda

    Argumentos:
    estado -- o estado atual do 8-puzzle, formatado como '12345678_'

    Retorna: string representando o estado após executar a ação

    '''
    pos_vazio = estado.find("_")
    if pos_vazio == 0 or pos_vazio == 3 or pos_vazio == 6: 
        return estado
    else:
        pos_esquerda_vazio = pos_vazio - 1
        num_esquerda_vazio = estado[pos_esquerda_vazio]
        estado = estado[:pos_esquerda_vazio] + vazio + num_esquerda_vazio + estado[pos_vazio+1:]
        return estado

def sucessor(estado):
    '''decide o próximo estado do 8-puzzle para cada ação possível

    Argumentos:
    estado -- o estado atual do 8-puzzle, formatado como '12345678_'

    Retorna: lista de pares (ação, estado)

    '''
    lista_sucessores = []

    lista_sucessores.append(('acima', acao_cima(estado)))
    lista_sucessores.append(('abaixo', acao_baixo(estado)))
    lista_sucessores.append(('direita', acao_direita(estado)))
    lista_sucessores.append(('esquerda', acao_esquerda(estado)))

    for sucessor_item in lista_sucessores:
        if sucessor_item[1] == estado:
            lista_sucessores.remove(sucessor_item)

    return lista_sucessores

def expande(nodo):
    '''
    expande um nodo, retornando seus vizinhos

    Argumentos:
    nodo -- o nodo a ser expandido, respeitando a classe Node

    Retorna: lista de nodos vizinhos
    '''

    lista_nodos_sucessores = []
    lista_estados_sucessores = sucessor(nodo.estado)
    for item in lista_estados_sucessores:
        novoNodo = Node(nodo, item[1], item[0], nodo.custo+1)
        lista_nodos_sucessores.append(novoNodo)

    return lista_nodos_sucessores

def node_in_list(node, list):
    for item in list:
        if item.estado == node.estado:
            return True
    return False

def push_node_into_heap(node, cost, heap):
    heapq.heappush(heap, (cost, node))

def pop_node_from_heap(heap):
    heap_item = heapq.heappop(heap)
    return heap_item[1]

def calcula_distancia_manhattan(pos1, pos2):
    x_pos1 = pos1 % 3 
    '''resto da divisão inteira por 3'''
    y_pos1 = pos1 // 3
    '''floor da divisão inteira por 3'''

    x_pos2 = pos2 % 3
    y_pos2 = pos2 // 3

    return abs(x_pos1 - x_pos2) + abs(y_pos1 - y_pos2)

def compute_heuristic_h2(node):
    estado_atual = node.estado
    custo_h2 = 0
    for index in range(0, len(estado_atual)):
        caractere_atual = estado_atual[index]
        if caractere_atual != "_":
            index_objetivo = estado_objetivo.index(caractere_atual)
            custo_h2 += calcula_distancia_manhattan(index, index_objetivo)
    return custo_h2

def compute_heuristic(node):
    return compute_heuristic_h2(node)

def a_star_search(s):
    ''''
    busca A*
    Argumentos:
    nodo
    Retorna: caminho
    '''
    caminho = ""
    x = []
    f = []
    push_node_into_heap(s, compute_heuristic(s), f)
    while f:
        v = pop_node_from_heap(f)
        
        if v.estado == estado_objetivo:
            while v.acao != None:
                caminho = v.acao + " " + caminho
                v = v.pai
            return(caminho)
                
        if not node_in_list(v,x):
            x.append(v)
            for item in expande(v):
                push_node_into_heap(item, compute_heuristic(item)+item.custo, f)

    return "FALHA"

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("usage: avalia_astar_h1.sh estado")

    else:
        estado = sys.argv[1]
        custo = 0
        nodo = Node(None, estado, None, custo)
        
        print("h2: "+str(compute_heuristic(nodo)))
        print("")
        resultado = a_star_search(nodo)
        print(resultado)