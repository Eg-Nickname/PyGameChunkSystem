import pygame
import os
FILERDIR = os.path.dirname(os.path.abspath(__file__))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x = None, pos_y = None):
        super().__init__()
        # Position
        self.position_x = pos_x or 0
        self.position_y = pos_y or 0

        # Velocity
        self.velocity_x = 0
        self.velocity_x_increse = 40
        self.max_x_velocity = 280

        self.velocity_y = 0
        self.velocity_y_increse = 40
        self.max_y_velocity = 280
        

        # Sprite
        self.sprites = []
        self.image = pygame.transform.scale(pygame.image.load("cat.png"),(32,32))

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position_x, self.position_y]
