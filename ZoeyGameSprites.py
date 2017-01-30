import pygame

class PrincessSprite(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./assets/art/zoeyPlaceHolder.png")
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(90, 300)
        

    def get_position(self):
        return (self.rect.x, self.rect.y)

    def draw(self, display):
        display.blit(self.image, self.rect)

    def update(self, xmove, display_width=0, map_width=0):
        self.rect.x = self.rect.x+xmove
        ''' if self.rect.x <0:
            self.rect.x = 0
            print('zero')
        elif self.rect.x + self.rect.width > display_width/1.75:
            if display_width/1.75 + self.rect.width > map_width - display_width/1.75:
                if self.rect.x + self.rect.width > display_width:
                    self.rect.x = display_width - self.rect.width
            else:
                self.rect.x = display_width/1.75 - self.rect.width
            print('width' + str(self.rect.width))
        else:
            self.rect.x = self.rect.x+xmove        
            print('else')
        print(self.rect.x)    
   #     self.rect.move_ip(self.rect.x+xmove, 0) '''
        