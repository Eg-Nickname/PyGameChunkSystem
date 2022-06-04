import chunk
import pygame

pygame.init()

pygame.display.set_caption("Chunk System")

screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()

DELTA_TIME = 0
TILE_SIZE = 32
CHUNK_SIZE = 8

loop = 1

def draw():

    for idy in range(CHUNK_SIZE):
        for idx in range(CHUNK_SIZE):
            top_x = TILE_SIZE * idx
            top_y = TILE_SIZE * idy
            pygame.draw.rect(screen, (idy*10,idx*10,150), (top_x,top_y,TILE_SIZE,TILE_SIZE))



    pygame.display.update()

while loop:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
            loop = 0

    
    clock.tick(60) # fps
    DELTA_TIME += 1
    draw()

pygame.quit()