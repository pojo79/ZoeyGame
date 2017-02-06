import math
import pygame
from GameSetting import *

vec = pygame.math.Vector2

class obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        # used for debug
        self.image = pygame.Surface((math.floor(width), math.floor(height)))
        self.image.fill((255, 0, 255))

class projectile(pygame.sprite.Sprite):

    def __init__(self, acceleration_x, acceleration_y, start_coord, spriteImage):
        pygame.sprite.Sprite.__init__(self)
        self.acceleration = vec(acceleration_x, acceleration_y)
        self.velocity = vec(0,0)
        self.position = vec(start_coord)
        self.image = spriteImage
        self.rect = self.image.get_rect()
        self.rect.x = start_coord[0]
        self.rect.y = start_coord[1]

    def update(self, gravity, screen_width, screen_height):
        #print('acc = '+str(self.acceleration) + ' vel = '+str(self.velocity))
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x + .5 * self.acceleration.x
        self.rect.y += self.velocity.y + .5 * self.acceleration.y
        self.acceleration = vec(0, gravity)

        if self.position.x < 0 or self.position.y < 0 or \
            self.position.x > screen_width or self.position.y > screen_height:
            self.kill()

class nerf_pistol(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/art/nerf_pistol.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(start_x, start_y)
