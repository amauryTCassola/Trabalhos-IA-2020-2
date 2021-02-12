import sys

vazio = "_"

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

    123
    456
    78_

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

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("usage: avalia_sucessor.sh estado")

    else:
        for item in sucessor(sys.argv[1]):
            print("("+item[0]+",\""+item[1]+"\")", end =" ")