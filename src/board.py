from const import *
from square import Square
from piece import *

class Board:
    def __init__(self):
        self.cmdBoard = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._place_pieces('white')
        self._place_pieces('black')
        
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.cmdBoard[row][col] = Square(row, col)


    def _place_pieces(self, colour):
        row_pawn, row_pieces = (6, 7) if colour == 'white' else (1, 0)
        
        # pawns
        for col in range(COLS):
            self.cmdBoard[row_pawn][col] = Square(row_pawn, col, Pawn(colour))

        #knights
        self.cmdBoard[row_pieces][1] = Square(row_pieces, 1, Knight(colour))
        self.cmdBoard[row_pieces][6] = Square(row_pieces, 6, Knight(colour))

        #bishops
        self.cmdBoard[row_pieces][2] = Square(row_pieces, 2, Bishop(colour))
        self.cmdBoard[row_pieces][5] = Square(row_pieces, 5, Bishop(colour))

        #rooks
        self.cmdBoard[row_pieces][0] = Square(row_pieces, 0, Rook(colour))
        self.cmdBoard[row_pieces][7] = Square(row_pieces, 7, Rook(colour))
        
        #couple
        self.cmdBoard[row_pieces][4] = Square(row_pieces, 3, Queen(colour))
        self.cmdBoard[row_pieces][3] = Square(row_pieces, 4, King(colour))
        
            
