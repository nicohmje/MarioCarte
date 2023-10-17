import pygame
from grass import Grass 
import track

class Lava():  # Vous pouvez ajouter des classes parentes
    surface_type = 0.02
    color = (255, 0, 0)

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        pass
    
    def draw(self, screen):
        if (Grass.texture_image is None):
            pygame.draw.rect(screen, self.color, self.rect)    
        pass
    
    # A completer