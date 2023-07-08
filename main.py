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
    board = pygame.Surface((664, 664))

    selected = None

    promote = None
    requirePromotion = False
    promoteLocs = {}

    board = drawBoard(board)
    drawIndex(screen)

    group, promote = drawPieces(screen, True)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = helpers.posToLoc(pygame.mouse.get_pos())
                if(selected!=None):
                    if(not requirePromotion):
                        if(pieces[selected]==None):
                            selected = None 
                            print("selected is none") 
                        else:
                            pieces[selected].findValidMoves()
                    elif(selected in promoteLocs):
                        promotePiece = promoteLocs[selected]
                        pieces[promote] = Piece(promotePiece[0], promotePiece[1], promote)
                        promote = None
                        requirePromotion = False
                        promoteLocs = {}
                        group, promote = drawPieces(screen, True)
                    
                
            if event.type == pygame.QUIT:
                running = False

        screen.fill((48,46,43))
        screen.blit(board, (68, 68))
        if(selected and pieces[selected]):
            drawSelected(screen, selected)
        else:
            selected = None
        drawIndex(screen)
        group, promote = drawPieces(screen, False) 
        group.update(eventList)
        group.draw(screen)

        if promote:
            requirePromotion = True
            promoteLocs = drawPromotion(screen, promote)
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

    for move in piece.validMoves:
        pygame.draw.circle(screen, (0,0,0), helpers.locToPos(move), 15)

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
    promote = None
    for key in pieces:
        if pieces[key] != None:
            if pieces[key].drag.dragging:
                selected = key
            else:
               group.add(pieces[key])  
            if init:
                pieces[key].draw(screen)
            if pieces[key].type=="p" and (pieces[key].loc[1]=="8" or pieces[key].loc[1]=="1"):
                promote = key

    if(selected):
        group.add(pieces[selected])

    return group, promote

def drawPromotion(screen, loc):
    board = pygame.Surface((83, 332))
    board.fill((255,255,255))
    x, y = helpers.locToPos(loc)

    col = "b"
    offset = -1
    y-=249
    if pieces[loc].color=="w":
        col = "w"
        offset = 1
        y+=249
    
    screen.blit(board, (x-41.5, y-41.5)) 

    promotion = [col+"q", col+"r", col+"n", col+"b"]

    promoteLocs = {}

    for i in range(len(promotion)):
        image = pygame.image.load(f"images/{promotion[i]}.png")
        image = pygame.transform.scale(image, (80, 80))
        location = f"{loc[0]}{int(loc[1])-(offset*i)}"
        promoteLocs[location] = f"{promotion[i]}"
        x, y = helpers.locToPos(location) 
        rect = image.get_rect()
        rect.center = (x, y)
        screen.blit(image, rect) 
    
    return promoteLocs
  
if __name__=="__main__":
    main()