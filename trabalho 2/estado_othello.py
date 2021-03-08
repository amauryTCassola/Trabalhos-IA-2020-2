class Estado_othello:
    def __init__(self, pai, tabuleiro, movimento, valor):
        self.pai = pai
        self.tabuleiro = tabuleiro
        self.movimento = movimento
        self.valor = valor

    def __lt__(self, other):
        return self.custo < other.custo