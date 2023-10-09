import pygame
import track

class Grass():  # Vous pouvez ajouter des classes parentes
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.surface_type = 0.3 
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)    
        pass
    
    # A completer