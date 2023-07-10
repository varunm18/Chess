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

def pond(piece, board, attack):
    list = []
    offset = 1
    col = piece.color
    if col == "b":
        offset = -1
    
    # move 1 up
    up1 = f"{piece.loc[0]}{int(piece.loc[1])+offset}"
    if not attack:
        if up1 in board and board[up1]==None:
            list.append(up1)

    # move 2 up
    if not attack:
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
        elif(attack):
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
        elif(attack):
            list.append(rightd)
         # enpassant right
        else:
            checkright = f"{chr(int(ord(piece.loc[0]))-offset)}{int(piece.loc[1])}"
            if board[checkright] and board[checkright].color!=col and board[checkright].up2:
                list.append(rightd+"ep"+checkright)

    return list

def rook(piece, board, attack):
    list = []
    for i in range(4):
        for j in range(8):
            if i==0:
                move = f"{chr(int(ord(piece.loc[0]))+(j+1))}{int(piece.loc[1])}"
            elif i==1:
                move = f"{chr(int(ord(piece.loc[0]))-(j+1))}{int(piece.loc[1])}"
            elif i==2:
                move = f"{chr(int(ord(piece.loc[0])))}{int(piece.loc[1])+(j+1)}"
            elif i==3:
                move = f"{chr(int(ord(piece.loc[0])))}{int(piece.loc[1])-(j+1)}"

            if move not in board:
                break

            if board[move]==None:
                list.append(move)
            elif board[move].color!=piece.color:
                list.append(move)
                break
            elif attack:
                list.append(move)
                break
            else:
                break

    return list

def knight(piece, board, attack):
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
                if board[square]==None:
                    list.append(square)
                if board[square]:
                    if board[square].color!=col:
                        list.append(square)
                    elif(attack):
                        list.append(square)

    return list


def bishop(piece, board, attack):
    list = []
    for i in range(4):
        for j in range(8):
            if i==0:
                move = f"{chr(int(ord(piece.loc[0]))+(j+1))}{int(piece.loc[1])+(j+1)}"
            elif i==1:
                move = f"{chr(int(ord(piece.loc[0]))-(j+1))}{int(piece.loc[1])+(j+1)}"
            elif i==2:
                move = f"{chr(int(ord(piece.loc[0]))+(j+1))}{int(piece.loc[1])-(j+1)}"
            elif i==3:
                move = f"{chr(int(ord(piece.loc[0]))-(j+1))}{int(piece.loc[1])-(j+1)}"

            if move not in board:
                break

            if board[move]==None:
                list.append(move)
            elif board[move].color!=piece.color:
                list.append(move)
                break
            elif attack:
                list.append(move)
                break
            else:
                break

    return list

def king(piece, board, attackers, attack):
    list = []
    # regular movement
    shift = [-1, 0, 1]
    for i in shift:
        for j in shift:
            if i==0 and j==0:
                continue
            move = f"{chr(int(ord(piece.loc[0]))+i)}{int(piece.loc[1])+j}"
            if move in board:
                if board[move]==None:
                    list.append(move)
                elif board[move].color!=piece.color:
                    list.append(move)
                elif attack:
                    list.append(move)
    left = False
    right = False
    col = piece.color
    # castling
    # check that, rook is at location, didn't move, same color, king isn't in check, king didn't move, squares king travels between and including start and end isn't under attack or occupied
    print(piece.check)
    if not attack and not piece.moved and not piece.check:
        rank = 8
        if col == "w":
            rank = 1
        rookLocs = [f"a{rank}", f"h{rank}"]
        for loc in rookLocs:
            if board[loc] and board[loc].type == "r" and board[loc].color == col and not board[loc].moved:
                if loc == rookLocs[0]:
                    left = True
                else:
                    right = True
    if left:
        checkList = [f"d{rank}", f"c{rank}", f"b{rank}piece"]
        for item in checkList:
            set = "w"
            if col=="w":
                set = "b"
            for attack in attackers[set]:
                if "piece" in item:
                    if board[item[:2]]:
                        left = False
                elif attack == item or board[item]:
                    left = False
    if right:
        checkList = [f"f{rank}", f"g{rank}"]
        for item in checkList:
            set = "w"
            if col=="w":
                set = "b"
            for attack in attackers[set]:
                if attack == item or board[item]:
                    right = False
    
    if left:
        list.append(f"c{rank}00a{rank}d{rank}")
    if right:
        list.append(f"g{rank}00h{rank}f{rank}")

    return list

def checkChecks(piece, attackers):
    col = piece.color
    set = "w"
    if col=="w":
        set = "b"
    location = piece.loc
    for attack in attackers[set]:
        if attack == location:
            print(col)
            print("in check")
            print()
            return True
    print(col)
    print("out of check")
    print()
    return False

def queen(piece, board, attack):
    list = rook(piece, board, attack)
    bishopeMoves = bishop(piece, board, attack)

    for move in bishopeMoves:
        if move not in list:
            list.append(move)
    
    return list