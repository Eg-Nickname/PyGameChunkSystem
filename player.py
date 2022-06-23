import pygame
import os
FILERDIR = os.path.dirname(os.path.abspath(__file__))

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x = None, pos_y = None):
        super().__init__()
        # Position
        self.position_x = pos_x or 0
        self.position_y = pos_y or 0
        self.velocity = 2
        self.direction = pygame.math.Vector2()

        self.status = "up"
        
        self.last_attack = 0
        self.attack_delay = 60 # 1s

        # Sprite
        self.sprites = []
        self.image = pygame.transform.scale(pygame.image.load("./static_graphics/cat.png").convert_alpha(),(32,32))

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position_x, self.position_y]
        self.hitbox = self.rect.inflate(-8,-8)

        self.collision_objects = pygame.sprite.Group()


    def movement(self, pressed_keys):
        if pressed_keys[100]:
            self.direction.x = 1
            self.status = 'right'
        elif pressed_keys[97]:    
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

        if pressed_keys[119]:    
            self.direction.y = -1
            self.status = 'up'
        elif pressed_keys[115]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # if self.direction.magnitude() != 0:
        #     self.direction = self.direction.normalize()
            
    
        self.hitbox.x += self.direction.x * self.velocity
        self.collision('horizontal')

        self.hitbox.y += self.direction.y * self.velocity
        self.collision('vertical')
        self.rect.center = self.hitbox.center

        self.position_x = self.rect.topleft[0]
        self.position_y = self.rect.topleft[1]

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.collision_objects:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.collision_objects:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom