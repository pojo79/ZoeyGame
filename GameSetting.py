import pygame
class Move():

    RIGHT = 'right'
    LEFT  = 'left'
    STOP = 'stop'
    PLAYER_MOVE = .8 
    PLAYER_RUN = 1.7
    PLAYER_JUMP = -16
    PLAYER_POP = -8
    ZERO_THRESHOLD = .025
    PLAYER_BULLET_SPEED = 12
    PLAYER_BULLET_ARC = -4

class Control():
    JOYSTICK_DEADZONE = .3
    JUMP_FOGIVENESS = 200
    JUMP_BUTTON = 1
    RUN_BUTTON = 0
    SHOOT_BUTTON = 2

class Game():
    DEBUG = False
    WINDOW_HEIGHT = 768
    WINDOW_WIDTH = 1024
    RIGHT_BOUNDS = 450
    LEFT_BOUNDS = 100
    LEVEL_CLEAR_VALUE = 750
    FPS = 60
    COLOR_KEY = (227,59,158)
    NUMBERS_SPRITE_SHEET = "./assets/art/numbers.png"
    NUMBERS_SPRITE_WIDTH = 24
    NUMBERS_SPRITE_HEIGHT = 24
    DEATH_SCENE_OVERLAY = "./assets/art/death_scene.png"
    GAME_OVER_OVERLAY = "./assets/art/game_over.png"
    OVERLAY_IMAGE = "./assets/art/screen_overlay.png"
    START_SCREEN = "./assets/art/start_screen.png"
    OVERLAY_LIVES_POS = 100
    OVERLAY_AMMO_POS = 295
    OVERLAY_SCORE_POS = 820
    OVERLAY_HOMEWORK_POS = 575
    EXTRA_LIFE_PAPERS = 100
    DART_BOUNCE = 3
    MUSIC_VOLUME = .05
    NERF_PISTOL_SPEED = 12
    NERF_PISTOL_ARC = -4
    NERF_PISTOL_START_AMMO = 2
    NERF_RIFLE_SPEED = 18
    NERF_RIFLE_ARC = -3
    NERF_RIFLE_START_AMMO = 6
    NERF_DART_IMAGE = "./assets/art/nerf_dart.png"  
    NERF_PISTOL_IMAGE = "./assets/art/nerf_pistol.png"
    NERF_RIFLE_IMAGE = "./assets/art/nerf_rifle.png"
    PLAYER_START_LIVES = 2
    PAPER_IMAGE = "./assets/art/paper.png"
    PAPER_POINTS = 10
    ENEMY_KILL_SOUND = "./assets/sound/splat.wav"
    EXTRA_LIFE_SOUND = "./assets/sound/extra_life.wav"
    PLAYER_HIT_SOUND = "./assets/sound/player_hit.wav"

class Player():
    PLAYER_JUMP_SOUND = "./assets/sound/jump.wav"
    PLAYER_SHOOT_SOUND = "./assets/sound/pop.wav"
    PLAYER_X_SHRINK = -40
    PLAYER_Y_SHRINK = -10
    ZOEY_SPRITE_SHEET = "./assets/art/zoey_sprite_sheet.png"
    PLAYER_SPRITE_HEIGHT = 80
    PLAYER_SPRITE_WIDTH = 60

class Enemy():
    ZOMBIE_POINT_VALUE = 200
    ZOMBIE_ANIMATE_SPEED = 200
    ZOMBIE_WALK_SPEED = .08
    ZOMBIE_SPRITE_WIDTH = 59
    ZOMBIE_SPRITE_HEIGHT = 96
    ZOMBIE_X_INFLATE = -20
    ZOMBIE_Y_INFLATE = -45
    ZOMBIE_SPRITE_SHEET = "./assets/art/zombie_sprite_sheet.png"
    SKELETON_POINT_VALUE = 400
    SKELETON_SPRITE_SHEET = "./assets/art/skeleton_sprite_sheet.png"
    SKELETON_SPRITE_WIDTH = 48
    SKELETON_SPRITE_HEIGHT = 96
    SKELETON_X_INFLATE = -20
    SKELETON_Y_INFLATE = -45
    SKELETON_ANIMATE_SPEED = 750
    SKELETON_SPRITE_BULLET_WIDTH = 20
    SKELETON_SPRITE_BULLET_HEIGHT = 20
    SKELETON_SPRITE_BULLET_LENGTH = 2
    SKELETON_BULLET_SPRITE = "./assets/art/skeleton_bullet.png"
    SKELETON_SHOOT_RATE = 2500
    SKELETON_BULLET_ARC = -4
    SKELETON_BULLET_SPEED = 18
    GOLFER_POINT_VALUE = 300
    GOLFER_BULLET_SPEED = 12
    GOLFER_BULLET_ARC = -7
    GOLFER_SPRITE_SHEET = "./assets/art/golfer_sprite_sheet.png"
    GOLFER_SOUND = "./assets/sound/Swing.wav"
    GOLFER_SPRITE_WIDTH = 48
    GOLFER_SPRITE_HEIGHT = 96
    GOLFER_X_INFLATE = -20
    GOLFER_Y_INFLATE = -45
    GOLFER_ANIMATE_SPEED = 1000
    GOLFER_BULLET_SPRITE = "./assets/art/golfer_bullet.png"
    GOLFER_SHOOT_RATE = 2000
    GOLF_CART_POINT_VALUE = 300
    GOLF_CART_SPRITE_SHEET = "./assets/art/golf_cart_sprite_sheet.png"
    GOLF_CART_SOUND = "./assets/sound/cart.wav"
    GOLF_CART_SPRITE_WIDTH = 120
    GOLF_CART_SPRITE_HEIGHT = 96
    GOLF_CART_ANIMATE_SPEED = 1000
    GOLF_CART_MOVE_SPEED = 1.5
    GOLFCART_X_INFLATE = -15
    GOLFCART_Y_INFLATE = -40

class ParticleImages(object):
    SMOKE = "./assets/art/particle/smoke.png"
    BLOOD = "./assets/art/particle/blood.png"