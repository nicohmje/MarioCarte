import track
import pygame
from grass import Grass


#Class for the checkpoint block

class Checkpoint():  # Vous pouvez ajouter des classes parentes
    __surface_type = 0.02
    __color = (255, 184, 104)

    @classmethod
    def surface_type_(cls):
        return cls.__surface_type

    def __init__(self, x, y, id):
        self.__rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        Checkpoint.surface_type = 0.10
        self.id = id
        self.__color = (255, 184, 104)
        pass
    
    def draw(self, screen):
        if (Grass.track_texture is None):
            pygame.draw.rect(screen, Checkpoint.__color, self.__rect) 
            Checkpoint.sound = pygame.mixer.Sound("sounds/checkpoint.wav")

        pass    
    # A completer