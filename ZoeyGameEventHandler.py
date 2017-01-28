import pygame


class GamePlayEventHandler(object):

    def __init__(self):
        self.endGame = False

    def isEndGame(self):
        return self.endGame

    def handleEvent(self, pygame_event):    
        for event in pygame_event.get():
            print(event)
            if event.type == pygame.QUIT:
                self.endGame = True

