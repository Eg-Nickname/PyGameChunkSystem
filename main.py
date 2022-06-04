from math import floor
import pygame
from pygame.locals import *

from player import Player

pygame.init()

pygame.display.set_caption("Chunk System")

screen = pygame.display.set_mode((640,360),SCALED,OPENGL)
w, h = pygame.display.get_surface().get_size()

clock = pygame.time.Clock()

DELTA_TIME = 0
TILE_SIZE = 32
CHUNK_SIZE = 10

sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

loop = 1
# print(w, " ", h)
def draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK):
    screen.fill((0,0,0))
    for chy in range(3):
        for chx in range(3):
            for idy in range(CHUNK_SIZE):
                for idx in range(CHUNK_SIZE):
                    top_x = (TILE_SIZE * idx + (chx+PLAYER_CHUNK[0]-1) * TILE_SIZE * CHUNK_SIZE) - OFFSET_X
                    top_y = (TILE_SIZE * idy + (chy+PLAYER_CHUNK[1]-1) * TILE_SIZE * CHUNK_SIZE) - OFFSET_Y
                    if top_x < w and top_x > -32 or top_y > h and top_y < -32:
                        pygame.draw.rect(screen, (idy*12,idx*12,100), (top_x,top_y,TILE_SIZE,TILE_SIZE))

    
    screen.blit(player.image, (player.position_x - OFFSET_X, player.position_y - OFFSET_Y))
    FPS = str(int(clock.get_fps()))
    pygame.display.update()

while loop:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
            loop = 0

    if pressed_keys[K_d]:
    	if player.velocity_x < player.max_x_velocity:
            player.velocity_x+=player.velocity_x_increse

    if pressed_keys[K_a]:	
        if player.velocity_x > -player.max_x_velocity:
            player.velocity_x-=player.velocity_x_increse

    if pressed_keys[K_w]:	
        if player.velocity_y > -player.max_y_velocity:
            player.velocity_y-=player.velocity_y_increse

    if pressed_keys[K_s]:
    	if player.velocity_y < player.max_x_velocity:
            player.velocity_y+=player.velocity_x_increse

    player.position_x += int(player.velocity_x/100)
    player.position_y += int(player.velocity_y/100)

    # Player position and State
    if player.velocity_x>0:
        player.velocity_x-=15
    elif player.velocity_x<0:
        player.velocity_x+=15

    if player.velocity_y>0:
        player.velocity_y-=15
    elif player.velocity_y<0:
        player.velocity_y+=15

    # print(player.position_x, "|", player.position_y)

    OFFSET_X = player.position_x - 320
    OFFSET_Y = player.position_y - 180
    
    
    clock.tick(60) # fps
    DELTA_TIME += 1

    if DELTA_TIME%60 == 1:
        print("---------------------------------------------------")
        print("Player Pos",player.position_x, " | ", player.position_y)
        print("Chunk", floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), " | ",  floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
        print("---------------------------------------------------")
    PLAYER_CHUNK = (floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
        


    draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK)

pygame.quit()