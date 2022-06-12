from opensimplex import OpenSimplex
from GraphicsLoader import graphics

elevation_noise_seed = 2137
moisture_noise_seed = 4321
temp_noise_seed = 51515


elevation_noise = OpenSimplex(elevation_noise_seed)
moisture_noise = OpenSimplex(moisture_noise_seed)
temp_noise = OpenSimplex(temp_noise_seed)

from settings import *

class Tile():
    def __init__(self, tile_name=None):
        self.tile_name = tile_name or "placeholder"



water_level = -0.0009
def world_generate_chunk(current_chunk_x, current_chunk_y):
        generated_chunk = []
        chunk_top_left = (current_chunk_x*CHUNK_SIZE,current_chunk_y*CHUNK_SIZE)
        for idy in range(CHUNK_SIZE):
            row = []
            tile_top_left_y = (chunk_top_left[1]+idy)
            for idx in range(CHUNK_SIZE):
                tile_top_left_x = (chunk_top_left[0]+idx)
                
                noise00 = elevation_noise.noise2(tile_top_left_x/100, tile_top_left_y/100)
                mn=moisture_noise.noise2(tile_top_left_x/100, tile_top_left_y/100)
                tn=temp_noise.noise2(tile_top_left_x/100, tile_top_left_y/100)
                # print(mn+tn)
                if noise00>water_level:
                    row.append(Tile("grass"))
                else:
                    noise0_1    = elevation_noise.noise2(tile_top_left_x/100, (tile_top_left_y-1)/100)     
                    noise_10    = elevation_noise.noise2((tile_top_left_x-1)/100, tile_top_left_y/100)
                    noise10     = elevation_noise.noise2((tile_top_left_x+1)/100, tile_top_left_y/100)
                    noise01     = elevation_noise.noise2(tile_top_left_x/100, (tile_top_left_y+1)/100) 
                    water_img = str(int(noise0_1>water_level))+str(int(noise_10>water_level))+str(int(noise10>water_level))+str(int(noise01>water_level))
                    if water_img == "0000":
                        if elevation_noise.noise2((tile_top_left_x-1)/100, (tile_top_left_y-1)/100)>water_level:
                            water_img += "_1000"
                        elif elevation_noise.noise2((tile_top_left_x+1)/100, (tile_top_left_y-1)/100)>water_level:
                            water_img += "_0100"
                        elif elevation_noise.noise2((tile_top_left_x-1)/100, (tile_top_left_y+1)/100)>water_level:
                            water_img += "_0010"
                        elif elevation_noise.noise2((tile_top_left_x+1)/100, (tile_top_left_y+1)/100)>water_level:
                            water_img += "_0001"
                        else:
                            water_img == "0000"

                    row.append(Tile("water"+water_img))
            generated_chunk.append(row)
        return generated_chunk