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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game.gameOver = True
                if event.key == pygame.K_RIGHT:
                    self.player.move(GameSetting.Move.RIGHT)
                if event.key == pygame.K_LEFT:
                    self.player.move(GameSetting.Move.LEFT)
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.move(GameSetting.Move.RIGHT, True)
                if event.key == pygame.K_LEFT:
                    self.player.move(GameSetting.Move.LEFT, True)