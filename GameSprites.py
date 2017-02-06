import math
import pygame
from GameSetting import *

vec = pygame.math.Vector2


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, start_coord):
        pygame.sprite.Sprite.__init__(self)
        self.MOVE_SPEED = 1.75
        self.space_pushed = False
        self.is_dead = False
        self.image_right = pygame.image.load(
            "./assets/art/zoeyPlaceHolder.png")
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.direction = Move.STOP
        self.rect.inflate_ip(-20, 0)
        self.vel = vec(0, 0)
        self.pos = vec(start_coord[0], start_coord[1])
        self.acc = vec(0, 0)
        self.jump_buffer = None
        self.duck = False
        self.run = False
        self.onGround = False
        self.rect.move_ip(self.pos)
        self.jump_sound = pygame.mixer.Sound("./assets/sound/jump.wav")

    def draw(self, display):
        display.blit(self.image, self.rect)

    def move(self, direction, stop_movement=False):
        if stop_movement and self.direction == direction:
            self.direction = Move.STOP
        elif not stop_movement:
            self.direction = direction
    
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
    
    ''' add a jumper to the buffer with the current time of button press
    This will make jumping more responsive since you can press button slightly before hitting the ground and still
    have jump register '''
    def add_jump_to_buffer(self):
        self.jump_buffer = pygame.time.get_ticks()

    def update(self, friction, gravity, floor):
       # print("vel = "+str(self.vel) + "acc = "+str(self.acc) + "pos = "+str(self.pos))
        if self.direction == Move.LEFT:
            if self.run:
                self.acc.x = -Move.PLAYER_RUN
            else:
                self.acc.x = -Move.PLAYER_MOVE
            if not self.onGround and self.vel.x > .05:
                self.acc.x = -Move.PLAYER_MOVE / 2
            self.image = self.image_left
        if self.direction == Move.RIGHT:
            if self.run:
                self.acc.x = Move.PLAYER_RUN
            else:
                self.acc.x = Move.PLAYER_MOVE
            if not self.onGround and self.vel.x < -.05:
                self.acc.x = Move.PLAYER_MOVE / 2
            self.image = self.image_right
        self.jump()
        
        self.acc.x += self.vel.x * friction
        if math.fabs(self.acc.x) <= Move.ZERO_THRESHOLD:
            self.acc.x = 0
            self.vel.x = 0
        
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y > floor:
            self.is_dead = True
        self.acc = vec(0, gravity)
        
        self.onGround = False

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
        if self.vel.y - gravity > 0 and enemy.rect.top >= self.rect.bottom - y_vel:
            self.vel.y = Move.PLAYER_POP
            return True
        else:
            self.is_dead = True
            return False


class obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        # used for debug
        self.image = pygame.Surface((math.floor(width), math.floor(height)))
        self.image.fill((255, 0, 255))


class snake(pygame.sprite.Sprite):

    def __init__(self, x, y, travel=40):
        pygame.sprite.Sprite.__init__(self)
        self.UPDATE_FRAME_ON = 150
        self.current_frame = 0
        self.last_frame = 0
        self.TRAVEL_SPEED = 1
        self.sprite_width = 52
        self.sprite_height = 87
        self.spritesheet = Spritesheet("./assets/art/zombie_sprite_sheet.png")
        self.load_images()
        self.image = self.walking_frames_left[0]
        self.image_set = self.walking_frames_left
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_travel = 0
        self.x_max_travel = travel
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(-self.TRAVEL_SPEED, 0)

    def load_images(self):
        self.walking_frames_left = [self.spritesheet.get_image_row_column(self.sprite_width, self.sprite_height, 2, 0),
                                    self.spritesheet.get_image_row_column(
                                        self.sprite_width, self.sprite_height, 1, 0),
                                    self.spritesheet.get_image_row_column(
                                        self.sprite_width, self.sprite_height, 0, 0),
                                    self.spritesheet.get_image_row_column(
                                        self.sprite_width, self.sprite_height, 2, 0),
                                    self.spritesheet.get_image_row_column(
                                        self.sprite_width, self.sprite_height, 3, 0),
                                    self.spritesheet.get_image_row_column(self.sprite_width, self.sprite_height, 4, 0)]

        self.walking_frames_right = []
        for frame in self.walking_frames_left:
            self.walking_frames_right.append(
                pygame.transform.flip(frame, True, False))

    def update(self, friction, gravity):
        force = False
        if math.fabs(self.x_travel) <= self.x_max_travel:
            self.rect.x += self.acc.x
            self.x_travel += self.acc.x
        else:
            self.x_travel = 0
            if self.acc.x > 0:
                self.acc.x = -self.TRAVEL_SPEED
                self.current_frame = 0
                self.image_set = self.walking_frames_left
                force = True
            else:
                self.acc.x = self.TRAVEL_SPEED
                self.current_frame = 0
                self.image_set = self.walking_frames_right
                force = True
        self.animate(force)

    def animate(self, force):
        now = pygame.time.get_ticks()
        if (now - self.last_frame >= self.UPDATE_FRAME_ON) or (force):
            self.last_frame = now
            self.current_frame += 1
            if self.current_frame >= len(self.walking_frames_left):
                self.current_frame = 0
            self.image = self.image_set[self.current_frame]


class eye(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/art/golfer.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Spritesheet:

    def __init__(self, filename):
        self.COLOR_KEY = (255, 20, 147)  # PINK
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):

        image = pygame.Surface((width, height))
        image.set_colorkey(self.COLOR_KEY)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

    def get_image_row_column(self, width, height, column, row):
        x = width * column
        y = height * row
        #print('loading image at x:'+ str(x) +" y: " +str(y))
        return self.get_image(x, y, width, height)
