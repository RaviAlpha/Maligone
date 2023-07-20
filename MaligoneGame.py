import pygame
import sys

pygame.init()

# set window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 6 / 8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# set caption
pygame.display.set_caption('Maligone: Origin')

#set frame rate
clock = pygame.time.Clock()
FPS = 60


run = True

while run:

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # run = False
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
