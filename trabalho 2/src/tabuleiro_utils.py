from estado_othello import Estado_othello
import numpy

def string_to_matrix(string):

    line_list = string.splitlines()

    res = numpy.array([ list(word) for word in line_list ])

    return res

def ler_tabuleiro(filename):
    """
    Dado o nome do arquivo do tabuleiro, retorna o estado inicial
    do tabuleiro com a estrutura definida em estado-othello.py
    """
    f = open(filename, "r")
    estado = Estado_othello(string_to_matrix(f.read()), None)
    return estado