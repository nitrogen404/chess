import pygame
from const import * 

class Dragger:
    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0
        self.piece = None
        self.dragged = False
    
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos  # tuple

    def save_initial_position(self, pos): # XY co-ordinates
        self.initialRow = pos[1] // SQSIZE
        self.initialCol = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragged = True
    
    def undrag_piece(self):
        self.piece = None
        self.dragged = False
    
    def update_blit(self, surface):
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)