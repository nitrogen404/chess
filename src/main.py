import pygame
import sys
from const import *
from game import Game
from square import Square
from moves import Move


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
            game.showLastMove(screen)
            game.show_moves(screen)
            game.render_pieces(screen)
            
            if dragger.dragged:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clickedRow = dragger.mouseY // SQSIZE # returns integer indicates the row number where mouse is clicked
                    clickedCol = dragger.mouseX // SQSIZE 
                    
                    if board.cmdBoard[clickedRow][clickedCol].has_piece():
                        piece = board.cmdBoard[clickedRow][clickedCol].piece
                        if piece.colour == game.nextTurn:
                            board.calcMoves(piece, clickedRow, clickedCol, bool=True)
                            dragger.save_initial_position(event.pos)
                            dragger.drag_piece(piece)
                            
                            game.show_bg(screen)
                            game.showLastMove(screen)
                            game.show_moves(screen)
                            game.render_pieces(screen)
                        
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragged:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.showLastMove(screen)
                        game.show_moves(screen)
                        game.render_pieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragged:
                        dragger.update_mouse(event.pos)
                        releasedRow = dragger.mouseY // SQSIZE
                        releasedCol = dragger.mouseX // SQSIZE
                        initialPos = Square(dragger.initialRow, dragger.initialCol)
                        finalPos = Square(releasedRow, releasedCol)
                        move = Move(initialPos, finalPos)

                        if board.valid_move(dragger.piece, move):
                            print("valid move!")
                            board.moveonBoard(dragger.piece, move)
                            board.set_true_enPassant(dragger.piece)
                            game.show_bg(screen)
                            game.showLastMove(screen)
                            game.render_pieces(screen)
                            game.nextPlayerTurn()

                    dragger.undrag_piece()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()
