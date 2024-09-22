import pygame
from const import *
from board import Board
from dragger import Dragger

class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    colour = (234, 235, 200)
                else:
                    colour = (119, 154, 88)
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, colour, rect)

   
    def render_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.cmdBoard[row][col].has_piece():
                    piece = self.board.cmdBoard[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    
    def show_moves(self, surface): 
        if self.dragger.dragged:
            piece = self.dragger.piece
            
            for move in piece.validMoves:
                colour = "#C86464" if (move.finalPlace.row + move.finalPlace.col) % 2 == 0 else "#C84646"
                rect = (move.finalPlace.col * SQSIZE, move.finalPlace.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, colour, rect)
