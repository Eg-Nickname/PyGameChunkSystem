import pygame
from pygame.locals import *
from math import floor, radians
from settings import *

# Pygame init stuff
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT),SCALED,OPENGL)

# Engine imports
from chunks import Chunks
from camera import calculate_offset
from player import Player
from particles import Particle
from GraphicsLoader import graphics



particle_light = pygame.transform.scale(pygame.image.load("./static_graphics/particle_light.png").convert_alpha(),(12,12))

particles = []

chunks = Chunks()
sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

def draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK, selected_tile, particles):
    chunks.render_chunk(screen, PLAYER_CHUNK, (OFFSET_X, OFFSET_Y))

    for particle in particles:
        screen.blit(particle_light, (particle.pos_x-OFFSET_X-2, particle.pos_y-OFFSET_Y-2), special_flags=BLEND_RGB_ADD)
        screen.blit(particle.image, (particle.pos_x-OFFSET_X, particle.pos_y-OFFSET_Y))

    # Render graphic on top of tile that cursor is on top of
    screen.blit(graphics["tile_select"], (selected_tile[0]-OFFSET_X-2, selected_tile[1]-OFFSET_Y-2))

    
    screen.blit(player.image, (player.position_x - OFFSET_X, player.position_y - OFFSET_Y))
    FPS = str(int(clock.get_fps()))
    pygame.display.set_caption(FPS)
    # print(FPS)
    pygame.display.update()

loop = True
while loop:
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
    	if event.type == pygame.QUIT:
            loop = False

    player.movement(pressed_keys)
    OFFSET_X, OFFSET_Y = calculate_offset(player)

    # Circle effect

    if pressed_keys[118]:
        if DELTA_TIME-player.attack_delay>player.last_attack:
            player.last_attack = DELTA_TIME
            for particle in range(15):
                rotation = pygame.math.Vector2(1.5,0).rotate_rad(radians((360/15)*particle))
                particles.append(Particle(player.position_x+16, player.position_y+16, rotation, DELTA_TIME))
    
    # Spirall Effect

    # if pressed_keys[98]:
    #     if DELTA_TIME-player.attack_delay>player.last_attack:
    #         player.last_attack = DELTA_TIME
    #         for particle in range(15):
    #             rotation = pygame.math.Vector2(1,0).rotate_rad(radians((360/15)*particle))*particle/5
    #             particles.append(Particle(player.position_x+16, player.position_y+16, rotation, DELTA_TIME))


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

    

    DELTA_TIME += 1

    # if DELTA_TIME%120 == 1:
        # print("---------------------------------------------------")
        # print("Player Pos",player.position_x, " | ", player.position_y)
        # print("Mouse World Tile Pos", mouse_pos_x, " | ", mouse_pos_y)
        # print("Pisel perf mouse", mouse_pos)
        # print("Chunk", floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), " | ",  floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))
        # print("---------------------------------------------------")
    
    PLAYER_CHUNK = (floor((player.position_x)/(CHUNK_SIZE*TILE_SIZE)), floor((player.position_y)/(CHUNK_SIZE*TILE_SIZE)))



    if DELTA_TIME% CHUNKS_SAVE_DELAY == 1:
        chunks.save_chunks()

    draw(player, OFFSET_X, OFFSET_Y, PLAYER_CHUNK, selected_tile, particles)
    clock.tick() # fps
pygame.quit()