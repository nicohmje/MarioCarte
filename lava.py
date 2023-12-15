import pygame
from grass import Grass 
import track


#Class for the lava block

class Lava():  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (159, 45, 32)
    sound = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y):
        self.__rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        pass
    
    def draw(self, screen):
        if (Lava.sound is None):
            Lava.sound = pygame.mixer.Sound("sounds/lava.wav")
        if (Grass.track_texture is None):
            pygame.draw.rect(screen, Lava.__color, self.__rect)    
        pass
    
    # A completer