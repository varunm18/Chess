# relative to screen
def locToPos(loc):
    file = int(ord(loc[0])) - 96
    rank = int(loc[1])
    return file*83+26.5, 773.5-rank*83

def posToLoc(pos):
    x, y = pos
    rank = round(-y/83 + 9.319277108)
    file = round(x/83 - 0.3192771084)
    if file < 1 or file > 8 or rank < 1 or rank > 8:
        return None
    return chr(file+96)+str(rank)

# reset up2 boolean for any pieces excluding the one that was most recently moved
def updatePonds(piece, board):
    for item in board:
        if board[item] and board[item]!=piece:
            if board[item].up2:
                board[item].up2 = False

def pond(piece, board):
    list = []
    offset = 1
    col = piece.color
    if col == "b":
        offset = -1
    
    # move 1 up
    up1 = f"{piece.loc[0]}{int(piece.loc[1])+offset}"
    if up1 in board and board[up1]==None:
        list.append(up1)

    # move 2 up
    if not piece.moved and up1 in list:
        up2 = f"{piece.loc[0]}{int(piece.loc[1])+2*offset}"
        if up2 in board and board[up2]==None:
            list.append(up2+"up2")

    leftd = f"{chr(int(ord(piece.loc[0]))+offset)}{int(piece.loc[1])+offset}"
    rightd = f"{chr(int(ord(piece.loc[0]))-offset)}{int(piece.loc[1])+offset}"

     # move diagonal, for enpassant or for capturing pieces
    if leftd in board:
        # capture left
        if board[leftd]:
            if board[leftd].color != col:
                list.append(leftd)
        # enpassant left
        else:
            checkleft = f"{chr(int(ord(piece.loc[0]))+offset)}{int(piece.loc[1])}"
            if board[checkleft] and board[checkleft].color!=col and board[checkleft].up2:
                list.append(leftd+"ep"+checkleft)
    
    if rightd in board:
        # capture right
        if board[rightd]:
            if board[rightd].color != col:
                list.append(rightd)
         # enpassant right
        else:
            checkright = f"{chr(int(ord(piece.loc[0]))-offset)}{int(piece.loc[1])}"
            if board[checkright] and board[checkright].color!=col and board[checkright].up2:
                list.append(rightd+"ep"+checkright)

    return list

def rook(piece, board):
    return []

def knight(piece, board):
    list = []
    col = piece.color

    leftup = f"{chr(int(ord(piece.loc[0]))+1)}{int(piece.loc[1])+1}ru"
    rightup = f"{chr(int(ord(piece.loc[0]))-1)}{int(piece.loc[1])+1}lu"
    leftdown = f"{chr(int(ord(piece.loc[0]))+1)}{int(piece.loc[1])-1}rd"
    rightdown = f"{chr(int(ord(piece.loc[0]))-1)}{int(piece.loc[1])-1}ld"
    possible = [leftup, rightup, leftdown, rightdown]

    for move in possible:
        for i in range(2):
            action = move[2+i:3+i]
            match action:
                case "l":
                    square = f"{chr(int(ord(move[0]))-1)}{int(move[1])}"
                case "u":
                    square = f"{chr(int(ord(move[0])))}{int(move[1])+1}"
                case "r":
                    square = f"{chr(int(ord(move[0]))+1)}{int(move[1])}"
                case "d":
                    square = f"{chr(int(ord(move[0])))}{int(move[1])-1}"
            if square in board:
                if board[square]:
                    if board[square].color!=col:
                        list.append(square)
                else:
                    list.append(square)

    return list


def bishop(piece, board):
    return []

def king(piece, board):
    return []

def queen(piece, board):
    return []