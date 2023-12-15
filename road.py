import track
import pygame
from grass import Grass

class Road():  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (33, 41, 48)
    sound = None

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y):
        self.__rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        pass
    
    def draw(self, screen):
        if (Grass.track_texture is None):
            pygame.draw.rect(screen, Road.__color, self.__rect)    
        pass
    
    # A completer