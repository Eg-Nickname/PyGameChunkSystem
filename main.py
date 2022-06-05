from turtle import position
import pygame
from pygame.locals import *
from math import floor, radians

from settings import *
from camera import calculate_offset
from player import Player
from particles import Particle

pygame.init()

pygame.display.set_caption("Chunk System")
screen = pygame.display.set_mode((WIDTH, HEIGHT),SCALED,OPENGL)
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

particles = []

loop = 1
# print(w, " ", h)
def draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK, selected_tile, particles):
    screen.fill((0,0,0))
    for chy in range(3):
        for chx in range(3):
            for idy in range(CHUNK_SIZE):
                for idx in range(CHUNK_SIZE):
                    top_x = (TILE_SIZE * idx + (chx+PLAYER_CHUNK[0]-1) * TILE_SIZE * CHUNK_SIZE) - OFFSET_X
                    top_y = (TILE_SIZE * idy + (chy+PLAYER_CHUNK[1]-1) * TILE_SIZE * CHUNK_SIZE) - OFFSET_Y
                    if top_x < WIDTH and top_x > -32 or top_y > HEIGHT and top_y < -32:
                            pygame.draw.rect(screen, (idy*12,idx*12,100), (top_x,top_y,TILE_SIZE,TILE_SIZE))
    
    for particle in particles:
        pygame.draw.circle(screen, (255,255,255), (particle.pos_x-OFFSET_X, particle.pos_y-OFFSET_Y), 8)
        pygame.draw.circle(screen, (255,0,0), (particle.pos_x-OFFSET_X, particle.pos_y-OFFSET_Y), 6)

    # Render graphic on top of tile that cursor is on top of
    screen.blit(pygame.image.load("tile_select.png"), (selected_tile[0]-OFFSET_X-2, selected_tile[1]-OFFSET_Y-2))

    
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

    if pressed_keys[118]:
        for particle in range(15):
            rotation = pygame.math.Vector2(1.5,0).rotate_rad(radians((360/15)*particle))
            particles.append(Particle(player.position_x+16, player.position_y+16, rotation, DELTA_TIME))


    for particle in particles:
        particle.update_pos()
        if DELTA_TIME > particle.life_span + particle.creation_time:
            particles.remove(particle)







    pygame.mouse.get_visible()
    mouse_pos = pygame.mouse.get_pos()

    player.position_x - player.position_x%TILE_SIZE

    mouse_pos_x = mouse_pos[0]  + player.position_x - 320
    mouse_pos_y = mouse_pos[1]-19  + player.position_y - 160

    mouse_pos_x = mouse_pos_x - mouse_pos_x%TILE_SIZE
    mouse_pos_y = mouse_pos_y - mouse_pos_y%TILE_SIZE




    selected_tile = (mouse_pos_x,mouse_pos_y)
    # print(selected_tile)   
    

    DELTA_TIME += 1

    # if DELTA_TIME%120 == 1:
    #     print("---------------------------------------------------")
    #     print("Player Pos",player.position_x, " | ", player.position_y)
    #     print("Mouse World Tile Pos", mouse_pos_x, " | ", mouse_pos_y)
    #     print("Pisel perf mouse", mouse_pos)
    #     # print("Chunk", floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), " | ",  floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
    #     print("---------------------------------------------------")
    
    PLAYER_CHUNK = (floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
        


    draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK, selected_tile, particles)
    clock.tick(60) # fps
pygame.quit()