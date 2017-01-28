import sys
sys.path.insert(0, "/home/michael/dev/python/ZoeyGame")
import ZoeyGameEventHandler
import pygame

#initiate pygame
pygame.init()
game_display = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Princess Zoey's Adventure")
fps_clock = pygame.time.Clock()


gameOver = False

currentHandler = ZoeyGameEventHandler.GamePlayEventHandler()

def endGame(bool_endGame):
    gameOver = endGame

while not gameOver:
    game_display.fill((255,255,255))
    pygame.display.update()
    currentHandler.handleEvent(pygame.event)
    if(currentHandler.isEndGame()):
        gameOver = True
