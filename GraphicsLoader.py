import os
import pygame

biome_list = ["candy", "toxic", "death", "desert", "swamp", "fire"]

base_pallete = [pygame.Color("#fdf1f2"), pygame.Color("#f3c4d8"), pygame.Color("#e18dcb"), pygame.Color("#c760bc"), pygame.Color("#b44db7"), pygame.Color("#783a8d"), pygame.Color("#603b7f"), pygame.Color("#2f2442")]

color_palletes = [
    [pygame.Color("#fdf1f2"), pygame.Color("#f3c4d8"), pygame.Color("#e18dcb"), pygame.Color("#c760bc"), pygame.Color("#b44db7"), pygame.Color("#783a8d"), pygame.Color("#603b7f"), pygame.Color("#2f2442")],
    [pygame.Color("#eeffcc"), pygame.Color("#bedc7f"), pygame.Color("#89a257"), pygame.Color("#4d8061"), pygame.Color("#305d42"), pygame.Color("#1e3a29"), pygame.Color("#112318"), pygame.Color("#040c06")],
    [pygame.Color("#9ba9ab"), pygame.Color("#7c8893"), pygame.Color("#5d687c"), pygame.Color("#444a65"), pygame.Color("#30324d"), pygame.Color("#26203a"), pygame.Color("#23132d"), pygame.Color("#1e0721")],
    [pygame.Color("#ffe377"), pygame.Color("#cdba76"), pygame.Color("#bda576"), pygame.Color("#a48d6a"), pygame.Color("#8b7d62"), pygame.Color("#736554"), pygame.Color("#52484e"), pygame.Color("#292442")],
    [pygame.Color("#ffffff"), pygame.Color("#efe1cc"), pygame.Color("#d8b686"), pygame.Color("#bc8a45"), pygame.Color("#9f6624"), pygame.Color("#784420"), pygame.Color("#532620"), pygame.Color("#3a1220")],
    [pygame.Color("#f2e749"), pygame.Color("#e5be22"), pygame.Color("#d97e16"), pygame.Color("#bf481d"), pygame.Color("#992817"), pygame.Color("#732017"), pygame.Color("#4d130f"), pygame.Color("#330d10")],
    
    # [pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color(""), pygame.Color("")],
]

def palette_swap(surf, old_c, new_c):
    img_copy = pygame.Surface((32,32))
    img_copy.fill(new_c)
    surf.set_colorkey(old_c)
    img_copy.blit(surf, (0, 0))
    return img_copy

def generate_biome_graphics(list, file, img):
    graphics = list
    for bid, biome in enumerate(biome_list):
        img_copy = img
        for cid, color in enumerate(base_pallete): 
            img_copy = palette_swap(img_copy, base_pallete[cid], color_palletes[bid][cid])
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