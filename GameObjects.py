import math
import pygame
from GameSetting import *
import SpriteBase

vec = pygame.math.Vector2

class Obstacle(SpriteBase.GameSprite):

    def __init__(self, x, y, width, height):
        super().__init__((x,y))
        self.map_x = x
        self.map_y = y
        self.rect = pygame.Rect(x, y, width, height)
        # used for debug
        self.image = pygame.Surface((math.floor(width), math.floor(height)))
        self.image.fill((255, 0, 255))

    def world_shift(self, xdiff):
        self.rect.x += xdiff
    
    def get_map_location(self):
        return (self.map_x,  self.map_y)


class Paper(SpriteBase.GameSprite):

    def __init__(self, start_coord):
        super().__init__(start_coord)
        self.image = pygame.image.load(Game.PAPER_IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.pos.x, self.pos.y)
        self.shouldDraw = True

    def world_shift(self, xdiff):
        self.rect.x += xdiff


class Projectile(SpriteBase.GameSprite):

    def __init__(self, acceleration_x, acceleration_y, start_coord, spriteImage):
        super().__init__(start_coord)
        self.acceleration = vec(acceleration_x, acceleration_y)
        self.velocity = vec(0,0)
        self.position = vec(start_coord)
        self.image = spriteImage
        self.rect = self.image.get_rect()
        self.rect.x = start_coord[0]
        self.rect.y = start_coord[1]
        self.xdiff = 0
        self.shouldDraw = True

    def world_shift(self, xdiff):
        self.rect.x += xdiff
        self.xdiff = xdiff

    def update(self, gravity):
        #print('acc = '+str(self.acceleration) + ' vel = '+str(self.velocity))
        self.velocity += self.acceleration
        self.rect.x += self.velocity.x + .5 * self.acceleration.x
        self.rect.y += self.velocity.y + .5 * self.acceleration.y
        self.acceleration = vec(0, gravity)

class AnimatedBullet(Projectile):
    def __init__(self, acceleration_x, acceleration_y, start_coord, spriteSheet, sprite_width, sprite_height, sprite_length):
        pygame.sprite.Sprite.__init__(self)
        self.collision_rect = None
        self.acceleration = vec(acceleration_x, acceleration_y)
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.last_frame = 0
        self.last_update = 0
        self.current_frame = 0
        self.UPDATE_FRAME_ON = 150
        self.velocity = vec(0,0)
        self.position = vec(start_coord)
        self.sprite_length = sprite_length
        self.spriteSheet = spriteSheet
        self.frames = self.load_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = start_coord[0]
        self.rect.y = start_coord[1]

    def load_frames(self):
        frames = []
        for I in range(self.sprite_length):
            frames.append(self.spriteSheet.get_image_row_column(self.sprite_width,self.sprite_height,I,0))
        return frames

    def animate(self):
        now = pygame.time.get_ticks()
        if (now - self.last_frame >= self.UPDATE_FRAME_ON):
            self.last_frame = now
            self.current_frame += 1
            if self.current_frame >= self.sprite_length:
                self.current_frame = 0
            self.image = self.frames[self.current_frame]

    def update(self, gravity):
        self.animate()
        super().update(gravity)


class NerfGun(SpriteBase.GameSprite):

    def __init__(self, start_x, start_y, image_path, x_speed, y_speed, ammo):
        super().__init__((start_x, start_y))
        self.image = pygame.image.load(image_path).convert()
        self.image.set_colorkey(Game.COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rect.move_ip(start_x, start_y)
        self.x_shoot_speed = x_speed
        self.y_shoot_speed = y_speed
        self.ammo_amount = ammo
        self.shouldDraw = True
    
    def world_shift(self,xdiff):
        self.rect.x += xdiff
    
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
        NerfGun.__init__(self, start_x, start_y, Game.NERF_PISTOL_IMAGE,\
         Game.NERF_PISTOL_SPEED, Game.NERF_PISTOL_ARC, Game.NERF_PISTOL_START_AMMO)


class NerfRifle(NerfGun):

     def __init__(self, start_x, start_y):
        NerfGun.__init__(self, start_x, start_y, Game.NERF_RIFLE_IMAGE,
                          Game.NERF_RIFLE_SPEED, Game.NERF_RIFLE_ARC, Game.NERF_RIFLE_START_AMMO)
         
