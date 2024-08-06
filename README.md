# Chess
#### Description:

Final Project for Harvard's CS50P Course

A python project that codes chess from scratch. Specifically, I replicated the style of https://www.chess.com. The project gives the user the ability to play against an AI (stockfish) at a skill level they choose or a local game. They are also given the chose of their own time controls.

<img width="400" alt="Screenshot 2023-07-15 at 12 24 38 AM" src="https://github.com/varunm18/Chess/assets/94499114/5a334916-0979-44e6-8cdf-6eb80fa66ada">


#### This Project Uses pygame, pygame_widgets, and stockfish

* main.py: program runner
    * main(): Creates A new pygame and, using pygame_widgets, it displays 2 buttons(local play or AI play) as well as 2 sliders(AI Skill and time control). Based on which button is clicked, the respective function for the specific type of game is called.
    * playLocal(): A new pygame is called. The entire board and all items are drawn and the game loop is started. pygame listens for a mouse click and, when heard, it gets the location and if there is a piece on the board(and if it corresponds to color whose turn it is) it will select it and find its valid moves. However, if there is currently a promotion required, pygame won't look at any other clicks other than those that promote the piece. Every frame, the time is refreshed for the player currently going. Once a player moves, the positions on the board that are attacked by each piece are found and both kings are analyzed for checks. Finally, the neccessary updates happen and the screen updates these by calling multiple draw functions.
    * playAI(): Same as playLocal(), however, stockfish is also initialized at the skill level designated by user.
    * drawBoard(): Takes in a pygame screen and draws the neccessary squares in alternating colors.
    * drawSelected(): If something is selected by the user, then this function draws a yellow hue on the square to represent that it is selected. It will also draw the circles representing the valid moves the user can make with the piece.
    * drawIndex(): Draws time, rank numbers, file letters, and what pieces each user captured as well as the score difference
    * drawPieces(): Adds each piece to a pygame.sprite.Group() which will then be drawed in main game loop when group.update(eventList) is called. It also checks if ponf is in position of promoting.
    * drawPromotion(): Draws a list of pieces that the user can choose from when promoting.
    * findAttackers(): Finds all positions on board that are attacked by a piece.
    * stockFishTurn(): Called in AI Game which gives stockfish the current move list and recieves a next best move. This move is then reflected in the game.
      
* helpers.py: holds functions for move detection and click detection
    * locToPos(): Given an x, y click location, returns a file and rank on the board
    * posToLoc(): Given a file and rank, returns the x, y location on board
    * updatePonds(): Resets up2 boolean for any ponds excluding the one that was most recently moved
    * pond(): Finds up 1, up 2, and capturing on diagonals(including en passant) for ponds
    * rook(): Finds straight vertical and horizontal moves and current file and rank for rooks
    * knight(): Finds all L shaped moves for horses
    * bishop(): Finds all diagonal moves for bishops
    * king(): Finds moves to squares bordering king, and castling
    * queen(): Finds moves from bishop() and rook() functions
    * checkChecks(): Given a piece, and list of squares being attacked, returns if piece is in check
    * pieceValue(): returns value of any given piece type
    * validate(): Given the current board, current piece, un-validated move list, returns valid move list by checking if the move leaves the piece's king in check

* piece.py: holds different objects for pieces and global variables
    * Piece: Subclass of pygame.sprite.Sprite, holds values such as color, type, loc, image, valid move list, the DragOperator and other Bools. Sets its image by pygame specifications, draws itself and has update function which is called by main() every frame
    * TakenPiece
    * taken, attackers, moveList, pieces: dictionary of lists of what pieces are taken by each color, dicitonary of lists of what squares are attacked by color, list of all moves, dicitonary of Piece objects or None representing the state of each square, respectivly

* dragOperator.py, roundedRect.py: allows pieces to be dragged, and allows pygame to draw rounded rectangles
    * from https://stackoverflow.com/questions/66467383/how-to-draw-a-chessboard-with-pygame-and-move-the-pieces-on-the-board and https://www.pygame.org/project-AAfilledRoundedRect-2349-.html respectivly
      
* /images: holds all images of the pieces with file names condensed to two characters
