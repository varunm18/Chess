import pygame
import helpers
from dragOperator import DragOperator

class Piece(pygame.sprite.Sprite):
    def __init__(self, color, type, loc):
        super().__init__() 
        self.color = color
        self.loc = loc
        self.type = type
        self.image = pygame.image.load(f"images/{self.color}{self.type}.png")
        self.validMoves = []
        self.drag = DragOperator(self)

    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, img):
        image = pygame.transform.scale(img, (80, 80))
        self._image = image

    def draw(self, surface):
        self.surface = surface
        x, y = helpers.locToPos(self.loc) 
        rect = self.image.get_rect()
        rect.center = (x, y)
        self.rect = self.image.get_rect(center = (x,y))
        surface.blit(self.image, rect) 

    def update(self, event_list):
        self.drag.update(event_list)
        if not self.drag.dragging:
            if helpers.posToLoc((self.rect.centerx, self.rect.centery)) in self.validMoves:
                pieces[self.loc] = None
                self.loc = helpers.posToLoc((self.rect.centerx, self.rect.centery))
                pieces[self.loc] = self
                self.draw(self.surface) 
            else:
                self.draw(self.surface)
    
    def findValidMoves(self):
        match self.type:
            case "p":
                self.validMoves = helpers.pond(self)
            case "r":
                self.validMoves = helpers.rook(self)
            case "n":
                self.validMoves = helpers.knight(self)
            case "b":
                self.validMoves = helpers.bishop(self)
            case "k":
                self.validMoves = helpers.king(self)
            case "q":
                self.validMoves = helpers.queen(self)

    def __str__(self):
        return f"{self.color}{self.type} at {self.loc}"


pieces = {
    "a1" : Piece("w", "r", "a1"),
    "b1" : Piece("w", "n", "b1"),
    "c1" : Piece("w", "b", "c1"),
    "d1" : Piece("w", "q", "d1"),
    "e1" : Piece("w", "k", "e1"),
    "f1" : Piece("w", "b", "f1"),
    "g1" : Piece("w", "n", "g1"),
    "h1" : Piece("w", "r", "h1"),

    "a2" : Piece("w", "p", "a2"),
    "b2" : Piece("w", "p", "b2"),
    "c2" : Piece("w", "p", "c2"),
    "d2" : Piece("w", "p", "d2"),
    "e2" : Piece("w", "p", "e2"),
    "f2" : Piece("w", "p", "f2"),
    "g2" : Piece("w", "p", "g2"),
    "h2" : Piece("w", "p", "h2"),

    "a3" : None,
    "b3" : None,
    "c3" : None,
    "d3" : None,
    "e3" : None,
    "f3" : None,
    "g3" : None,
    "h3" : None, 

    "a4" : None,
    "b4" : None,
    "c4" : None,
    "d4" : None,
    "e4" : None,
    "f4" : None,
    "g4" : None,
    "h4" : None,

    "a5" : None,
    "b5" : None,
    "c5" : None,
    "d5" : None,
    "e5" : None,
    "f5" : None,
    "g5" : None,
    "h5" : None,

    "a6" : None,
    "b6" : None,
    "c6" : None,
    "d6" : None,
    "e6" : None,
    "f6" : None,
    "g6" : None,
    "h6" : None,

    "a7" : Piece("b", "p", "a7"),
    "b7" : Piece("b", "p", "b7"),
    "c7" : Piece("b", "p", "c7"),
    "d7" : Piece("b", "p", "d7"),
    "e7" : Piece("b", "p", "e7"),
    "f7" : Piece("b", "p", "f7"),
    "g7" : Piece("b", "p", "g7"),
    "h7" : Piece("b", "p", "h7"),

    "a8" : Piece("b", "r", "a8"),
    "b8" : Piece("b", "n", "b8"),
    "c8" : Piece("b", "b", "c8"),
    "d8" : Piece("b", "q", "d8"),
    "e8" : Piece("b", "k", "e8"),
    "f8" : Piece("b", "b", "f8"),
    "g8" : Piece("b", "n", "g8"),
    "h8" : Piece("b", "r", "h8")
}  
