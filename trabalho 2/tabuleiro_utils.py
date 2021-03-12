from estado_othello import Estado_othello

def string_to_matrix(string):
    line_list = string.splitlines()
    res = [list(sub) for sub in line_list][:8]
    return res

def ler_tabuleiro(filename):
    """
    Dado o nome do arquivo do tabuleiro, retorna o estado inicial
    do tabuleiro com a estrutura definida em estado-othello.py
    """
    f = open(filename, "r")
    estado = Estado_othello(None, string_to_matrix(f.read()), None, 0)
    return estado