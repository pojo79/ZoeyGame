import pygame
import SpriteBase
import math
from GameSetting import *
from GameObjects import *

vec = pygame.math.Vector2


class EnemyBase(SpriteBase.GameSprite):
    def __init__(self, start_coord):
        super().__init__(start_coord)
        self.bullets = None

    def get_bullets(self):
        return self.bullets

class Zombie(EnemyBase):

    def __init__(self, x, y, travel=40):
        super().__init__((x, y))
        self.UPDATE_FRAME_ON = 150
        self.current_frame = 0
        self.last_frame = 0
        self.spritesheet = SpriteBase.Spritesheet(Enemy.ZOMBIE_SPRITE_SHEET)
        self.load_images()
        self.image = self.walking_frames_left[0]
        self.image_set = self.walking_frames_left
        self.rect = self.image.get_rect()
        self.x_travel = 10000
        self.x_max_travel = travel
        self.facing = Move.RIGHT

    def world_shift(self, xdiff):
        self.pos.x += xdiff

    def load_images(self):
        self.walking_frames_left = [self.spritesheet.get_image_row_column(Enemy.ZOMBIE_SPRITE_WIDTH, Enemy.ZOMBIE_SPRITE_HEIGHT, 2, 0),
                                    self.spritesheet.get_image_row_column(
                                        Enemy.ZOMBIE_SPRITE_WIDTH, Enemy.ZOMBIE_SPRITE_HEIGHT, 1, 0),
                                    self.spritesheet.get_image_row_column(
                                        Enemy.ZOMBIE_SPRITE_WIDTH, Enemy.ZOMBIE_SPRITE_HEIGHT, 0, 0),
                                    self.spritesheet.get_image_row_column(
                                        Enemy.ZOMBIE_SPRITE_WIDTH, Enemy.ZOMBIE_SPRITE_HEIGHT, 2, 0),
                                    self.spritesheet.get_image_row_column(
            Enemy.ZOMBIE_SPRITE_WIDTH, Enemy.ZOMBIE_SPRITE_HEIGHT, 3, 0),
            self.spritesheet.get_image_row_column(Enemy.ZOMBIE_SPRITE_WIDTH, Enemy.ZOMBIE_SPRITE_HEIGHT, 4, 0)]

        self.walking_frames_right = []
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(
                pygame.transform.flip(frame, True, False))

    def update(self, friction, gravity, player_pos):
        force = False
        if math.fabs(self.x_travel) <= self.x_max_travel:
            self.x_travel += self.vel.x
            if self.facing == Move.LEFT:
                self.acc.x = -Enemy.ZOMBIE_WALK_SPEED
            else:
                self.acc.x = Enemy.ZOMBIE_WALK_SPEED
        else:
            self.x_travel = 0
            if self.facing == Move.RIGHT:
                self.acc.x = -Enemy.ZOMBIE_WALK_SPEED
                self.current_frame = 0
                self.image_set = self.walking_frames_left
                force = True
                self.facing = Move.LEFT
            else:
                self.acc.x = Enemy.ZOMBIE_WALK_SPEED
                self.current_frame = 0
                self.image_set = self.walking_frames_right
                force = True
                self.facing = Move.RIGHT
        self.acc.x += self.vel.x * friction
        self.update_position(gravity)

        self.animate(force)
        self.acc = vec(0, 0)

    def animate(self, force):
        now = pygame.time.get_ticks()
        if (now - self.last_frame >= self.UPDATE_FRAME_ON) or (force):
            self.last_frame = now
            self.current_frame += 1
            if self.current_frame >= len(self.walking_frames_left):
                self.current_frame = 0
            self.image = self.image_set[self.current_frame]


class Golfer(EnemyBase):

    def __init__(self, x, y):
        super().__init__((x,y))
        self.image = pygame.image.load(Enemy.GOLFER_SPRITE_SHEET).convert_alpha()
        self.bullet_image = pygame.image.load(Enemy.GOLFER_BULLET_SPRITE).convert()
        self.bullet_image.set_colorkey(Game.COLOR_KEY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bullets = SpriteBase.BulletBaseGroup()
        self.bullet_last_shot = 0

    def world_shift(self, xdiff):
        self.pos.x += xdiff    

    def update(self, friction, gravity, player_pos):
        ticks = pygame.time.get_ticks()
        self.update_position(gravity)
        if ticks - self.bullet_last_shot > Enemy.GOLFER_SHOOT_RATE:
            self.bullet_last_shot = ticks
            if self.pos.x < player_pos.x:
                self.bullets.add(Projectile(Enemy.GOLFER_BULLET_SPEED, Enemy.GOLFER_BULLET_ARC, self.rect.midbottom, self.bullet_image))
            if self.pos.x > player_pos.x:
                self.bullets.add(Projectile(-Enemy.GOLFER_BULLET_SPEED, Enemy.GOLFER_BULLET_ARC, self.rect.midbottom, self.bullet_image))

class Skeleton(EnemyBase):
    
    def __init__(self, x, y):
        super().__init__((x,y))
        self.image = pygame.image.load(Enemy.SKELETON_SPRITE_SHEET).convert_alpha()
        self.bullet_image = SpriteBase.Spritesheet(Enemy.SKELETON_BULLET_SPRITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.bullets = SpriteBase.BulletBaseGroup()
        self.bullet_last_shot = 0

    def world_shift(self, xdiff):
        self.pos.x += xdiff    

    def update(self, friction, gravity, player_pos):
        ticks = pygame.time.get_ticks()
        self.update_position(gravity)
        if ticks - self.bullet_last_shot > Enemy.SKELETON_SHOOT_RATE:
            self.bullet_last_shot = ticks
            if self.pos.x < player_pos.x:
                self.bullets.add(AnimatedBullet(Enemy.SKELETON_BULLET_SPEED, Enemy.SKELETON_BULLET_ARC, self.rect.topleft, self.bullet_image,
                Enemy.SKELETON_SPRITE_BULLET_WIDTH, Enemy.SKELETON_SPRITE_BULLET_HEIGHT, Enemy.SKELETON_SPRITE_BULLET_LENGTH))
            if self.pos.x > player_pos.x:
                self.bullets.add(AnimatedBullet(-Enemy.SKELETON_BULLET_SPEED, Enemy.SKELETON_BULLET_ARC, self.rect.topright, self.bullet_image,
                Enemy.SKELETON_SPRITE_BULLET_WIDTH, Enemy.SKELETON_SPRITE_BULLET_HEIGHT, Enemy.SKELETON_SPRITE_BULLET_LENGTH))
