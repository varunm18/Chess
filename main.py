# Example file showing a circle moving on screen
import pygame
from piece import Piece

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    running = True
    dt = 0

    board = pygame.Surface((664, 664))

    drawBoard(board, screen)

    pieces = drawPieces(screen)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

def drawBoard(board, screen):

    board.fill((227,193,111))

    for y in range(8):
        if(y%2==1):
            for x in range(0, 8, 2):
                pygame.draw.rect(board, (184,139,74), (x*83, y*83, 83, 83))
        else:
            for x in range(0, 8, 2):
                pygame.draw.rect(board, (184,139,74), ((x+1)*83, y*83, 83, 83))

    screen.blit(board, (68, 68))

    font = pygame.font.Font('freesansbold.ttf', 20)

    for i in range(8):
        text = font.render(chr(97+i), True, (255,255,255))
        textRect = text.get_rect()
        textRect.topleft = (54+83*(i+1), 710)
        screen.blit(text, textRect)
        text = font.render(str(8-i), True, (255,255,255))
        textRect = text.get_rect()
        textRect.topleft = (74, 83*(i+1)-8)
        screen.blit(text, textRect)

def drawPieces(screen):
    pieces = [Piece("w", "r", "a1"), Piece("w", "n", "b1"), Piece("w", "b", "c1"), Piece("w", "q", "d1"), Piece("w", "k", "e1"), Piece("w", "b", "f1"), Piece("w", "n", "g1"), Piece("w", "r", "h1"), Piece("b", "r", "a8"), Piece("b", "n", "b8"), Piece("b", "b", "c8"), Piece("b", "q", "d8"), Piece("b", "k", "e8"), Piece("b", "b", "f8"), Piece("b", "n", "g8"), Piece("b", "r", "h8")]
    for i in range(8):
        pieces.append(Piece("w", "p", chr(97+i)+"2"))
        pieces.append(Piece("b", "p", chr(97+i)+"7"))    

    for piece in pieces:
        piece.draw(screen)
  
if __name__=="__main__":
    main()