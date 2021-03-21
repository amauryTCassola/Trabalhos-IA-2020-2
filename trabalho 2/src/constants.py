black = "black"
white = "white"
blackChar = "B"
whiteChar = "W"
empty = "."
pos_infinity = float('inf')
neg_infinity = float('-inf')

def print_board(board):
    for i in range(8):
        print(str(board[i])+"""
        """)