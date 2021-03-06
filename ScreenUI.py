import pygame
import GameSetting
from SpriteBase import Spritesheet

class ScreenOverlay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(GameSetting.Game.OVERLAY_IMAGE).convert_alpha()
        self.number_sprite_sheet = Spritesheet(GameSetting.Game.NUMBERS_SPRITE_SHEET)
        self.rect = self.image.get_rect()
        self.numbers = self.get_number_images()

    def get_number_images(self):
        nums = []
        for num in range(10):
            nums.append(self.number_sprite_sheet.get_image_row_column(GameSetting.Game.NUMBERS_SPRITE_WIDTH, GameSetting.Game.NUMBERS_SPRITE_HEIGHT,num,0))
        return nums
    
    def draw_numbers(self,screen, number, start_x, start_y, width):
        num_string = str(number)
        position = 0
        for num in num_string:
            screen.blit(self.numbers[int(num_string[position])],(start_x+position*width, start_y))
            position += 1
            

    def draw(self, screen, lives, ammo, points, homework):
        screen.blit(self.image, self.image.get_rect())
        self.draw_numbers(screen,lives,GameSetting.Game.OVERLAY_LIVES_POS, self.image.get_rect().y, GameSetting.Game.NUMBERS_SPRITE_WIDTH)
        self.draw_numbers(screen,ammo,GameSetting.Game.OVERLAY_AMMO_POS, self.image.get_rect().y, GameSetting.Game.NUMBERS_SPRITE_WIDTH)
        self.draw_numbers(screen,homework,GameSetting.Game.OVERLAY_HOMEWORK_POS, self.image.get_rect().y, GameSetting.Game.NUMBERS_SPRITE_WIDTH)
        self.draw_numbers(screen,points,GameSetting.Game.OVERLAY_SCORE_POS, self.image.get_rect().y, GameSetting.Game.NUMBERS_SPRITE_WIDTH)
        