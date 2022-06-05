import pygame
from pygame.locals import *
from math import floor

from settings import *
from camera import calculate_offset
from player import Player

pygame.init()

pygame.display.set_caption("Chunk System")

screen = pygame.display.set_mode((WIDTH, HEIGHT),SCALED,OPENGL)


clock = pygame.time.Clock()



sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

loop = 1
# print(w, " ", h)
def draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK, selected_tile):
    screen.fill((0,0,0))
    for chy in range(3):
        for chx in range(3):
            for idy in range(CHUNK_SIZE):
                for idx in range(CHUNK_SIZE):
                    top_x = (TILE_SIZE * idx + (chx+PLAYER_CHUNK[0]-1) * TILE_SIZE * CHUNK_SIZE) - OFFSET_X
                    top_y = (TILE_SIZE * idy + (chy+PLAYER_CHUNK[1]-1) * TILE_SIZE * CHUNK_SIZE) - OFFSET_Y
                    if top_x < WIDTH and top_x > -32 or top_y > HEIGHT and top_y < -32:
                        if (selected_tile[0], selected_tile[1]) == (top_x+OFFSET_X, top_y+OFFSET_Y):
                            pygame.draw.rect(screen, (255,0,0), (top_x,top_y,TILE_SIZE,TILE_SIZE))
                        else:
                            pygame.draw.rect(screen, (idy*12,idx*12,100), (top_x,top_y,TILE_SIZE,TILE_SIZE))


    
    screen.blit(player.image, (player.position_x - OFFSET_X, player.position_y - OFFSET_Y))
    FPS = str(int(clock.get_fps()))
    pygame.display.update()

while loop:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
            loop = 0

    player.movement(pressed_keys)
    OFFSET_X, OFFSET_Y = calculate_offset(player)

    pygame.mouse.get_visible()
    mouse_pos = pygame.mouse.get_pos()

    player.position_x - player.position_x%TILE_SIZE

    mouse_pos_x = mouse_pos[0]  + player.position_x - 320
    mouse_pos_y = mouse_pos[1]-19  + player.position_y - 160

    mouse_pos_x = mouse_pos_x - mouse_pos_x%TILE_SIZE
    mouse_pos_y = mouse_pos_y - mouse_pos_y%TILE_SIZE




    selected_tile = (mouse_pos_x,mouse_pos_y)
    # print(selected_tile)   
    
    clock.tick(60) # fps
    DELTA_TIME += 1

    if DELTA_TIME%120 == 1:
        print("---------------------------------------------------")
        print("Player Pos",player.position_x, " | ", player.position_y)
        print("Mouse World Tile Pos", mouse_pos_x, " | ", mouse_pos_y)
        print("Pisel perf mouse", mouse_pos)
        # print("Chunk", floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), " | ",  floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
        print("---------------------------------------------------")
    
    PLAYER_CHUNK = (floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
        


    draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK, selected_tile)

pygame.quit()