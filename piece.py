import pygame
import helpers

class Piece:
    def __init__(self, color, type, loc):
        self.color = color
        self.loc = loc
        self.type = type
        self.img = pygame.image.load(f"pieces/{self.color}{self.type}.png")

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
