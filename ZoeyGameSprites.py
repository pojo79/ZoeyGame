import pygame
vec = pygame.math.Vector2

class PrincessSprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.MOVE_SPEED = 2
        self.image = pygame.image.load("./assets/art/zoeyPlaceHolder.png")
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(-20, 0)
        self.vel = vec(0, 0)
        self.pos = vec(30, 150)
        self.acc = vec(0,0)
        self.onGround = False
        self.rect.move_ip(self.pos)
        

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def draw(self, display):
        display.blit(self.image, self.rect)

    def jump(self):
        self.onGround = False
        self.acc.y = -15

    def update(self, friction, gravity):
        self.acc = vec(0,0.8)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -self.MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            self.acc.x = self.MOVE_SPEED
        if keys[pygame.K_SPACE]:
            if self.onGround == True:
                self.jump()

        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc

        print(str(self.vel + .5 * self.acc))

        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        if self.pos.y > 800:
            self.pos = vec(30,150)
        
        #self.update_xaxis()
        #self.update_yaxis()

    def set_position(self, object):
        if self.vel.y > 0 and object.rect.top >= self.rect.bottom-30:
            self.onGround = True
            self.pos.y = object.rect.top-self.rect.height
            self.vel.y =0

class obstacle(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x,y,width,height)