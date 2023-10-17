import track
import pygame
from grass import Grass

class Checkpoint():  # Vous pouvez ajouter des classes parentes
    surface_type = 0.02
    color = (50, 50, 0)
    id = 0

    def __init__(self, x, y, id):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.surface_type = 0.10
        self.id = id
        self.color = (50, 50, id)
        pass
    
    def draw(self, screen):
        if (Grass.texture_image is None):
            pygame.draw.rect(screen, self.color, self.rect) 
        pass    
    # A completer