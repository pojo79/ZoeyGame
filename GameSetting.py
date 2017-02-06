class Move():

    RIGHT = 'right'
    LEFT  = 'left'
    STOP = 'stop'
    PLAYER_MOVE = 1 
    PLAYER_RUN = 1.6
    PLAYER_JUMP = -15
    PLAYER_POP = -8
    ZERO_THRESHOLD = .001
    PLAYER_BULLET_SPEED = 12
    PLAYER_BULLET_ARC = -4

class Control():
    JOYSTICK_DEADZONE = .3
    JUMP_FOGIVENESS = 200
    JUMP_BUTTON = 1
    RUN_BUTTON = 0
    SHOOT_BUTTON = 2

class Game():
    FPS = 60
    DART_BOUNCE = 2
    MUSIC_VOLUME = 0


