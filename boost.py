import track
import pygame

class Boost():  # Vous pouvez ajouter des classes parentes
    
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.surface_type = 0.1 
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)    
        pass
    
    # A completer