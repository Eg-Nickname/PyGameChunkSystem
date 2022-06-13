from opensimplex import OpenSimplex
from GraphicsLoader import graphics

# World gen settings
elevation_noise_seed = 2137
moisture_noise_seed = 4321
temp_noise_seed = 51515
WATER_LEVEL = -0.1
GROUND_SIZE = 20
BIOME_SIZE = 20


elevation_noise = OpenSimplex(elevation_noise_seed)
moisture_noise = OpenSimplex(moisture_noise_seed)
temp_noise = OpenSimplex(temp_noise_seed)

from settings import *

class Tile():
    def __init__(self, tile_name=None):
        self.tile_name = tile_name or "placeholder"

def world_generate_chunk(current_chunk_x, current_chunk_y):
        generated_chunk = []
        chunk_top_left = (current_chunk_x*CHUNK_SIZE,current_chunk_y*CHUNK_SIZE)
        for idy in range(CHUNK_SIZE):
            row = []
            tile_top_left_y = (chunk_top_left[1]+idy)
            for idx in range(CHUNK_SIZE):
                tile_top_left_x = (chunk_top_left[0]+idx)
                
                noise00 = elevation_noise.noise2(tile_top_left_x/GROUND_SIZE, tile_top_left_y/GROUND_SIZE)
                mn=moisture_noise.noise2(tile_top_left_x/BIOME_SIZE, tile_top_left_y/BIOME_SIZE)
                tn=temp_noise.noise2(tile_top_left_x/BIOME_SIZE, tile_top_left_y/GROUND_SIZE)
                # print(mn+tn)

                tile_name = "grass"
                if noise00>WATER_LEVEL:
                    tile_name = "grass"
                else:
                    noise0_1    = elevation_noise.noise2(tile_top_left_x/GROUND_SIZE, (tile_top_left_y-1)/GROUND_SIZE)     
                    noise_10    = elevation_noise.noise2((tile_top_left_x-1)/GROUND_SIZE, tile_top_left_y/GROUND_SIZE)
                    noise10     = elevation_noise.noise2((tile_top_left_x+1)/GROUND_SIZE, tile_top_left_y/GROUND_SIZE)
                    noise01     = elevation_noise.noise2(tile_top_left_x/GROUND_SIZE, (tile_top_left_y+1)/GROUND_SIZE) 
                    water_img = str(int(noise0_1>WATER_LEVEL))+str(int(noise_10>WATER_LEVEL))+str(int(noise10>WATER_LEVEL))+str(int(noise01>WATER_LEVEL))
                    if water_img == "0000":
                        if elevation_noise.noise2((tile_top_left_x-1)/GROUND_SIZE, (tile_top_left_y-1)/GROUND_SIZE)>WATER_LEVEL:
                            water_img += "_1000"
                        elif elevation_noise.noise2((tile_top_left_x+1)/GROUND_SIZE, (tile_top_left_y-1)/GROUND_SIZE)>WATER_LEVEL:
                            water_img += "_0100"
                        elif elevation_noise.noise2((tile_top_left_x-1)/GROUND_SIZE, (tile_top_left_y+1)/GROUND_SIZE)>WATER_LEVEL:
                            water_img += "_0010"
                        elif elevation_noise.noise2((tile_top_left_x+1)/GROUND_SIZE, (tile_top_left_y+1)/GROUND_SIZE)>WATER_LEVEL:
                            water_img += "_0001"
                        else:
                            water_img == "0000"
                    tile_name = "water"+water_img
                
                if mn<-0.6:
                    tile_name="death_"+tile_name
                elif mn<0.3:
                    tile_name="toxic_"+tile_name
                else:
                    tile_name="candy_"+tile_name

                row.append(Tile(tile_name))
            generated_chunk.append(row)
        return generated_chunk