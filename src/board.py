from const import *
from square import Square
from piece import *
from moves import Move

class Board:
    def __init__(self):
        self.cmdBoard = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.lastMove = None
        self._create()
        self._place_pieces('white')
        self._place_pieces('black')
    
    def moveonBoard(self, piece, move):
            initialPos = move.initialPlace
            finalPos = move.finalPlace
            self.cmdBoard[initialPos.row][initialPos.col].piece = None
            self.cmdBoard[finalPos.row][finalPos.col].piece = piece
            piece.moved = True
            piece.clearMoves()
            self.lastMove = move

    def valid_move(self, piece, argMove):
        print("called valid move", piece.name, argMove)
        return argMove in piece.validMoves
    
    def calcMoves(self, piece, row, col):
        def pawnMoves():
            steps = 1 if piece.moved else 2
            
            # straight moves
            start = row + piece.dir  # for white pieces row = 6
            end = row + (piece.dir * (1 + steps)) # 6 + (-1 *(1 + 2))
            for possibleRowMove in range(start, end, piece.dir):
                if Square.in_range(possibleRowMove):
                    if self.cmdBoard[possibleRowMove][col].isEmpty():
                        initialPos = Square(row, col)
                        finalPos = Square(possibleRowMove, col)
                        move = Move(initialPos, finalPos)
                        piece.add_move(move)
                    else: break
                else: break
            
            # diagonal pawn move
            possibleRowMove = row + piece.dir
            possibleColMoves = [col - 1, col + 1]
            for possibleColMove in possibleColMoves:
                if Square.in_range(possibleRowMove, possibleColMove):
                    if self.cmdBoard[possibleRowMove][possibleColMove].hasRivalPiece(piece.colour):
                        initialPos = Square(row, col)
                        finalPos = Square(possibleRowMove, possibleColMove)
                        move = Move(initialPos, finalPos)
                        piece.add_move(move) 


        def knightMoves():
            possibleMoves = [
                (row + 2, col + 1), 
                (row + 2, col - 1), 
                (row - 2, col + 1), 
                (row - 2, col - 1), 
                (row + 1, col + 2), 
                (row + 1, col - 2),
                (row - 1, col + 2), 
                (row - 1, col - 2) 
            ]

            for possibleMove in possibleMoves:
                possiblemoveInRow, possiblemoveInCol = possibleMove

                if Square.in_range(possiblemoveInRow, possiblemoveInCol):
                    if self.cmdBoard[possiblemoveInRow][possiblemoveInCol].isEmptyorRival(piece.colour):  # checks if we have a empty/rival piece square
                        initialPos = Square(row, col)
                        finalPos = Square(possiblemoveInRow, possiblemoveInCol)
                        move = Move(initialPos, finalPos)
                        piece.add_move(move)

        
        def straightLineMoves(increments):
            for increment in increments:  # increments = list
                rowIncr, colIncr = increment
                possibleRowMove = row + rowIncr
                possibleColMove = col + colIncr

                while True:
                    if Square.in_range(possibleRowMove, possibleColMove):
                        initialPos = Square(row, col)
                        finalPos = Square(possibleRowMove, possibleColMove)
                        move = Move(initialPos, finalPos)
                        
                        if self.cmdBoard[possibleRowMove][possibleColMove].isEmpty():
                            piece.add_move(move)

                        if self.cmdBoard[possibleRowMove][possibleColMove].hasRivalPiece(piece.colour):
                            piece.add_move(move)
                            break
                        if self.cmdBoard[possibleRowMove][possibleColMove].hasFriendPiece(piece.colour):
                            break
                    else:
                        break
                        
                    possibleRowMove, possibleColMove = possibleRowMove + rowIncr, possibleColMove + colIncr
        
        
        def kingMoves():
            possibleMoves = [
                (row - 1, col + 0), # up 
                (row + 1, col + 0), # down
                (row + 1, col + 1), # down right
                (row + 1, col - 1), # down left
                (row + 0, col + 1), # right
                (row + 0, col - 1), # left
                (row + 1, col - 1), # down left
                (row - 1, col - 1)  # up left
            ]
            
            for possibleMove in possibleMoves:
                possibleRowMove, possibleColMove = possibleMove
                if Square.in_range(possibleRowMove, possibleColMove):
                    if self.cmdBoard[possibleRowMove][possibleColMove].isEmptyorRival(piece.colour):
                        initialPos = Square(row, col)
                        finalPos = Square(possibleRowMove, possibleColMove)
                        move = Move(initialPos, finalPos)
                        piece.add_move(move)

        
        if isinstance(piece, Pawn): 
            pawnMoves()
        elif isinstance(piece, Knight): 
            knightMoves()
        
        elif isinstance(piece, Rook):
            straightLineMoves([
                (-1, 0), 
                (1, 0), 
                (0, 1), 
                (0, -1)
            ])
        
        elif isinstance(piece, Bishop):
            straightLineMoves([
                (-1, 1),
                (-1, -1), 
                (1, -1), 
                (1, 1)
            ])
        
        elif isinstance(piece, Queen):
            straightLineMoves([
                (-1, 0), 
                (1, 0), 
                (0, 1), 
                (0, -1), 
                (-1, 1),
                (-1, -1), 
                (1, -1), 
                (1, 1)
            ])
        
        elif isinstance(piece, King):
            kingMoves()


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

