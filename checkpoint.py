import track
import pygame

class Checkpoint():  # Vous pouvez ajouter des classes parentes
    
    def __init__(self, x, y, checkpoint_id):
        self.rect = pygame.Rect(x, y, track.BLOCK_SIZE, track.BLOCK_SIZE)
        self.surface_type = 0.8
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 0), self.rect)    
        pass
    
    # A completer