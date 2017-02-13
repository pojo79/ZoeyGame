import pygame
import math
import GameSetting

class ScrollingBackground(object):
    SCROLL_RATE = 3

    def __init__(self, background, display_width, display_height):
        self.background = background
        self.scrolling_bg = background
        self.display_width = display_width
        self.display_height = display_height
        self.doubled = False
        self.bg_length = background.get_rect().width
        self.current_x = 0
        self.create_scrolling_background()

    def create_scrolling_background(self):
        self.scrolling_bg = pygame.Surface((self.bg_length*2, self.display_height))
        self.scrolling_bg.blit(self.background, (0,0))
        self.scrolling_bg.blit(self.background, (self.bg_length, 0))

    def draw(self, display):
        draw_rect = self.scrolling_bg.get_rect()
        draw_rect.x = math.fabs(self.current_x)
        display.blit(self.scrolling_bg, (0, 0), (draw_rect))

    def update(self, world_x):
        self.current_x += world_x / self.SCROLL_RATE
        if math.fabs(self.current_x) + GameSetting.Game.RIGHT_BOUNDS > self.bg_length+GameSetting.Game.RIGHT_BOUNDS:
            self.current_x = 0

            

