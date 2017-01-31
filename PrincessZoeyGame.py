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
            
    def __init__(self, filename, friction, gravity):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tm = pytmx.load_pygame(dir_path+filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.level_friction = friction
        self.level_gravity = gravity
        self.spawn = (0,0)
        self.ground = pygame.sprite.Group()
        self.goal = 0

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
        self.allGameObjects = pygame.sprite.Group()
        self.loadLevel()
        self.game_display = game_display
        self.player = PrincessSprite(self.level.spawn)
        self.gameLoop()


    def loadLevel(self):
        self.level = Level("/assets/level/test_level.tmx", -.35, 0.8)
        self.tileSurface = self.level.make_map()
        
        for tile_object in self.level.tmxdata.objects:
            if tile_object.name == "ground":
                self.level.ground.add(obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "player_spawn":
                self.level.spawn = (tile_object.x, tile_object.y)
            if tile_object.name == "goal":
                self.level.goal = obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.allGameObjects.add(self.level.goal)

            self.allGameObjects.add(self.level.ground)
        
        self.rightBounds = 450
        self.leftBounds = self.rightBounds - 100

    def shiftAll(self):
        if self.player.pos.x > self.rightBounds:
            if self.world_x <= 0 - self.tileSurface.get_width() + game_display.get_width():
                self.world_x = 0- self.tileSurface.get_width() + game_display.get_width()
                if(self.player.rect.right > game_display.get_width() ):
                    self.player.pos.x = game_display.get_width() - self.player.rect.width
            else:
                self.world_x += self.rightBounds - self.player.pos.x
                self.player.pos.x = self.rightBounds
                for item in self.allGameObjects:
                    item.rect.x = item.original_x + self.world_x
                    
        if self.player.pos.x <= self.leftBounds:
            if self.world_x >= 0:
                self.world_x = 0
                if self.player.pos.x < 0:
                    self.player.pos.x = 0
            else:
                self.world_x += self.leftBounds - self.player.pos.x
                self.player.pos.x = self.leftBounds
                for item in self.allGameObjects:
                    item.rect.x = item.original_x + self.world_x

    def gameLoop(self):
        while not self.gameOver:

            self. shiftAll()
            
            self.handleEvent(pygame.event)
            self.game_display.blit(self.tileSurface, (self.world_x, 0))
            self.player.update(self.level.level_friction, 0)

            if pygame.sprite.collide_rect(self.level.goal, self.player):
                print("yea, you win")
                self.gameOver = True

            collide = pygame.sprite.spritecollide(self.player, self.level.ground, False)
            if collide:
                self.player.set_position(collide[0])

            #draw platform hitbox
            #self.ground.draw(self.game_display)
            self.allGameObjects.draw(self.game_display)

            self.player.draw(self.game_display)
            pygame.display.update()
            self.fps_clock.tick(60)
        
    def handleEvent(self, pygame_event):    
        for event in pygame_event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True

ZoeyGame(game_display)