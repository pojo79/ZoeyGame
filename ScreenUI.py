import pygame
import GameSetting
from SpriteBase import Spritesheet

class ScreenOverlay(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(GameSetting.Game.OVERLAY_IMAGE).convert_alpha()
        self.numbers = Spritesheet(GameSetting.Game.NUMBERS_SPRITE_SHEET)
        self.rect = self.image.get_rect()

    def get_number_image(self, number):
        return self.numbers.get_image_row_column(GameSetting.Game.NUMBERS_SPRITE_WIDTH, GameSetting.Game.NUMBERS_SPRITE_HEIGHT,number,0)

    def draw(self, screen, lives, ammo):
        screen.blit(self.image, self.image.get_rect())
        screen.blit(self.get_number_image(lives),(GameSetting.Game.OVERLAY_LIVES_POS, self.image.get_rect().y))
        screen.blit(self.get_number_image(ammo),(GameSetting.Game.OVERLAY_AMMO_POS, self.image.get_rect().y))
        