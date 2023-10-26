import track
import pygame
from grass import Grass

class Boost():  # Vous pouvez ajouter des classes parentes
    surface_type = 0.02
    color = (245, 254, 0)


    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        pass
    
    def draw(self, screen):
        if (Grass.track_texture is None):
            pygame.draw.rect(screen, self.color, self.rect)    
        pass
    # A completer