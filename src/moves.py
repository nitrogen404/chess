class Move:
    def __init__(self, initialPlace, finalPlace):
        self.initialPlace = initialPlace
        self.finalPlace = finalPlace
    
    def __str__(self):
        s = ''
        s += f'({self.initialPlace.col}, {self.initialPlace.row})'
        s += f' -> ({self.finalPlace.col}, {self.finalPlace.row})'
        return s

    def __eq__(self, other):
        return self.initialPlace == other.initialPlace and self.finalPlace == other.finalPlace
    