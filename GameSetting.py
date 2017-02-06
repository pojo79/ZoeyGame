class Move():

    RIGHT = 'right'
    LEFT  = 'left'
    STOP = 'stop'
    PLAYER_MOVE = 1.25 
    PLAYER_RUN = 2.60
    PLAYER_JUMP = -15
    PLAYER_POP = -8
    ZERO_THRESHOLD = .05

class Control():
    JOYSTICK_DEADZONE = .3
    JUMP_FOGIVENESS = 200
    JUMP_BUTTON = 1
    RUN_BUTTON = 0
    SHOOT_BUTTON = 2