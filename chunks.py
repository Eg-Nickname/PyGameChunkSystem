import pygame

import pickle
from math import floor
from functools import lru_cache


from settings import *
from GraphicsLoader import graphics
from worldgen import world_generate_chunk, save_regions


# Working with chunks 
@lru_cache
def load_chunk(current_chunk_x, current_chunk_y):
    chunk_index = str(current_chunk_x)+";"+str(current_chunk_y)
    try:
        chunk_file = open(f'{save_path}/chunks/{chunk_index}.save', "rb")
        chunk = pickle.load(chunk_file)
        chunk_file.close()
        return chunk
    except:
        generated_chunk = world_generate_chunk(current_chunk_x, current_chunk_y)
        chunk_file = open(f'{save_path}/chunks/{chunk_index}.save', "wb")
        chunk_file = pickle.dump(generated_chunk, chunk_file)
        return generated_chunk

def save_chunk(chunk_index, chunk):
        chunk_file = open(f'{save_path}/chunks/{chunk_index}.save', "wb")
        chunk_file = pickle.dump(chunk, chunk_file)

def get_chunk_pos(pos_x, pos_y):
    return (floor(pos_x/(CHUNK_SIZE*TILE_SIZE)), floor(pos_y/(CHUNK_SIZE*TILE_SIZE)))

def get_tile(pos_x, pos_y):
    chunk_pos = get_chunk_pos(pos_x, pos_y)
    chunk = load_chunk(chunk_pos[0], chunk_pos[1])
    tile_pos = (floor((pos_x-(CHUNK_SIZE*TILE_SIZE*chunk_pos[0]))/TILE_SIZE), floor((pos_y-(CHUNK_SIZE*TILE_SIZE*chunk_pos[1]))/TILE_SIZE))
    return chunk[tile_pos[1]][tile_pos[0]]

def render_chunk(screen, PLAYER_CHUNK, OFFSET, player):
        player.collision_objects.empty()
        for chy in range(3):
            current_chunk_y = chy+PLAYER_CHUNK[1]-1
            for chx in range(3):
                current_chunk_x = chx+PLAYER_CHUNK[0]-1
                render_chunk = load_chunk(current_chunk_x, current_chunk_y)

                for idy in range(CHUNK_SIZE):
                    top_y = (TILE_SIZE * idy + (current_chunk_y) * TILE_SIZE * CHUNK_SIZE) - OFFSET[1]
                    for idx in range(CHUNK_SIZE):
                        top_x = (TILE_SIZE * idx + (current_chunk_x) * TILE_SIZE * CHUNK_SIZE) - OFFSET[0]
                        if top_x < WIDTH and top_x > -32 or top_y > HEIGHT and top_y < -32:
                            for layer in range(2):
                                tile = render_chunk[idy][idx][layer]
                                if tile.tile_name != "empty":
                                    screen.blit(graphics[tile.tile_name],  (top_x,top_y))
                                if tile.has_collision:
                                    player.collision_objects.add(tile)


# Old
# class Chunks():
#     def __init__(self, player):
#         self.chunks = {}
#         self.player = player

#         try:
#             map_file = open("map.save", "rb")
#             self.chunks = pickle.load(map_file)
#             map_file.close()
#         except:
#             pass

#     def save_chunks(self):
#         map_file = open("map.save", "wb")
#         map_file = pickle.dump(self.chunks, map_file)
#         save_regions()
#         print("Chunks Saved!")

#     def generate_chunk(self, chunk_index, current_chunk_x, current_chunk_y):
#         generated_chunk = world_generate_chunk(current_chunk_x, current_chunk_y)
#         self.chunks[chunk_index] = generated_chunk

#     def load_chunk(self, current_chunk_x, current_chunk_y):
#         chunk_index = str(current_chunk_x)+";"+str(current_chunk_y)
#         try:
#             loaded_chunk = self.chunks[chunk_index]
#         except:
#             self.generate_chunk(chunk_index, current_chunk_x, current_chunk_y)
#             loaded_chunk = self.chunks[chunk_index]
#         return loaded_chunk

#     def get_chunk_pos(self, pos_x, pos_y):
#         return (floor(pos_x/(CHUNK_SIZE*TILE_SIZE)), floor(pos_y/(CHUNK_SIZE*TILE_SIZE)))

#     def get_tile(self, pos_x, pos_y):
#         chunk_pos = self.get_chunk_pos(pos_x, pos_y)
#         chunk = self.load_chunk(chunk_pos[0], chunk_pos[1])
#         (CHUNK_SIZE*TILE_SIZE*chunk_pos[0])
#         tile_pos = (floor((pos_x-(CHUNK_SIZE*TILE_SIZE*chunk_pos[0]))/TILE_SIZE), floor((pos_y-(CHUNK_SIZE*TILE_SIZE*chunk_pos[1]))/TILE_SIZE))
#         return chunk[tile_pos[1]][tile_pos[0]]

#     def render_chunk(self, screen, PLAYER_CHUNK, OFFSET):
#         self.player.collision_objects.empty()
#         for chy in range(3):
#             current_chunk_y = chy+PLAYER_CHUNK[1]-1
#             for chx in range(3):
#                 current_chunk_x = chx+PLAYER_CHUNK[0]-1
#                 render_chunk = self.load_chunk(current_chunk_x, current_chunk_y)

#                 for idy in range(CHUNK_SIZE):
#                     top_y = (TILE_SIZE * idy + (current_chunk_y) * TILE_SIZE * CHUNK_SIZE) - OFFSET[1]
#                     for idx in range(CHUNK_SIZE):
#                         top_x = (TILE_SIZE * idx + (current_chunk_x) * TILE_SIZE * CHUNK_SIZE) - OFFSET[0]
#                         if top_x < WIDTH and top_x > -32 or top_y > HEIGHT and top_y < -32:
#                             for layer in range(3):
#                                 tile = render_chunk[idy][idx][layer]
#                                 if tile.tile_name != "empty":
#                                     screen.blit(graphics[tile.tile_name],  (top_x,top_y))
#                                 if tile.has_collision:
#                                     self.player.collision_objects.add(tile)
