import pygame
import GameSetting
import math
vec = pygame.math.Vector2

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, start_coord):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = vec(start_coord)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.shouldDraw = False

    def is_should_draw(self):
        return self.shouldDraw

    def sprite_on_screen(self, x_max, y_max):
        if self.pos.x >= 0 and self.pos.x <= x_max and self.pos.y >= 0 and self.pos.y <= y_max:
            self.shouldDraw = True
            return True
        else:
            self.shouldDraw = False
            return False

    def get_acceleration(self):
        return self.acc
    
    def set_acceleration(self, x_accel, y_accel):
        self.acc = vec(x_accel, y_accel)

    def get_velocity(self):
        return self.vel

    def set_velocity(self, x_vel, y_vel):
        self.vel = vec(x_vel, y_vel)

    def get_position(self):
        return self.pos

    def set_position(self, x_pos, y_pos):
        self.pos = vec(x_pos, y_pos)

    def update_position(self, gravity):
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

class Spritesheet:

    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):

        image = pygame.Surface((width, height))
        image.set_colorkey(GameSetting.Game.COLOR_KEY)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

    def get_image_row_column(self, width, height, column, row):
        x = width * column
        y = height * row
        return self.get_image(x, y, width, height)

class OnScreenGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)

    def update(self, screen_width, screen_height, friction, gravity, player_pos):

        for sprite in self.sprites():
            if sprite.sprite_on_screen(screen_width, screen_height):
                sprite.update(friction,gravity,player_pos)

    def draw(self, surface):
        for sprite in self.sprites():
            if sprite.is_should_draw():
                surface.blit(sprite.image, sprite.rect)

class BulletBaseGroup(OnScreenGroup):
    def __init__(self):
        super().__init__()

    def update(self,gravity, map_width, map_height):
        for sprite in self.sprites():
            if sprite.rect.x < 0 or sprite.rect.y < 0 or \
                sprite.rect.x > map_width or sprite.rect.y > map_height:
                sprite.kill()
            else:
                sprite.update(gravity)

    def draw(self, surface):
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect)