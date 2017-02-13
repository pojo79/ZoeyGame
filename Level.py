import pygame
import os
import pytmx
import SpriteBase
from GameSetting import Game

class Level(object):

    def __init__(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tm = pytmx.load_pygame(dir_path + filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.level_friction = float(tm.properties['friction'])
        self.level_gravity = float(tm.properties['gravity'])
        self.level_background = pygame.image.load("./assets/level/golf_background.png")
        self.level_bmg = tm.properties['bgm']
        self.spawn = (0, 0)
        self.ground = SpriteBase.OnScreenGroup()
        self.enemies = SpriteBase.OnScreenGroup()
        self.powerups = SpriteBase.OnScreenGroup()
        self.ammo = SpriteBase.OnScreenGroup()
        self.checkpoints = SpriteBase.OnScreenGroup()
        self.goal = 0

    def render(self, surface):
        getTile = self.tmxdata.get_tile_image
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    surface.blit(image, (x * self.tmxdata.tilewidth,
                                         y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        temp_surface.fill(Game.COLOR_KEY)  # blue background
        temp_surface.set_colorkey(Game.COLOR_KEY)
        self.render(temp_surface)
        return temp_surface
