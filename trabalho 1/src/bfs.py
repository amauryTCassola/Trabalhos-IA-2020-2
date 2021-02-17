import sys

class Node:
    """Classe representando um nodo no grafo de busca"""
    def __init__(self, pai, estado, acao, custo):
        self.pai = pai
        self.estado = estado
        self.acao = acao
        self.custo = custo

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

def breadth_first_search(s):
    ''''
    busca em largura (BFS)
    Argumentos:
    nodo
    Retorna: caminho
    '''
    caminho = ""
    x = []
    f = []
    f.append(s)
    while f:
        v = f.pop(0)
        
        if v.estado == estado_objetivo:
            while v.acao != None:
                caminho = v.acao + " " + caminho
                v = v.pai
            return(caminho)
                
        if not node_in_list(v,x):
            x.append(v)
            for item in expande(v):
                f.append(item)

    return "FALHA"

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("usage: avalia_bfs.sh estado")

    else:
        estado = sys.argv[1]
        custo = 0
        nodo = Node(None, estado, None, custo)
        
        resultado = breadth_first_search(nodo)
        print(resultado)