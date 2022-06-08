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
        
        self.last_attack = 0
        self.attack_delay = 60 # 1s

        # Sprite
        self.sprites = []
        self.image = pygame.transform.scale(pygame.image.load("./graphics/cat.png"),(32,32))

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position_x, self.position_y]


    def movement(self, pressed_keys):
        if pressed_keys[100]:
            if self.velocity_x < self.max_x_velocity:
                self.velocity_x+=self.velocity_x_increse

        if pressed_keys[97]:	
            if self.velocity_x > -self.max_x_velocity:
                self.velocity_x-=self.velocity_x_increse

        if pressed_keys[119]:	
            if self.velocity_y > -self.max_y_velocity:
                self.velocity_y-=self.velocity_y_increse

        if pressed_keys[115]:
            if self.velocity_y < self.max_x_velocity:
                self.velocity_y+=self.velocity_x_increse

        self.position_x += int(self.velocity_x/100)
        self.position_y += int(self.velocity_y/100)

        if self.velocity_x>0:
            self.velocity_x-=15
        elif self.velocity_x<0:
            self.velocity_x+=15

        if self.velocity_y>0:
            self.velocity_y-=15
        elif self.velocity_y<0:
            self.velocity_y+=15