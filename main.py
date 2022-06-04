import pygame
from pygame.locals import *

pygame.init()

pygame.display.set_caption("Chunk System")

screen = pygame.display.set_mode((640,370),SCALED,OPENGL)
clock = pygame.time.Clock()

DELTA_TIME = 0
TILE_SIZE = 16
CHUNK_SIZE = 16

loop = 1

def draw():
    TILE_COUNT = 0
    for chy in range(2):
        for chx in range(3):
            for idy in range(CHUNK_SIZE):
                for idx in range(CHUNK_SIZE):
                    top_x = TILE_SIZE * idx + chx * TILE_SIZE * CHUNK_SIZE
                    top_y = TILE_SIZE * idy + chy * TILE_SIZE * CHUNK_SIZE
                    TILE_COUNT += 1
                    pygame.draw.rect(screen, (idy*12,idx*12,100), (top_x,top_y,TILE_SIZE,TILE_SIZE))

    pygame.display.update()

while loop:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
            loop = 0

    
    clock.tick(60) # fps
    DELTA_TIME += 1

    if DELTA_TIME%60 == 1:
        print()
    draw()

pygame.quit()