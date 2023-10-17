import pygame
import track

class Grass():  # Vous pouvez ajouter des classes parentes
    surface_type = 0.2
    color = (0,255,0)

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.surface_type = 0.2
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)    
        pass
    
    # A completer