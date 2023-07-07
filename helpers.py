# relative to screen
def locToPos(loc):
    file = int(ord(loc[0])) - 96
    rank = int(loc[1])
    print(f"File: {file} Rank: {rank}")
    return file*83+26.5, 773.5-rank*83