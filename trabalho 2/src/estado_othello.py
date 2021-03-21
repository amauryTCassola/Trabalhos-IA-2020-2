class Estado_othello:
    def __init__(self, tabuleiro, movimento):
        self.tabuleiro = tabuleiro
        self.movimento = movimento

    def __lt__(self, other):
        return self.custo < other.custo