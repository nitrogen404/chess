import pygame
import sys
from const import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.render_pieces(screen)
            if dragger.dragged:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clickedRow = dragger.mouseY // SQSIZE # returns integer indicates the row number where mouse is clicked
                    clickedCol = dragger.mouseX // SQSIZE 
                    if board.cmdBoard[clickedRow][clickedCol].has_piece:
                        piece = board.cmdBoard[clickedRow][clickedCol].piece
                        dragger.save_initial_position(event.pos)
                        dragger.drag_piece(piece)
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragged:
                        dragger.update_mouse(event.pos)
                        # game.show_bg(screen)
                        # game.render_pieces(screen)
                        dragger.update_blit(screen)
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

    
main = Main()
main.mainloop()
