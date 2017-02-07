import GameEventHandlers
import pygame
import pytmx
import os
import numpy
import GameSetting
from PlayerSprite import *
from EnemySprites import *
from GameObjects import Obstacle
import GameObjects

# initiate pygame
pygame.init()
game_display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Flint and Zoeys Adventure")

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


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
        self.powerups = pygame.sprite.Group()
        self.ammo = pygame.sprite.Group()
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
        #TODO externalize level variables
        self.level = Level("/assets/level/test_level.tmx", -.2, 0.8)
        self.tileSurface = self.level.make_map()

        for tile_object in self.level.tmxdata.objects:
            if tile_object.name == "ground":
                self.level.ground.add(
                    Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "nerf_pistol":
                self.level.powerups.add(GameObjects.NerfPistol(tile_object.x, tile_object.y))
            if tile_object.name == "player_spawn":
                self.level.spawn = (tile_object.x, tile_object.y)
            if tile_object.name == "goal":
                self.level.goal = Obstacle(
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
            self.allGameObjects.add(self.level.ammo)
            self.allGameObjects.add(self.level.powerups)

        self.rightBounds = 450
        self.leftBounds = self.rightBounds - 100

    def shiftAll(self):
        #TODO something in this method causing player to "skate"
        xdiff = 0
        if self.player.pos.x > self.rightBounds:
            if self.world_x <= 0 - self.tileSurface.get_width() + game_display.get_width():
                self.world_x = 0 - self.tileSurface.get_width() + game_display.get_width()
                if(self.player.rect.right > game_display.get_width()):
                    self.player.pos.x = game_display.get_width() - self.player.rect.width
            else:
                print('in else '+ str(self.player.pos.x) + ' right bounds ' + str(self.rightBounds))
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
        pygame.mixer.music.set_volume(Game.MUSIC_VOLUME)
        handler = GameEventHandlers.GamePlayEventHandler(self, self.player)
        while not self.gameOver:

            self.game_display.blit(self.tileSurface, (self.world_x, 0))
            bullets = self.player.get_bullets()

            self.do_player_bullet_collisions(bullets)
            
            self.do_player_collisions()

            
            handler.handleEvent()
            bullets.update(self.level.level_gravity, self.game_display.get_width(), self.game_display.get_height())
            self.player.update(self.level.level_friction,
                               self.level.level_gravity, self.tileSurface.get_height())
            self.level.enemies.update(
                self.level.level_friction, self.level.level_gravity)

            # draw platform hitbox
            # self.level.ground.draw(self.game_display)
            # self.allGameObjects.draw(self.game_display)
            self. shiftAll()

            # draw items
            bullets.draw(self.game_display)
            self.level.powerups.draw(self.game_display)
            self.level.enemies.draw(self.game_display)
            self.player.draw(self.game_display)
            pygame.display.update()

            if self.player.is_dead:
                self.death_time = pygame.time.get_ticks()
                self.do_death_sequence()
                self.respawn_player()
                handler.set_player(self.player)

            self.fps_clock.tick(GameSetting.Game.FPS)
        pygame.mixer.music.stop()
        self.do_game_over()
    
    def do_player_collisions(self):
        if pygame.sprite.collide_rect(self.level.goal, self.player):
            print("yea, you win")
            self.gameOver = True

        hits = pygame.sprite.spritecollide(self.player, self.level.enemies, False)
        if hits:
            for hit in hits:
                if self.player.kill_enemy(hit, self.level.level_gravity):
                    self.splat.play()
                    hit.kill()

        collide = pygame.sprite.spritecollide(self.player, self.level.ground, False)
        if collide:
            self.player.set_position(collide[0])

        get_powerup = pygame.sprite.spritecollide(self.player, self.level.powerups, True)
        if get_powerup:
            self.player.set_gun(get_powerup[0])


    def do_player_bullet_collisions(self, bullets):
        if bullets.sprites:
            capped = pygame.sprite.groupcollide(bullets, self.level.enemies, False, True)
            if capped:
                for dart in capped:
                    if dart.velocity.x > 0:
                        dart.acceleration = vec(0, 0)
                        dart.velocity = vec(-GameSetting.Game.DART_BOUNCE, self.level.level_gravity)
                    elif dart.velocity.x < 0:
                        dart.velocity = vec(GameSetting.Game.DART_BOUNCE, self.level.level_gravity)
            
            ground_capped = pygame.sprite.groupcollide(bullets, self.level.ground, False, False)
            if ground_capped:
                for dart in ground_capped:
                    self.level.ammo.add(dart)
                    dart.acceleration = vec(0, 0)
                    dart.velocity = vec(0, 0)
                    dart.rect.y = ground_capped[dart][0].rect.top - dart.rect.height

            pickup_ammo = pygame.sprite.spritecollide(self.player, bullets, True)
            if pickup_ammo:
                for ammo in pickup_ammo:
                    self.player.add_ammo(1)
        self.allGameObjects.add(self.level.ammo)

    def do_game_over(self):
        ending = True
        
        handler = GameEventHandlers.GameOverHandler()
        while ending:
            self.game_over_screen.blit(self.game_over_screen, self.game_over_screen.get_rect())
            game_display.blit(self.game_over_screen, self.game_over_screen.get_rect())
            pygame.display.update()
            ending = handler.handle_event()

    def do_death_sequence(self):
        time = pygame.time.get_ticks()

        death_scene = self.game_display
        pygame.time.delay(200)

        death_scene.blit(self.death_scene, self.death_scene.get_rect())
        game_display.blit(death_scene, death_scene.get_rect())
        pygame.display.update()
        pygame.time.delay(1000)

    def respawn_player(self):
        if self.player_lives == 0:
            self.gameOver = True
        else:
            self.world_x = 0
            self.loadLevel()
            self.player = PlayerSprite(self.level.spawn)
            self.player_lives -= 1


FlintAndZoeyGame(game_display)
