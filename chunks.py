import pygame

import pickle

from settings import *
from GraphicsLoader import graphics
from worldgen import world_generate_chunk

class Chunks():
    def __init__(self):
        self.chunks = {}

        try:
            map_file = open("map.save", "rb")
            self.chunks = pickle.load(map_file)
            map_file.close()
        except:
            pass

    def save_chunks(self):
        map_file = open("map.save", "wb")
        map_file = pickle.dump(self.chunks, map_file)
        print("Chunks Saved!")

    def generate_chunk(self, chunk_index, current_chunk_x, current_chunk_y):
        generated_chunk = world_generate_chunk(current_chunk_x, current_chunk_y)
        self.chunks[chunk_index] = generated_chunk

    def load_chunk(self, current_chunk_x, current_chunk_y):
        chunk_index = str(current_chunk_x)+";"+str(current_chunk_y)
        try:
            loaded_chunk = self.chunks[chunk_index]
        except:
            self.generate_chunk(chunk_index, current_chunk_x, current_chunk_y)
            loaded_chunk = self.chunks[chunk_index]

        return loaded_chunk

    def render_chunk(self, screen, PLAYER_CHUNK, OFFSET):
        for chy in range(3):
            current_chunk_y = chy+PLAYER_CHUNK[1]-1
            for chx in range(3):
                current_chunk_x = chx+PLAYER_CHUNK[0]-1
                render_chunk = self.load_chunk(current_chunk_x, current_chunk_y)

                for idy in range(CHUNK_SIZE):
                    top_y = (TILE_SIZE * idy + (current_chunk_y) * TILE_SIZE * CHUNK_SIZE) - OFFSET[1]
                    for idx in range(CHUNK_SIZE):
                        top_x = (TILE_SIZE * idx + (current_chunk_x) * TILE_SIZE * CHUNK_SIZE) - OFFSET[0]
                        if top_x < WIDTH and top_x > -32 or top_y > HEIGHT and top_y < -32:
                            # render_chunk[idy][idx].color
                            screen.blit(graphics[render_chunk[idy][idx].tile_name],  (top_x,top_y))
                            # pygame.draw.rect(screen, render_chunk[idy][idx].color, (top_x,top_y,TILE_SIZE,TILE_SIZE))