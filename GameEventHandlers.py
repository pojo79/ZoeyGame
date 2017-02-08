import pygame
import GameSetting

class GamePlayEventHandler(object):

    def __init__(self, game, player):
        self.endGame = False
        self.game = game
        self.player = player

    def set_player(self, player):
        self.player = player

    def handleEvent(self):   
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                self.game.gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    self.player.set_run(True)
                if event.key == pygame.K_q:
                    self.game.gameOver = True
                if event.key == pygame.K_DOWN:
                    self.player.set_duck(True)
                if event.key == pygame.K_RIGHT:
                    self.player.move(GameSetting.Move.RIGHT)
                if event.key == pygame.K_LEFT:
                    self.player.move(GameSetting.Move.LEFT)
                if event.key == pygame.K_SPACE:
                    self.player.add_jump_to_buffer()
                if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                    self.player.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    self.player.set_run(False)
                if event.key == pygame.K_DOWN:
                    self.player.set_duck(False)
                if event.key == pygame.K_RIGHT:
                    self.player.move(GameSetting.Move.RIGHT, True)
                if event.key == pygame.K_LEFT:
                    self.player.move(GameSetting.Move.LEFT, True)
            if event.type == pygame.JOYHATMOTION:
                if event.value[0] == 1:
                    self.player.move(GameSetting.Move.RIGHT)
                if event.value[0] == -1:
                    self.player.move(GameSetting.Move.LEFT)
                if event.value[0] == 0:
                    self.player.move(self.player.direction, True)
                if event.value[1] == -1:
                    self.player.set_duck(True)
                if event.value[1] == 0:
                    self.player.set_duck(False)
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value > GameSetting.Control.JOYSTICK_DEADZONE:
                        self.player.move(GameSetting.Move.RIGHT)
                    if event.value < -GameSetting.Control.JOYSTICK_DEADZONE:
                        self.player.move(GameSetting.Move.LEFT)
                    if event.value <= GameSetting.Control.JOYSTICK_DEADZONE and event.value >= -GameSetting.Control.JOYSTICK_DEADZONE:
                        self.player.move(self.player.direction, True)
                if event.axis == 1:
                    if event.value > -GameSetting.Control.JOYSTICK_DEADZONE:
                        self.player.set_duck(True)
                    else:
                        self.player.set_duck(False)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == GameSetting.Control.JUMP_BUTTON:
                    self.player.add_jump_to_buffer()
                if event.button == GameSetting.Control.RUN_BUTTON:
                    self.player.set_run(True)
                if event.button == GameSetting.Control.SHOOT_BUTTON:
                    self.player.shoot()
            if event.type == pygame.JOYBUTTONUP:
                if event.button == GameSetting.Control.RUN_BUTTON:
                    self.player.set_run(False)

class GameOverHandler(object):

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return False
            if event.type == pygame.JOYBUTTONDOWN:
                return False
        return True