from GameSprites import *
import GameEventHandlers
import pygame
import pytmx
import os
import numpy

# initiate pygame
pygame.init()
game_display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Flint and Zoeys Adventure")


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
        self.ground = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.goal = 0

    def render(self, surface):
        getTile = self.tmxdata.get_tile_image
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    surface.blit(image, (x * self.tmxdata.tilewidth,
                                         y * self.tmxdata.tileheight))

    def load_objects(self):
        for tile_object in self.tmxdata.objects:
            print(tile_object)

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        temp_surface.fill((0, 100, 250))  # blue background
        self.render(temp_surface)
        return temp_surface


class FlintAndZoeyGame(object):

    def __init__(self, game_display):
        self.fps_clock = pygame.time.Clock()
        self.gameOver = False
        self.world_x = 0
        self.rightBounds = 0
        self.leftBounds = 0
        self.player_lives = 3
        self.death_time = None
        self.event_handler = None #set to start screen handler when start screen created
        self.death_scene = pygame.image.load("./assets/art/death_scene.png")
        self.game_over_screen = pygame.image.load("./assets/art/game_over.png").convert()
        self.allGameObjects = pygame.sprite.Group()
        self.loadLevel()
        self.load_music()
        self.splat = pygame.mixer.Sound("./assets/sound/splat.wav")
        self.game_display = game_display
        self.player = PlayerSprite(self.level.spawn)
        self.gameLoop()

    def load_music(self):
        pygame.mixer.music.load("./assets/sound/bgm/Queer.mid")

    def loadLevel(self):
        self.level = Level("/assets/level/test_level.tmx", -.25, 0.8)
        self.tileSurface = self.level.make_map()

        for tile_object in self.level.tmxdata.objects:
            if tile_object.name == "ground":
                self.level.ground.add(
                    obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "player_spawn":
                self.level.spawn = (tile_object.x, tile_object.y)
            if tile_object.name == "goal":
                self.level.goal = obstacle(
                    tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.allGameObjects.add(self.level.goal)
            if tile_object.name == "snake":
                travel = tile_object.properties['travel']
                self.level.enemies.add(
                    snake(tile_object.x, tile_object.y, float(travel)))
            if tile_object.name == "eye":
                self.level.enemies.add(eye(tile_object.x, tile_object.y))

            self.allGameObjects.add(self.level.ground)
            self.allGameObjects.add(self.level.enemies)

        self.rightBounds = 450
        self.leftBounds = self.rightBounds - 100

    def shiftAll(self):
        xdiff = 0
        if self.player.pos.x > self.rightBounds:
            if self.world_x <= 0 - self.tileSurface.get_width() + game_display.get_width():
                self.world_x = 0 - self.tileSurface.get_width() + game_display.get_width()
                if(self.player.rect.right > game_display.get_width()):
                    self.player.pos.x = game_display.get_width() - self.player.rect.width
            else:
                xdiff = math.floor(self.rightBounds - self.player.pos.x)
                self.player.pos.x = self.rightBounds

        if self.player.pos.x <= self.leftBounds:
            if self.world_x >= 0:
                self.world_x = 0
                if self.player.pos.x < 0:
                    self.player.pos.x = 0
            else:
                xdiff = math.floor(self.leftBounds - self.player.pos.x)
                self.player.pos.x = self.leftBounds

        self.world_x += xdiff
        for item in self.allGameObjects:
            item.rect.x += xdiff

    def gameLoop(self):
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(.35)
        handler = GameEventHandlers.GamePlayEventHandler(self, self.player)
        while not self.gameOver:

            self.game_display.blit(self.tileSurface, (self.world_x, 0))
            if pygame.sprite.collide_rect(self.level.goal, self.player):
                print("yea, you win")
                self.gameOver = True

            hits = pygame.sprite.spritecollide(
                self.player, self.level.enemies, False)
            if hits:
                for hit in hits:
                    if self.player.kill_enemy(hit, self.level.level_gravity):
                        self.splat.play()
                        hit.kill()

            collide = pygame.sprite.spritecollide(
                self.player, self.level.ground, False)
            if collide:
                self.player.set_position(collide[0])

            
            handler.handleEvent()
            self.player.update(self.level.level_friction,
                               self.level.level_gravity, self.tileSurface.get_height())
            self.level.enemies.update(
                self.level.level_friction, self.level.level_gravity)

            # draw platform hitbox
            # self.level.ground.draw(self.game_display)
            # self.allGameObjects.draw(self.game_display)
            self. shiftAll()

            # draw items
            self.level.enemies.draw(self.game_display)
            self.player.draw(self.game_display)
            pygame.display.update()

            if self.player.is_dead:
                self.death_time = pygame.time.get_ticks()
                self.do_death_sequence()
                self.respawn_player()
                handler.set_player(self.player)

            self.fps_clock.tick(60)
        pygame.mixer.music.stop()
        self.do_game_over()

    def do_game_over(self):
        ending = True

        while ending:
            self.game_over_screen.blit(self.game_over_screen, self.game_over_screen.get_rect())
            game_display.blit(self.game_over_screen, self.game_over_screen.get_rect())
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    ending = False

    def do_death_sequence(self):
        time = pygame.time.get_ticks()

        death_scene = self.game_display
        pygame.time.delay(200)

        death_scene.blit(self.death_scene, self.death_scene.get_rect())
        game_display.blit(death_scene, death_scene.get_rect())
        pygame.display.update()
        pygame.time.delay(1000)

    def respawn_player(self):
        print('Player Lives = ' + str(self.player_lives))
        if self.player_lives == 0:
            print('In if block')
            self.gameOver = True
        else:
            self.world_x = 0
            self.loadLevel()
            self.player = PlayerSprite(self.level.spawn)
            self.player_lives -= 1
        print('Respawn Lives left = ' + str(self.player_lives))

    def handleEvent(self, pygame_event):
        for event in pygame_event.get():
            if event.type == pygame.QUIT:
                self.gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.gameOver = True

FlintAndZoeyGame(game_display)
