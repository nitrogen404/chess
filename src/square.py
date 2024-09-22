class Square:
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
    
    def has_piece(self):
        return self.piece != None
    
    def isEmpty(self):
        return not self.has_piece()
    
    def hasFriendPiece(self, colour):
        return self.has_piece() and self.piece.colour == colour
    
    def hasRivalPiece(self, colour):
        return self.has_piece() and self.piece.colour != colour

    def isEmptyorRival(self, colour):
        return self.isEmpty() or self.hasRivalPiece(colour)
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    