import pygame

class PrincessSprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/art/zoeyPlaceHolder.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(30, 300)


    def update():
        print('in update')

    