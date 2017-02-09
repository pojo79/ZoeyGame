import pygame
from GameSetting import Sounds

class SoundManager(object):
    sounds = {}
    sounds['PLAYER_JUMP',pygame.mixer.Sound("./assets/sound/jump.wav")]
        
    
    @classmethod
    def load_sounds(self):
        print('loading sounds')
        self.sounds['PLAYER_JUMP',pygame.mixer.Sound(Sounds.PLAYER_JUMP)]
    
    @classmethod
    def play_sound(self, sound):
        print('printing sounds')
        for key in self.sounds:
            print('printing')
            print(key)
        self.sounds[sound].play()
