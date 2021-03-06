import pygame
class Particle():
    def __init__(self, pos_x, pos_y, rotation, creation_time):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rotation = rotation
        self.life_span = 240
        self.creation_time = creation_time
        
        self.image = pygame.image.load("./static_graphics/particle.png")

    def update_pos(self):
        self.pos_x += self.rotation[0] * 2
        self.pos_y += self.rotation[1] * 2