import ZoeyGameEventHandler
from ZoeyGameSprites import *
import pygame
import pytmx
import os

#initiate pygame
pygame.init()
game_display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Princess Zoey's Adventure")

class Level(object):
            
    def __init__(self, filename, friction):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tm = pytmx.load_pygame(dir_path+filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.level_friction = friction

    def render(self, surface):
        getTile = self.tmxdata.get_tile_image
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    surface.blit(image, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    
    def load_objects(self):
        for tile_object in self.tmxdata.objects:
            print(tile_object)
    
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        temp_surface.fill((0,100,250)) #blue background
        self.render(temp_surface)
        return temp_surface

class ZoeyGame(object):

    def __init__(self, game_display):
        self.fps_clock = pygame.time.Clock()
        self.gameOver = False
        self.world_x = 0
        self.rightBounds = 0
        self.leftBounds = 0
        self.currentHandler = ZoeyGameEventHandler.GamePlayEventHandler()
        self.game_display = game_display
        self.group = pygame.sprite.Group()
        self.player = PrincessSprite()
        self.ground = pygame.sprite.Group()
        self.loadLevel()
        self.gameLoop()


    def loadLevel(self):
        self.level = Level("/assets/level/test_level.tmx", -.35)
        self.tileSurface = self.level.make_map()
        for tile_object in self.level.tmxdata.objects:
            if tile_object.name == "ground":
                self.ground.add(obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
        self.rightBounds = 450
        self.leftBounds = self.rightBounds - 100

    def endGame(self, bool_endGame):
        self.gameOver = endGame   

    def shiftAll(self):
        x_diff = 0
        if self.player.get_position()[0] > self.rightBounds:
            if self.world_x <= 0 - self.tileSurface.get_width() + game_display.get_width():
                self.world_x = 0- self.tileSurface.get_width() + game_display.get_width()
            else:
                self.world_x += self.rightBounds - self.player.rect.x
                self.player.rect.x = self.rightBounds
        if self.player.get_position()[0] <= self.leftBounds:
            if self.world_x >= 0:
                self.world_x = 0
            else:
                self.world_x += self.leftBounds - self.player.rect.x
                self.player.rect.x = self.leftBounds

    def gameLoop(self):
        while not self.gameOver:

            #self. shiftAll()
            
            self.handleEvent(pygame.event)
            self.game_display.blit(self.tileSurface, (self.world_x, 0))
            self.player.update(self.level.level_friction, 0)

            collide = pygame.sprite.spritecollide(self.player, self.ground, False)
            if collide:
                self.player.set_position(collide[0])

            self.player.draw(self.game_display)
            pygame.display.update()
            if(self.currentHandler.isEndGame()):
                self.gameOver = True
            self.fps_clock.tick(10)
        
    def handleEvent(self, pygame_event):    
        for event in pygame_event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True

ZoeyGame(game_display)