import math
import pygame
from GameSetting import *

vec = pygame.math.Vector2

class Obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        # used for debug
        self.image = pygame.Surface((math.floor(width), math.floor(height)))
        self.image.fill((255, 0, 255))

class Projectile(pygame.sprite.Sprite):

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

class NerfGun(pygame.sprite.Sprite):

    def __init__(self, start_x, start_y, image_path, x_speed, y_speed, ammo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.move_ip(start_x, start_y)
        self.x_shoot_speed = x_speed
        self.y_shoot_speed = y_speed
        self.ammo_amount = ammo
    
    def set_ammo_amount(self, amount):
        self.ammo_amount = amount

    def get_ammo_amount(self):
        return self.ammo_amount

    def set_x_shoot_speed(self, x_speed):
        self.x_speed = x_speed
    
    def get_x_shoot_speed(self):
        return self.x_shoot_speed

    def set_y_shoot_speed(self, y_speed):
        self.y_speed = y_speed
    
    def get_y_shoot_speed(self):
        return self.y_shoot_speed

class NerfPistol(NerfGun):
    def __init__(self, start_x, start_y):
        NerfGun.__init__(self, start_x, start_y, "./assets/art/nerf_pistol.png",\
         Game.NERF_PISTOL_SPEED, Game.NERF_PISTOL_ARC, Game.NERF_PISTOL_START_AMMO)


class NerfRifle(NerfGun):

     def __init__(self, start_x, start_y):
        NerfGun.__init__(self, start_x, start_y, "./assets/art/nerf_pistol.png",
                          Game.NERF_RIFLE_SPEED, Game.NERF_RIFLE_ARC, Game.NERF_RIFLE_START_AMMO)
         
