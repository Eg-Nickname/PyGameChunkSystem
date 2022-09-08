from opensimplex import OpenSimplex
from GraphicsLoader import biome_list, graphics
from settings import *
from math import floor
import random
import pickle
import pygame

# World gen settings
map_seed = 2137
WATER_LEVEL = -0.5
GROUND_SIZE = 40

elevation_noise = OpenSimplex(map_seed)
random.seed(map_seed)

# Map save load
try:
    regions_file = open("regions.save", "rb")
    regions = pickle.load(regions_file)
    regions_file.close()
except:
        regions = dict()


def save_regions():
        regions_file = open("regions.save", "wb")
        regions_file = pickle.dump(regions, regions_file)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x , pos_y, biome=None, tile_type=None, collidable=None):
        super().__init__()
        self.position_x = pos_x*32
        self.position_y = pos_y*32

        self.biome = biome or ""
        self.tile_type = tile_type or "empty"
        self.has_collision = collidable or False

        if self.tile_type != "empty":
            self.tile_name = self.biome+"_"+self.tile_type
        else:
            self.tile_name = "empty"
        self.rect = graphics[self.tile_name].get_rect()
        self.rect.topleft = [self.position_x, self.position_y]
        self.hitbox = self.rect

    def update_tile(self, tile_type, collision):
        self.tile_type = tile_type
        self.has_collision = collision
        if self.tile_type != "empty":
            self.tile_name = self.biome+"_"+self.tile_type
        else:
            self.tile_name = "empty"
        self.rect = graphics[self.tile_name].get_rect()

class BiomeRegion():
    def __init__(self, pos_str, region_pos):
        self.pos_x      = random.randrange(0, (CHUNK_SIZE*REGION_SIZE)-1)+(region_pos[0]*(REGION_SIZE*CHUNK_SIZE))
        self.pos_y      = random.randrange(0, (CHUNK_SIZE*REGION_SIZE)-1)+(region_pos[1]*(REGION_SIZE*CHUNK_SIZE))
        self.pos_str    = pos_str
        self.biome      = biome_list[random.randrange(0,len(biome_list))]
        self.generate_biome(region_pos)


    def generate_biome(self, region_pos):
        neighboring_regions = list()
        neighboring_regions.append(str(region_pos[0])+";"+str(region_pos[1]-1))
        neighboring_regions.append(str(region_pos[0]-1)+";"+str(region_pos[1]))
        neighboring_regions.append(str(region_pos[0]+1)+";"+str(region_pos[1]))
        neighboring_regions.append(str(region_pos[0])+";"+str(region_pos[1]+1))

        rechosen = True
        while rechosen:
            rechosen = False
            for neighboring_region in neighboring_regions:
                try:
                    biome = regions[neighboring_region].biome
                    if self.biome == biome:
                        self.biome = biome_list[random.randrange(0,len(biome_list))]
                        rechosen = True
                except:
                    pass


def calculate_region(pos_x, pos_y):
    return (floor((pos_x)/(CHUNK_SIZE*REGION_SIZE)), floor((pos_y)/(CHUNK_SIZE*REGION_SIZE)))


def calc_nearest_region_point(region_pos, pos_x, pos_y):
    points = []
    for y in range(3):
        for x in range(3):
            region_pos_str = str(region_pos[0]+x-1)+";"+str(region_pos[1]+y-1)
            try:
                region_pos_x = regions[region_pos_str].pos_x
                region_pos_y = regions[region_pos_str].pos_y
            except:
                regions[region_pos_str] = BiomeRegion(region_pos_str, (region_pos[0]+x-1, region_pos[1]+y-1))
                region_pos_x = regions[region_pos_str].pos_x
                region_pos_y = regions[region_pos_str].pos_y 

            points.append((region_pos_x, region_pos_y, region_pos_str))


    distance = 11111111111
    nearest_point = ""
    for point in points:
        point_distance = ((pos_x-point[0])**2) + ((pos_y-point[1])**2)
        if point_distance < distance:
            distance = point_distance
            nearest_point = point[2]
    return nearest_point


def generate_biome_features(pos_x, pos_y, biome):
    tile_seed = random.randrange(0,40)
    collidable = False
    tile_type = ""
    if tile_seed==5:
        tile_type = "rock"
        collidable = True
    elif tile_seed > 30:
        tile_type = "grass"+str(random.randrange(1,4))
    return Tile(pos_x, pos_y, biome, tile_type, collidable)


def world_generate_chunk(current_chunk_x, current_chunk_y):
        generated_chunk = []
        chunk_top_left = (current_chunk_x*CHUNK_SIZE,current_chunk_y*CHUNK_SIZE)
        for idy in range(CHUNK_SIZE):
            row = []
            tile_top_left_y = (chunk_top_left[1]+idy)
            for idx in range(CHUNK_SIZE):
                tile_top_left_x = (chunk_top_left[0]+idx)

                # Biome determination
                region_pos = calculate_region(tile_top_left_x, tile_top_left_y)
                biome = regions[calc_nearest_region_point(region_pos, tile_top_left_x, tile_top_left_y)].biome

                # Water land selection
                noise00 = elevation_noise.noise2(tile_top_left_x/GROUND_SIZE, tile_top_left_y/GROUND_SIZE)

                # Tile graphic selection
                tile_name = "grass"
                layer1_tile_collision = False
                layer2_tile = Tile(tile_top_left_x, tile_top_left_y, biome)
                if noise00>WATER_LEVEL:
                    layer1_tile_name = "grass"
                    layer2_tile = generate_biome_features(tile_top_left_x, tile_top_left_y, biome)
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
                    else:
                        layer1_tile_collision = True
                    layer1_tile_name = "water"+water_img
                # layer1_tile_name=biome+"_"+layer1_tile_name
            

                level = []
                level.append(Tile(tile_top_left_x, tile_top_left_y, biome, layer1_tile_name, layer1_tile_collision))
                level.append(layer2_tile)

                row.append(level)

            generated_chunk.append(row)
        return generated_chunk