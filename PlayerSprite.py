import pygame
import math
from GameSetting import *
from GameObjects import Projectile
import SpriteBase

vec = pygame.math.Vector2

class PlayerSprite(SpriteBase.GameSprite):
    UPDATE_FRAME_ON = 100

    def __init__(self, start_coord):
        super().__init__(start_coord)
        self.move_speed = Move.PLAYER_MOVE
        self.space_pushed = False
        self.is_dead = False
        self.nerf_dart_image_right = pygame.image.load(Game.NERF_DART_IMAGE).convert()
        self.nerf_dart_image_left = pygame.transform.flip(self.nerf_dart_image_right, True, False)
        self.sprite_sheet = SpriteBase.Spritesheet(Player.ZOEY_SPRITE_SHEET)
        self.load_player_sprites()
        self.image_set = self.stop_image_left
        self.image = self.image_set[0]
        self.rect = self.image.get_rect()
        self.direction = Move.STOP
        self.facing = Move.RIGHT
        self.jump_buffer = None
        self.duck = False
        self.run = False
        self.onGround = False
        self.current_frame = 0
        self.last_frame = 0
        self.gun = None
        self.rect.move_ip(self.pos)
        self.collision_rect = self.rect.inflate(Player.PLAYER_X_SHRINK, Player.PLAYER_Y_SHRINK)
        self.jump_sound = pygame.mixer.Sound(Player.PLAYER_JUMP_SOUND)
        self.shoot_sound = pygame.mixer.Sound(Player.PLAYER_SHOOT_SOUND)
        self.shoot_sound.set_volume(100)
        self.bullets = SpriteBase.BulletBaseGroup()

    def load_player_sprites(self):
        self.frames_right = [self.sprite_sheet.get_image_row_column(Player.PLAYER_SPRITE_WIDTH, Player.PLAYER_SPRITE_HEIGHT, 0, 0),
                                    self.sprite_sheet.get_image_row_column(Player.PLAYER_SPRITE_WIDTH, Player.PLAYER_SPRITE_HEIGHT, 1, 0),
                                    self.sprite_sheet.get_image_row_column(Player.PLAYER_SPRITE_WIDTH, Player.PLAYER_SPRITE_HEIGHT, 2, 0)]
        self.stop_image_right = [self.sprite_sheet.get_image_row_column(Player.PLAYER_SPRITE_WIDTH, Player.PLAYER_SPRITE_HEIGHT, 3, 0)]
        self.stop_image_left = [pygame.transform.flip(self.stop_image_right[0], True, False)]
        self.image_jump_right = self.sprite_sheet.get_image_row_column(Player.PLAYER_SPRITE_WIDTH, Player.PLAYER_SPRITE_HEIGHT, 4, 0)
        self.image_jump_left = pygame.transform.flip(self.image_jump_right, True, False)
        self.frames_left = []
        for image in self.frames_right:
            self.frames_left.append(pygame.transform.flip(image, True, False))

    def get_bullets(self):
        return self.bullets

    def draw(self, display):
        display.blit(self.image, self.rect)
        
        if Game.DEBUG:
            collisiont_rect_image = pygame.Surface((self.collision_rect.width, self.collision_rect.height))
            collisiont_rect_image.fill((120,230,20))
            display.blit(collisiont_rect_image, self.collision_rect)

    def move(self, direction, stop_movement=False):
        if stop_movement and self.direction == direction:
            self.direction = Move.STOP
            if direction == Move.LEFT:
                self.image_set = self.stop_image_left
            else:
                self.image_set = self.stop_image_right
        elif not stop_movement:
            if not direction == self.direction:
                self.current_frame = 0
            self.direction = direction
            self.facing = direction
    
    def set_duck(self, duck):
        self.duck = duck

    def set_run(self, run):
        self.run = run
        
    def jump(self):
        if self.onGround and not self.jump_buffer == None:
            if pygame.time.get_ticks() - self.jump_buffer <= Control.JUMP_FOGIVENESS:
                self.jump_sound.play()
                self.onGround = False
                self.acc.y = Move.PLAYER_JUMP
                self.jump_buffer = None
                if self.facing == Move.LEFT:
                    self.image = self.image_jump_left
                else:
                    self.image = self.image_jump_right

    """ add a jumper to the buffer with the current time of button press
    This will make jumping more responsive since you can press button slightly before hitting the ground and still
    have jump register """
    def add_jump_to_buffer(self):
        self.jump_buffer = pygame.time.get_ticks()

    def set_move_speed(self):
        if self.move_speed == Move.PLAYER_MOVE:
            if self.run and self.onGround:
                self.move_speed = Move.PLAYER_RUN
        if self.move_speed == Move.PLAYER_RUN:
            if not self.run and self.onGround:
                self.move_speed = Move.PLAYER_MOVE

    def update(self, friction, gravity, floor):
        force = False
        self.set_move_speed()
        if self.direction == Move.LEFT:
            self.acc.x = -self.move_speed
            self.image_set = self.frames_left
        if self.direction == Move.RIGHT:
            self.acc.x = self.move_speed
            self.image_set = self.frames_right
        self.jump()
        
        self.acc.x += self.vel.x * friction
        if math.fabs(self.acc.x) <= Move.ZERO_THRESHOLD and self.onGround and self.direction == Move.STOP:
            self.acc.x = 0
            self.vel.x = 0
        
        self.update_position(gravity)
        #print("vel = "+str(self.vel) + "acc = "+str(self.acc) + "pos = "+str(self.pos))

        if self.pos.y > floor:
            self.is_dead = True
        self.acc = vec(0, gravity)
        
        self.animate(force)
        self.onGround = False

    def animate(self, force):
        now = pygame.time.get_ticks()
        if (now - self.last_frame >= self.UPDATE_FRAME_ON) and self.onGround or (force):
            self.last_frame = now
            self.current_frame += 1
            if self.current_frame >= len(self.image_set):
                self.current_frame = 0
            self.image = self.image_set[self.current_frame]   

    def set_position(self, object):
        y_vel = math.ceil(self.vel.y + .5 * self.acc.y)
        #print("object top = " + str(object.rect.top)+' self bottom = ' +str(self.rect.bottom) + " y_vel = "+str(y_vel))
        if self.vel.y > 0 and object.rect.top >= self.rect.bottom - y_vel:
            self.vel.y = 0
            if self.rect.bottom - 1 == object.rect.top:
                self.onGround = True
            self.pos.y = object.rect.top - self.rect.height

    def kill_enemy(self, enemy, gravity):
        y_vel = math.ceil(self.vel.y + .5 * self.acc.y)
      #  print('enemy top: '+str(enemy.rect.top) + ' self bottom: '+str(self.rect.bottom) + ' yvel = '+str(y_vel)
       # +' vel = '+str(self.vel))
        if self.vel.y - gravity > 0 and enemy.get_collision_rect().top >= self.collision_rect.bottom - y_vel:
            self.vel.y = Move.PLAYER_POP
            return True
        else:
            self.is_dead = True
            return False
    
    def set_gun(self, gun):
        self.gun = gun
    
    def get_ammo(self):
        ammo = 0
        if not self.gun == None:
            ammo = self.gun.get_ammo_amount()
        return ammo

    def shoot(self):
        if not self.gun == None and self.gun.get_ammo_amount() > 0:
            self.gun.set_ammo_amount(self.gun.get_ammo_amount() - 1)
            self.shoot_sound.play()
            if self.facing == Move.LEFT:
                self.bullets.add(Projectile(-self.gun.get_x_shoot_speed(),
                                            self.gun.get_y_shoot_speed(), (self.rect.x-self.nerf_dart_image_left.get_rect().width,self.rect.y+self.rect.height/2), self.nerf_dart_image_left))
            if self.facing == Move.RIGHT:
                self.bullets.add(Projectile(self.gun.get_x_shoot_speed(
                ), self.gun.get_y_shoot_speed(), self.rect.midright, self.nerf_dart_image_right))

    def add_ammo(self, amount):
        if not self.gun == None:
            self.gun.set_ammo_amount(self.gun.get_ammo_amount() + 1)
