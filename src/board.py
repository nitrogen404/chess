from const import *
from square import Square
from piece import *
from moves import Move
import copy

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
            enPassantEmpty = self.cmdBoard[finalPos.row][finalPos.col].isEmpty()
            
            self.cmdBoard[initialPos.row][initialPos.col].piece = None
            self.cmdBoard[finalPos.row][finalPos.col].piece = piece
            
            if isinstance(piece, Pawn):
                diff = finalPos.col - initialPos.col
                if diff != 0 and enPassantEmpty:
                    self.cmdBoard[initialPos.row][initialPos.col + diff].piece = None
                    self.cmdBoard[finalPos.row][finalPos.col].piece = piece

                else: self.isPromotion(piece, finalPos)

            if isinstance(piece, King):
                if self.castling(initialPos, finalPos):
                    diff = finalPos.col - initialPos.col
                    rook = piece.leftRook if (diff < 0) else piece.rightRook
                    self.moveonBoard(rook, rook.validMoves[-1])

            piece.moved = True
            piece.clearMoves()
            self.lastMove = move

    def valid_move(self, piece, argMove):
        print("called valid move", piece.name, argMove)
        return argMove in piece.validMoves
    
    def isPromotion(self, piece, finalPos):
        if finalPos.row == 0 or finalPos.row == 7:
            self.cmdBoard[finalPos.row][finalPos.col].piece = Queen(piece.colour)
        
    def castling(self, initialPos, finalPos):
        return abs(initialPos.col - finalPos.col) == 2
    
    def set_true_enPassant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.cmdBoard[row][col].piece, Pawn):
                    self.cmdBoard[row][col].piece.en_passant = False
        piece.en_passant = True

    def inCheck(self, piece, move):
        tempPiece = copy.deepcopy(piece)
        tempBoard = copy.deepcopy(self)
        tempBoard.moveonBoard(tempPiece, move)
        
        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.cmdBoard[row][col].hasRivalPiece(piece.colour):
                    p = tempBoard.cmdBoard[row][col].piece
                    tempBoard.calcMoves(p, row, col, bool=False)
                    for m in p.validMoves:
                        if isinstance(m.finalPlace.piece, King):
                            print("returned true")
                            return True
        print("returned false")
        return False


    def calcMoves(self, piece, row, col, bool=True):
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
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.add_move(move)
                        else:
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
                        finalPiece = self.cmdBoard[possibleRowMove][possibleColMove].piece
                        finalPos = Square(possibleRowMove, possibleColMove, finalPiece)
                        move = Move(initialPos, finalPos)
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.add_move(move) 
                        else:
                            piece.add_move(move) 
            
            # left enPassant
            r = 3 if piece.colour == "white" else 4
            finalR = 2 if piece.colour == "white" else 5
            if Square.in_range(col - 1) and row == r:
                if self.cmdBoard[row][col - 1].hasRivalPiece(piece.colour):
                    p = self.cmdBoard[row][col - 1].piece
                    if p.en_passant:
                        initialPos = Square(row, col)
                        finalPos = Square(finalR, col - 1, p)
                        move = Move(initialPos, finalPos)
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.add_move(move) 
                        else:
                            piece.add_move(move) 
            
            # right en_passant
            if Square.in_range(col + 1) and row == r:
                if self.cmdBoard[row][col + 1].hasRivalPiece(piece.colour):
                    p = self.cmdBoard[row][col + 1].piece
                    if p.en_passant:
                        initialPos = Square(row, col)
                        finalPos = Square(finalR, col + 1, p)
                        move = Move(initialPos, finalPos)
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.add_move(move) 
                        else:
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
                        finalPiece = self.cmdBoard[possiblemoveInRow][possiblemoveInCol].piece
                        finalPos = Square(possiblemoveInRow, possiblemoveInCol, finalPiece)
                        move = Move(initialPos, finalPos)
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        
        def straightLineMoves(increments):
            for increment in increments:  # increments = list
                rowIncr, colIncr = increment
                possibleRowMove = row + rowIncr
                possibleColMove = col + colIncr

                while True:
                    if Square.in_range(possibleRowMove, possibleColMove):
                        initialPos = Square(row, col)
                        finalPiece = self.cmdBoard[possibleRowMove][possibleColMove].piece
                        finalPos = Square(possibleRowMove, possibleColMove, finalPiece)
                        move = Move(initialPos, finalPos)
                        
                        if self.cmdBoard[possibleRowMove][possibleColMove].isEmpty():
                            if bool:
                                if not self.inCheck(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)


                        elif self.cmdBoard[possibleRowMove][possibleColMove].hasRivalPiece(piece.colour):
                            if bool:
                                if not self.inCheck(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)
                            break
                        elif self.cmdBoard[possibleRowMove][possibleColMove].hasFriendPiece(piece.colour):
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
            
            if not piece.moved:
                leftRook = self.cmdBoard[row][0].piece
                
                if isinstance(leftRook, Rook):
                    if not leftRook.moved:
                        for c in range(1, 3):
                            if self.cmdBoard[row][c].has_piece(): # cannot castle
                                break
                            if c == 2:
                                piece.leftRook = leftRook
                                # rook's move
                                initialSquare = Square(row, 0)
                                finalSquare = Square(row, 2)
                                moveRook = Move(initialSquare, finalSquare)
                                leftRook.add_move(moveRook)
                                
                                # king's move
                                initialSquare = Square(row, col)
                                finalSquare = Square(row, 1)
                                moveKing = Move(initialSquare, finalSquare)
                                piece.add_move(moveKing)
                
                
                rightRook = self.cmdBoard[row][7].piece
                if isinstance(rightRook, Rook): 
                    if not rightRook.moved:
                        for c in range(5, 7):
                            if self.cmdBoard[row][c].has_piece(): # cannot castle
                                break
                            if c == 6:
                                piece.rightRook = rightRook
                                # rook's move
                                initialSquare = Square(row, 7)
                                finalSquare = Square(row, 4) # as per chess.com
                                moveRook = Move(initialSquare, finalSquare)
                                rightRook.add_move(moveRook)
                                
                                # king's move
                                initialSquare = Square(row, col)
                                finalSquare = Square(row, 5) # as per chess.com
                                moveKing = Move(initialSquare, finalSquare)
                                piece.add_move(moveKing)
        
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

