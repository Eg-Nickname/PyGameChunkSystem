from json import load
import os
import pygame

def load_graphics(path):
    graphics = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            img = pygame.image.load(os.path.join(subdir, file)).convert_alpha()
            graphics[str(file.removesuffix('.png'))] = img
    return graphics