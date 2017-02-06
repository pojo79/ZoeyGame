import pygame
import SpriteBase
import math

vec = pygame.math.Vector2

class snake(pygame.sprite.Sprite):

    def __init__(self, x, y, travel=40):
        pygame.sprite.Sprite.__init__(self)
        self.UPDATE_FRAME_ON = 150
        self.current_frame = 0
        self.last_frame = 0
        self.TRAVEL_SPEED = 1
        self.sprite_width = 52
        self.sprite_height = 87
        self.spritesheet = SpriteBase.Spritesheet("./assets/art/zombie_sprite_sheet.png")
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