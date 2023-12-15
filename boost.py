import track
import pygame
from grass import Grass

class Boost():  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (149, 40, 143)
    sound = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y):
        self.__rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        pass
    
    def draw(self, screen):
        if (Boost.sound is None):
            Boost.sound = pygame.mixer.Sound("sounds/boost.wav")
        if (Grass.track_texture is None):
            pygame.draw.rect(screen, Boost.__color, self.__rect)    
        pass