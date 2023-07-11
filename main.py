# Example file showing a circle moving on screen
import pygame
from piece import Piece, pieces, attackers, taken
import moveCount
import helpers
from roundedRect import AAfilledRoundedRect

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

    wking = pieces["e1"]
    bking = pieces["e8"]

    lastCount = moveCount.count
    wMove = True

    findAttackers()

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
                        elif(wMove and pieces[selected].color=="w"):
                            pieces[selected].findValidMoves()
                            for key in pieces:
                                if pieces[key] and pieces[key].color==pieces[selected].color and key!=selected:
                                    pieces[key].validMoves = []
                        elif(not wMove and pieces[selected].color=="b"):
                            pieces[selected].findValidMoves()
                            for key in pieces:
                                if pieces[key] and pieces[key].color==pieces[selected].color and key!=selected:
                                    pieces[key].validMoves = []
                    elif(selected in promoteLocs):
                        promotePiece = promoteLocs[selected]
                        pieces[promote] = Piece(promotePiece[0], promotePiece[1], promote)
                        promote = None
                        requirePromotion = False
                        promoteLocs = {}
                        group, promote = drawPieces(screen, True)
                        findAttackers()
                        wking.checkForChecks()
                        bking.checkForChecks()
                    
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
        
        if moveCount.count!=lastCount:
            print("Turn Number: ", moveCount.count)
            lastCount = moveCount.count
            wMove = not wMove
            findAttackers()
            wking.checkForChecks()
            bking.checkForChecks()
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
        if i%2==0:
            color = (238,238,210)
        else:
            color = (117,150,86)
        text = font.render(chr(97+i), True, color)
        textRect = text.get_rect()
        textRect.topleft = (54+83*(i+1), 710)
        screen.blit(text, textRect)
        if i%2==1:
            color = (238,238,210)
        else:
            color = (117,150,86)
        text = font.render(str(8-i), True, color)
        textRect = text.get_rect()
        textRect.topleft = (74, 83*(i+1)-8)
        screen.blit(text, textRect)

    count1 = 0
    count2 = 0

    for key in taken:
        for item in taken[key]:
            if key=="w":
                count1+=helpers.pieceValue(item.type)
            else:
                count2+=helpers.pieceValue(item.type)

    if (len(taken["b"])==0 and len(taken["w"])==0) or count1==count2:
        start = False
    else:
        start = True
    
    bCount = False
    if count2 > count1:
        bCount = True
    
    print(f"{count1}, {count2}")

    for i in range(2):
        color = "Black"
        text = font.render(color, True, (0,0,0))
        if i==1:
            color = "White"
            text = font.render(color, True, (255,255,255))

        list = taken[color[:1].lower()]
        count = len(list)
        if color=="Black":
            if not start:
                bCount = 0
            AAfilledRoundedRect(screen, (62, 10, max(70, (count+bCount)*32)+4, 52), (238,238,210), 0.5) 
        elif color=="White":
            if not start:
                bCount = 1
            AAfilledRoundedRect(screen, (62, 742, max(70, (count+(not bCount))*32)+4, 52), (117,150,86), 0.5)

        textRect = text.get_rect()
        textRect.topleft = (68, 14+i*732)
        screen.blit(text, textRect)

        for j in range(len(list)):
            x, y = 68+j*30, 32+i*732
            rect = list[j].image.get_rect()
            rect.topleft = (x, y)
            screen.blit(list[j].image, rect) 

        if start:

            if bCount and color=="Black":
                text = font.render(f"+{count2-count1}", True, (0,0,0))
                textRect = text.get_rect()
                textRect.topleft = (len(taken["b"])*30+68, 38)
                screen.blit(text, textRect)

            elif not bCount and color=="White":
                text = font.render(f"+{count1-count2}", True, (255,255,255))
                textRect = text.get_rect()
                textRect.topleft = (len(taken["w"])*30+68, 770)
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

def findAttackers():
    whiteAttack = []
    blackAttack = []
    for key in pieces:
        if pieces[key]:
            match pieces[key].type:
                case "p":
                    moves = helpers.pond(pieces[key], pieces, True)
                case "r":
                    moves = helpers.rook(pieces[key], pieces, True)
                case "n":
                    moves = helpers.knight(pieces[key], pieces, True)
                case "b":
                    moves = helpers.bishop(pieces[key], pieces, True)
                case "k":
                    moves = helpers.king(pieces[key], pieces, attackers, True)
                case "q":
                    moves = helpers.queen(pieces[key], pieces, True)

            for move in moves:
                if pieces[key].color == "w":
                    if move not in whiteAttack:
                        whiteAttack.append(move)
                if pieces[key].color == "b":
                    if move not in blackAttack:
                        blackAttack.append(move)
    attackers["w"] = whiteAttack
    attackers["b"] = blackAttack

# def temp(screen, whiteAttack, blackAttack):
#     for move in whiteAttack:
#         pygame.draw.circle(screen, (255, 255, 255), helpers.locToPos(move), 15)
#     for move in blackAttack:
#         pygame.draw.circle(screen, (10, 21, 100), helpers.locToPos(move), 15)

if __name__=="__main__":
    main()