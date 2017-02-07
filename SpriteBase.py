import pygame
import GameSetting

vec = pygame.math.Vector2

class GameSprite(pygame.sprite.Sprite):

    def __init__(self, start_coord):
        pygame.sprite.Sprite.__init__(self)
        
        self.pos = vec(start_coord)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def get_acceleration(self):
        return acc
    
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