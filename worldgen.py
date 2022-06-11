import opensimplex as simplex
import random

elevation_noise_seed = 1234
moisture_noise_seed = 4321
simplex.seed(elevation_noise_seed)

from settings import *

class Tile():
    def __init__(self, color=None):
        self.color = color or (random.randint(0,255), random.randint(0,255), random.randint(0,255))

def elevation_noise(tile_index_x, tile_index_y):
    simplex.seed(elevation_noise_seed)
    return simplex.noise2(tile_index_x, tile_index_y)

def moisture_noise(tile_index_x, tile_index_y):
    simplex.seed(moisture_noise_seed)
    return simplex.noise2(tile_index_x, tile_index_y)



def world_generate_chunk(current_chunk_x, current_chunk_y):
        generated_chunk = []
        chunk_top_left = (current_chunk_x*CHUNK_SIZE,current_chunk_y*CHUNK_SIZE)
        for idy in range(CHUNK_SIZE):
            row = []
            tile_top_left_y = (chunk_top_left[1]+idy)/100
            for idx in range(CHUNK_SIZE):
                tile_top_left_x = (chunk_top_left[0]+idx)/100
                noise = elevation_noise(tile_top_left_x, tile_top_left_y)
                if noise>0:
                    row.append(Tile((0,255,0)))
                else:
                    row.append(Tile((0,0,255)))
            generated_chunk.append(row)
        return generated_chunk