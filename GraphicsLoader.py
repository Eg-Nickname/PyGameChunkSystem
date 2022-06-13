from lib2to3.pgen2.pgen import generate_grammar
import os
import pygame

biome_list = ["candy", "toxic", "death"]

base_pallete = [pygame.Color("#fdf1f2"), pygame.Color("#f3c4d8"), pygame.Color("#e18dcb"), pygame.Color("#c760bc"), pygame.Color("#b44db7"), pygame.Color("#783a8d"), pygame.Color("#603b7f"), pygame.Color("#2f2442")]

color_palletes = [
    [pygame.Color("#fdf1f2"), pygame.Color("#f3c4d8"), pygame.Color("#e18dcb"), pygame.Color("#c760bc"), pygame.Color("#b44db7"), pygame.Color("#783a8d"), pygame.Color("#603b7f"), pygame.Color("#2f2442")],
    [pygame.Color("#eeffcc"), pygame.Color("#bedc7f"), pygame.Color("#89a257"), pygame.Color("#4d8061"), pygame.Color("#305d42"), pygame.Color("#1e3a29"), pygame.Color("#112318"), pygame.Color("#040c06")],
    [pygame.Color("#9ba9ab"), pygame.Color("#7c8893"), pygame.Color("#5d687c"), pygame.Color("#444a65"), pygame.Color("#30324d"), pygame.Color("#26203a"), pygame.Color("#23132d"), pygame.Color("#1e0721")],
    
    # [pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color("")],
]

def generate_biome_graphics(list, file, img):
    graphics = list
    for bid, biome in enumerate(biome_list):
        img_copy = img
        for cid, color in enumerate(base_pallete): 
            img_copy = palette_swap(img_copy, base_pallete[cid], color_palletes[bid][cid])
            # img_copy.fill(color_palletes[bid][cid])
            # img.set_colorkey(base_pallete[cid])
            # img_copy.blit(img, (0, 0))
        graphics[str(biome)+"_"+str(file.removesuffix('.png'))] = img_copy
    return graphics



def load_graphics(path):
    graphics = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            img = pygame.image.load(os.path.join(subdir, file)).convert_alpha()
            if subdir.startswith('.\static_graphics\map'):
                graphics = generate_biome_graphics(graphics, file, img)
            else:
                graphics[str(file.removesuffix('.png'))] = img
    return graphics

graphics = load_graphics(".\static_graphics")



# def loadgraphics():
#     for biome in bioms:
#         for file in directory:
#             # some stuff changing colors
#             graphics[str(biome)+str(file.removesuffix('.png'))] = img
