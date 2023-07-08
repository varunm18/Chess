import pygame
import helpers

class Piece:
    def __init__(self, color, type, loc):
        self.color = color
        self.loc = loc
        self.type = type
        self.img = pygame.image.load(f"images/{self.color}{self.type}.png")
        self.validMove = []

    @property
    def img(self):
        return self._img
    
    @img.setter
    def img(self, img):
        img = pygame.transform.scale(img, (80, 80))
        self._img = img

    def draw(self, surface):
        x, y = helpers.locToPos(self.loc) 
        rect = self.img.get_rect()
        rect.center = (x, y)
        surface.blit(self.img, rect) 
    
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
