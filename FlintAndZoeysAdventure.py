import GameEventHandlers
import pygame
import numpy
import GameSetting
from PlayerSprite import *
from EnemySprites import *
from ScreenUI import *
from GameObjects import Obstacle
import GameObjects
from Level import *
from ParticleSystem import *
from ScrollingBackground import *

# initiate pygame
pygame.init()
game_display = pygame.display.set_mode((GameSetting.Game.WINDOW_WIDTH, GameSetting.Game.WINDOW_HEIGHT))
pygame.display.set_caption("Flint and Zoeys Adventure")

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

class FlintAndZoeyGame(object):
    levels = ["/assets/level/golf_level.tmx","/assets/level/test_level.tmx", "/assets/level/test_level2.tmx"]

    def __init__(self, game_display):
        self.fps_clock = pygame.time.Clock()
        self.current_level = 0
        self.handler = None
        self.gameOver = False
        self.world_x = 0
        self.rightBounds = 0
        self.leftBounds = 0
        self.player_lives = GameSetting.Game.PLAYER_START_LIVES
        self.death_time = None
        self.event_handler = None #set to start screen handler when start screen created
        self.death_scene = pygame.image.load(Game.DEATH_SCENE_OVERLAY).convert_alpha()
        self.game_over_screen = pygame.image.load(Game.GAME_OVER_OVERLAY).convert()
        self.smoke_particle = pygame.image.load(GameSetting.ParticleImages.SMOKE).convert()
        self.smoke_particle.set_colorkey(GameSetting.Game.COLOR_KEY)
        self.allGameObjects = pygame.sprite.Group()
        self.loadLevel(self.current_level)
        self.load_music()
        self.spawn = self.level.spawn
        self.splat = pygame.mixer.Sound("./assets/sound/splat.wav")
        self.game_display = game_display
        self.player = PlayerSprite(self.spawn)
        self.points = 0
        self.particleSystems = []
        self.gameLoop()
        

    def load_music(self):
        pygame.mixer.music.load(self.level.level_bmg)

    def loadLevel(self, level):
        #TODO externalize level variables
        self.level = Level(self.levels[level])
        self.tileSurface = self.level.make_map()
        self.allGameObjects.empty()

        for tile_object in self.level.tmxdata.objects:
            if tile_object.name == "ground":
                self.level.ground.add(
                    Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "nerf_pistol":
                self.level.powerups.add(GameObjects.NerfPistol(tile_object.x, tile_object.y))
            if tile_object.name == "nerf_rifle":
                self.level.powerups.add(GameObjects.NerfRifle(tile_object.x, tile_object.y))
            if tile_object.name == "player_spawn":
                self.level.spawn = (tile_object.x, tile_object.y)
            if tile_object.name == "goal":
                self.level.goal = Obstacle(
                    tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.allGameObjects.add(self.level.goal)
            if tile_object.name == "checkpoint":
                self.level.checkpoints.add(Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "zombie":
                travel = tile_object.properties['travel']
                self.level.enemies.add(
                    Zombie(tile_object.x, tile_object.y, float(travel)))
            if tile_object.name == "skeleton":
                self.level.enemies.add(Skeleton(tile_object.x, tile_object.y))
            if tile_object.name == "golfer":
                self.level.enemies.add(Golfer(tile_object.x, tile_object.y))
            if tile_object.name == "golf_cart":
                trigger = int(tile_object.properties['trigger'])
                self.level.enemies.add(GolfCart(tile_object.x, tile_object.y, trigger))

            self.allGameObjects.add(self.level.ground)
            self.allGameObjects.add(self.level.enemies)
            self.allGameObjects.add(self.level.ammo)
            self.allGameObjects.add(self.level.powerups)
            self.allGameObjects.add(self.level.checkpoints)

        self.rightBounds = GameSetting.Game.RIGHT_BOUNDS
        self.leftBounds = self.rightBounds - GameSetting.Game.LEFT_BOUNDS

    def shiftAll(self):
        #TODO something in this method causing player to "skate"
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
            item.world_shift(xdiff)

        #do particles seperatly becuase they are not in gameobjects group
        for particle in self.particleSystems:
            particle.world_shift(xdiff)

        return xdiff

    def start(self):
        start_game_splash = pygame.image.load(Game.START_SCREEN)
        self.handler = GameEventHandlers.GameStartHandler()
        
        startGame = False
        while not startGame:
            startGame = self.handler.handle_event()
            self.game_display.blit(start_game_splash,(0,0))
            pygame.display.update()
  
    def gameLoop(self):
        self.start()
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(Game.MUSIC_VOLUME)
        gameOverlay = ScreenOverlay()
        self.handler = GameEventHandlers.GamePlayEventHandler(self, self.player)
        force_update = False
        sb = ScrollingBackground(self.level.level_background, self.game_display.get_width(), self.game_display.get_height())

        while not self.gameOver:
            if self.player.is_dead:
                self.death_time = pygame.time.get_ticks()
                self.do_death_sequence()
                self.respawn_player()
                force_update = True

            self.handler.handleEvent()
            xdiff = self. shiftAll()

            sb.update(xdiff)
            sb.draw(self.game_display)
            #self.game_display.blit(self.level.level_background, (self.world_x/3,0))
            self.game_display.blit(self.tileSurface, (self.world_x, 0))
            
            self.player.update(self.level.level_friction,
                               self.level.level_gravity, self.tileSurface.get_height())

            bullets = self.player.get_bullets()
            bullets.update(self.level.level_gravity, self.level.width, self.level.height)
            self.do_player_bullet_collisions(bullets)
            self.do_player_collisions()
            self.do_enemy_ground_detection()
            self.do_enemy_bullet_loop()            
            self.level.enemies.update(self.game_display.get_width(), self.game_display.get_height(),
                self.level.level_friction, self.level.level_gravity, self.player.pos, force_update)
            
            for particleSystem in self.particleSystems:
                particleSystem.update_particles()

            # draw platform hitbox
            # self.level.ground.draw(self.game_display)
            # self.allGameObjects.draw(self.game_display)

            # draw items
            bullets.draw(self.game_display)
            self.level.powerups.draw(self.game_display)
            self.level.ammo.draw(self.game_display)
            self.level.enemies.draw(self.game_display)
            self.player.draw(self.game_display)
            gameOverlay.draw(self.game_display, self.player_lives, self.player.get_ammo(), self.points)
            for particleSystem in self.particleSystems:
                particleSystem.draw_particles(self.game_display)
            pygame.display.update()
            
            self.fps_clock.tick(GameSetting.Game.FPS)
            force_update = False
        pygame.mixer.music.stop()
        self.do_game_over()
    
    def do_enemy_ground_detection(self):
        collisions = pygame.sprite.groupcollide(self.level.enemies, self.level.ground, False, False)
        for collision in collisions:
            collision.set_position(collisions[collision][0])

    def do_enemy_bullet_loop(self):

        for enemy in self.level.enemies:
            enemybullets = enemy.get_bullets()
            if enemybullets:
                enemybullets.update(
                self.level.level_gravity, self.level.width, self.level.height)
                self.do_enemy_bullet_collision(enemybullets)
                enemybullets.draw(self.game_display)
                self.allGameObjects.add(enemybullets)
            
    def do_enemy_bullet_collision(self, bullets):
        playerHit = pygame.sprite.spritecollide(self.player, bullets, False)
        if playerHit:
            self.player.is_dead = True

    def do_player_collisions(self):
        if pygame.sprite.collide_rect(self.level.goal, self.player):
            self.points += GameSetting.Game.LEVEL_CLEAR_VALUE
            self.load_next_level()
        
        checkpoint = pygame.sprite.spritecollide(self.player, self.level.checkpoints, True)
        if checkpoint:
            self.spawn = checkpoint[0].get_map_location()

        hits = pygame.sprite.spritecollide(self.player, self.level.enemies, False)
        if hits:
            for hit in hits:
                if self.player.kill_enemy(hit, self.level.level_gravity):
                    self.splat.play()
                    self.do_kill_enemy(hit)
                    hit.kill()
                    self.points += hit.get_point_worth()

        ground = pygame.sprite.spritecollide(self.player, self.level.ground, False)
        if ground:
            self.player.set_position(ground[0])

        get_powerup = pygame.sprite.spritecollide(self.player, self.level.powerups, True)
        if get_powerup:
            self.player.set_gun(get_powerup[0])

    def do_kill_enemy(self, enemy):
        self.particleSystems.append(ParticleSystem(6,enemy.rect.center, self.smoke_particle))

    def do_player_bullet_collisions(self, bullets):
        if bullets.sprites:
            capped = pygame.sprite.groupcollide(bullets, self.level.enemies, False, True)
            if capped:
                for dart in capped:
                    self.do_kill_enemy(capped[dart][0])
                    self.points += math.floor(capped[dart][0].get_point_worth()/2)
                    if dart.velocity.x > 0:
                        dart.acceleration = vec(0, 0)
                        dart.velocity = vec(-GameSetting.Game.DART_BOUNCE, self.level.level_gravity)
                    elif dart.velocity.x < 0:
                        dart.velocity = vec(GameSetting.Game.DART_BOUNCE, self.level.level_gravity)
            
            ground_capped = pygame.sprite.groupcollide(bullets, self.level.ground, True, False)
            if ground_capped:
                for dart in ground_capped:
                    self.level.ammo.add(dart)
                    dart.acceleration = vec(0, 0)
                    dart.velocity = vec(0, 0)
                    dart.rect.y = ground_capped[dart][0].rect.top - dart.rect.height
                    self.level.ammo.add(dart)

            pickup_ammo = pygame.sprite.spritecollide(self.player, self.level.ammo, True)
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
    
    def do_win_screen(self):
        print("Win")

    def respawn_player(self):
        if self.player_lives == 0:
            self.gameOver = True
        else:
            self.world_x = 0
            self.loadLevel(self.current_level)
            self.player = PlayerSprite(self.spawn)
            self.handler.set_player(self.player)
            self.player_lives -= 1

    def load_next_level(self):

        if not self.current_level >= len(self.levels):
            self.current_level += 1
            self.world_x = 0
            self.loadLevel(self.current_level)
            self.spawn = self.level.spawn
            self.player = PlayerSprite(self.spawn)
            self.handler.set_player(self.player)
        else:
            self.do_win_screen()

FlintAndZoeyGame(game_display)
