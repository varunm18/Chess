# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
running = True
dt = 0

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

board = pygame.Surface((664, 664))
board.fill((227,193,111))

font = pygame.font.Font('freesansbold.ttf', 20)
 

for y in range(8):
    if(y%2==1):
        for x in range(0, 8, 2):
            pygame.draw.rect(board, (184,139,74), (x*83, y*83, 83, 83))
    else:
        for x in range(0, 8, 2):
            pygame.draw.rect(board, (184,139,74), ((x+1)*83, y*83, 83, 83))

screen.blit(board, (68, 68))

for i in range(8):
    text = font.render(files[i], True, (255,255,255))
    textRect = text.get_rect()
    textRect.topleft = (48+83*(i+1), 709)
    screen.blit(text, textRect)
    text = font.render(str(i+1), True, (255,255,255))
    textRect = text.get_rect()
    textRect.topleft = (74, 83*(i+1)-8)
    screen.blit(text, textRect)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()