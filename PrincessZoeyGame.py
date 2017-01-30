import ZoeyGameEventHandler
import ZoeyGameSprites
import pygame
import pytmx
import os

#initiate pygame
pygame.init()
game_display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Princess Zoey's Adventure")

class Level(object):
            
    def __init__(self, filename):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tm = pytmx.load_pygame(dir_path+filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        getTile = self.tmxdata.get_tile_image
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    surface.blit(image, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        temp_surface.fill((0,100,250)) #blue background
        self.render(temp_surface)
        return temp_surface

class ZoeyGame(object):

    def __init__(self, game_display):
        self.fps_clock = pygame.time.Clock()
        self.gameOver = False
        self.x = 0
        self.xmove = 0
        self.currentHandler = ZoeyGameEventHandler.GamePlayEventHandler()
        self.game_display = game_display
        self.group = pygame.sprite.Group()
        self.player = ZoeyGameSprites.PrincessSprite()
        self.loadLevel()
        self.gameLoop()

    def loadLevel(self):
        level = Level("/assets/level/test_level.tmx")
        self.tileSurface = level.make_map()  

    def endGame(self, bool_endGame):
        self.gameOver = endGame   

    def should_move_player(self, xpos, player, displayWidth):
        x = player.get_position()[0]
        print(x)
        width = player.rect.width

        if x < 0:
            return True
        if x >= displayWidth-width:
            return True
        if (x <= displayWidth/2):
            return True
        if x >= displayWidth/2 and x < displayWidth -width and xpos <= 0 - self.tileSurface.get_width() + game_display.get_width():
            return True
        return False

    def gameLoop(self):
        xpos = 0
        while not self.gameOver:
            xpos += self.x
            if xpos > 0:
                xpos = 0
            elif xpos <= 0 - self.tileSurface.get_width() + game_display.get_width():
                xpos = game_display.get_width() - self.tileSurface.get_width()

            
            self.handleEvent(pygame.event)
            self.game_display.blit(self.tileSurface, (0 + xpos, 0))
            if not self.should_move_player(xpos,self.player, game_display.get_width()):
                self.xmove = 0
            self.player.update(self.xmove)
            self.player.draw(self.game_display)
            pygame.display.update()
            if(self.currentHandler.isEndGame()):
                self.gameOver = True
        self.fps_clock.tick(30)
        
    def handleEvent(self, pygame_event):    
        for event in pygame_event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.x = -5
                    self.xmove = 5
                elif event.key == pygame.K_LEFT:
                    self.x = +5
                    self.xmove = -5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.x = 0
                    self.xmove = 0
                elif event.key == pygame.K_LEFT:
                    self.x = 0
                    self.xmove = 0

ZoeyGame(game_display)