import pygame

class Spritesheet:

    def __init__(self, filename):
        self.COLOR_KEY = (255, 20, 147)  # PINK
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):

        image = pygame.Surface((width, height))
        image.set_colorkey(self.COLOR_KEY)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image

    def get_image_row_column(self, width, height, column, row):
        x = width * column
        y = height * row
        #print('loading image at x:'+ str(x) +" y: " +str(y))
        return self.get_image(x, y, width, height)