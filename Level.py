import pygame
import os
import pytmx
import SpriteBase

class Level(object):

    def __init__(self, filename, friction, gravity):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tm = pytmx.load_pygame(dir_path + filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.level_friction = friction
        self.level_gravity = gravity
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
        temp_surface.fill((0, 100, 250))  # blue background
        self.render(temp_surface)
        return temp_surface