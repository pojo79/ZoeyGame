import pygame
vec = pygame.math.Vector2
import math

class PrincessSprite(pygame.sprite.Sprite):

    def __init__(self, start_coord):
        pygame.sprite.Sprite.__init__(self)
        self.MOVE_SPEED = 3.5
        self.space_pushed = False
        self.image = pygame.image.load("./assets/art/zoeyPlaceHolder.png")
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-20, 0)
        self.vel = vec(0, 0)
        self.pos = vec(start_coord[0], start_coord[1])
        self.acc = vec(0,0)
        self.onGround = False
        self.rect.move_ip(self.pos)
        
    def draw(self, display):
        display.blit(self.image, self.rect)

    def jump(self):
        self.onGround = False
        self.acc.y = -15
        print('jump')

    def update(self, friction, gravity):
        #add gravity variable
        print("vel = "+str(self.vel) + "acc = "+str(self.acc) + "pos = "+str(self.pos))
        self.acc = vec(0, gravity)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -self.MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.acc.x = self.MOVE_SPEED
        if keys[pygame.K_SPACE]:
            if self.onGround  and not self.space_pushed:
                self.space_pushed = True
                self.jump()
        else:
            self.space_pushed = False

        self.acc.x += self.vel.x * friction
        if math.fabs(self.acc.x) <= .05:
            self.acc.x = 0
            self.vel.x = 0
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y > 800:
            self.pos = vec(30,150)
        
    def set_position(self, object):
        y_vel = math.ceil(self.vel.y + .5 * self.acc.y)
        #print("object top = " + str(object.rect.top)+' self bottom = ' +str(self.rect.bottom) + " y_vel = "+str(y_vel))
        if self.vel.y > 0 and object.rect.top >= self.rect.bottom - y_vel:
            self.vel.y =0
            if self.rect.bottom - 1 == object.rect.top:
                self.onGround = True
            self.pos.y = object.rect.top-self.rect.height

    def kill_enemy(self, enemy, gravity):
        y_vel = self.vel.y + .5 * self.acc.y
        if self.vel.y - gravity > 0 and enemy.rect.top >= self.rect.bottom - y_vel:
            #self.pos.y = enemy.rect.top
            #self.vel.y = 0
            self.vel.y += -25
            return True
        else:
            return False

class obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)
        #used for debug
        self.image = pygame.Surface((math.floor(width), math.floor(height)))
        self.image.fill((255,0,255))

class snake(pygame.sprite.Sprite):
    def __init__(self, x, y, travel = 40):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/art/yellow_snake.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_travel = 0
        self.x_max_travel = travel
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.acc = vec(2,0)

    def update(self, friction, gravity):
        if math.fabs(self.x_travel) < self.x_max_travel:
            self.rect.x += self.acc.x
            self.x_travel += self.acc.x
        else:
            self.x_travel = 0
            if self.acc.x > 0:
                self.acc.x = -2
            else:
                self.acc.x = 2        

class eye(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/art/shining_eye.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y