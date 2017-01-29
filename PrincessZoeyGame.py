import ZoeyGameEventHandler
import pygame
import pytmx
import os


class Level(object):
            
    def __init__(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tm = pytmx.load_pygame(dir_path+filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        print(tm)

    def render(self, surface):
        getTile = self.tmxdata.get_tile_image
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    #tile = getTile(x, y, layer)
                    #if tile:
                    surface.blit(image, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        temp_surface.fill((0,100,250))
        self.render(temp_surface)
        return temp_surface

#initiate pygame
pygame.init()
game_display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Princess Zoey's Adventure")
fps_clock = pygame.time.Clock()
level = Level("/assets/level/test_level.tmx")
tileSurface = level.make_map()


gameOver = False

currentHandler = ZoeyGameEventHandler.GamePlayEventHandler()

def endGame(bool_endGame):
    gameOver = endGame


while not gameOver:
    game_display.fill((0, 100, 200))
    game_display.blit(tileSurface, (0, 0))
    pygame.display.update()
    currentHandler.handleEvent(pygame.event)
    if(currentHandler.isEndGame()):
        gameOver = True
