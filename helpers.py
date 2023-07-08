# relative to screen
def locToPos(loc):
    file = int(ord(loc[0])) - 96
    rank = int(loc[1])
    print(f"File: {file} Rank: {rank}")
    return file*83+26.5, 773.5-rank*83

def posToLoc(pos):
    x, y = pos
    rank = round(-y/83 + 9.319277108)
    file = round(x/83 - 0.3192771084)
    if file < 1 or file > 8 or rank < 1 or rank > 8:
        return None
    return chr(file+96)+str(rank)

def pond(piece):
    return []

def rook(piece):
    return []

def knight(piece):
    return []

def bishop(piece):
    return []

def king(piece):
    return []

def queen(piece):
    return []