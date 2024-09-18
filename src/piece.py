import os

class Piece:
    def __init__(self, name, colour, value, texture=None, texture_rect=None):
        self.name = name
        self.colour = colour
        self.texture = texture
        self.texture_rect = texture_rect
        self.set_texture()
        valueSign = 1 if colour == 'white' else -1
        self.value = value * valueSign
        self.validMoves = []
        self.moved = False


    def set_texture(self, size=80):
        self.texture = os.path.join(f'../assets/images/imgs-{size}px/{self.colour}_{self.name}.png')

    def add_moves(self, validMove):
        self.validMoves.append(validMove)


class Pawn(Piece):
    def __init__(self, colour):
        self.dir = -1 if colour == 'white' else 1
        super().__init__('pawn', colour, 1.0)

class Knight(Piece):
    def __init__(self, colour):
        super().__init__('knight', colour, 3.0)
    
class Bishop(Piece):
    def __init__(self, colour):
        super().__init__('bishop', colour, 3.001) # need to experiment with value

class Rook(Piece):
    def __init__(self, colour):
        super().__init__('rook', colour, 5.0)

class Queen(Piece):
    def __init__(self, colour):
        super().__init__('queen', colour, 9.0)

class King(Piece):
    def __init__(self, colour):
        super().__init__('king', colour, 100000.0)
