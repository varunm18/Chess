# Example file showing a circle moving on screen
import pygame
from piece import Piece
from piece import pieces
import helpers

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Chess")
    clock = pygame.time.Clock()
    running = True
    dt = 0
    selected = None
    board = pygame.Surface((664, 664))

    board = drawBoard(board)
    drawIndex(screen)

    group = drawPieces(screen, True)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = helpers.posToLoc(pygame.mouse.get_pos())
                if(selected!=None and pieces[selected]==None):
                    selected = None  
                else:
                    pieces[selected].findValidMoves()
            if event.type == pygame.QUIT:
                running = False

        screen.fill((48,46,43))
        screen.blit(board, (68, 68))
        if(selected):
            drawSelected(screen, selected)
        drawIndex(screen)
        group = drawPieces(screen, False) 
        group.update(eventList)
        group.draw(screen)
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

def drawBoard(board):

    board.fill((238,238,210))

    for y in range(8):
        if(y%2==1):
            for x in range(0, 8, 2):
                pygame.draw.rect(board, (117,150,86), (x*83, y*83, 83, 83))
        else:
            for x in range(0, 8, 2):
                pygame.draw.rect(board, (117,150,86), ((x+1)*83, y*83, 83, 83))

    return board

def drawSelected(screen, loc):
    piece = pieces[loc]
    x = int(ord(loc[0])) - 97
    y = int(loc[1]) - 1
    board = pygame.Surface((83, 83))
    pygame.draw.rect(board, (187,201,64), (0, 0, 83, 83))
    screen.blit(board, (68+x*83, 649-y*83))

def drawIndex(screen):

    font = pygame.font.Font('freesansbold.ttf', 20)

    for i in range(8):
        text = font.render(chr(97+i), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (54+83*(i+1), 710)
        screen.blit(text, textRect)
        text = font.render(str(8-i), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.topleft = (74, 83*(i+1)-8)
        screen.blit(text, textRect)

def drawPieces(screen, init):
    group = pygame.sprite.Group()
    selected = None
    for key in pieces:
        if pieces[key] != None:
            if pieces[key].drag.dragging:
                selected = key
            else:
               group.add(pieces[key])  

            if init:
                pieces[key].draw(screen)

    if(selected):
        group.add(pieces[selected])

    return group
  
if __name__=="__main__":
    main()